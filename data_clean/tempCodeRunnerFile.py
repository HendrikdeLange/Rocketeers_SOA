"""
Business Interruption Claims – Data Pipeline
=============================================
Production-quality, vectorised pandas code.
Follows all instructions from business_claims_criteria.docx exactly.
"""

import re
import os
import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# 0. CONSTANTS
# ─────────────────────────────────────────────

FREQ_COLS = [
    "policy_id", "station_id", "solar_system", "production_load",
    "energy_backup_score", "supply_chain_index", "avg_crew_exp",
    "maintenance_freq", "safety_compliance", "exposure", "claim_count",
]

SEV_COLS = [
    "claim_id", "claim_seq", "policy_id", "station_id", "solar_system",
    "production_load", "energy_backup_score", "safety_compliance",
    "exposure", "claim_amount",
]

# Columns shared between freq and sev (used for cross-imputation and checker)
SHARED_COLS = [
    "station_id", "solar_system", "production_load",
    "energy_backup_score", "safety_compliance", "exposure",
]

# Suffix pattern to strip: _???#### (3 any-chars + 4 digits)
SUFFIX_PATTERN = re.compile(r"_\w{3}\d{4}$")

# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────

def load_data(freq_path: str, sev_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load freq and sev datasets from South African (semicolon-delimited) CSV files."""
    freq = pd.read_csv(freq_path, sep=";", names=FREQ_COLS, header=0, dtype=str)
    sev  = pd.read_csv(sev_path,  sep=";", names=SEV_COLS,  header=0, dtype=str)
    return freq, sev


# ─────────────────────────────────────────────
# 2. ASSIGN policy_id IN freq
# ─────────────────────────────────────────────

def assign_policy_ids(freq: pd.DataFrame) -> pd.DataFrame:
    """Replace policy_id column with BI-000001 … BI-NNNNNN."""
    freq = freq.copy()
    freq["policy_id"] = [f"BI-{i:06d}" for i in range(1, len(freq) + 1)]
    return freq


# ─────────────────────────────────────────────
# 3. DROP UNWANTED COLUMNS
# ─────────────────────────────────────────────

def drop_columns(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Drop claim_count from freq; drop claim_id and claim_seq from sev."""
    freq = freq.drop(columns=["claim_count"], errors="ignore")
    sev  = sev.drop(columns=["claim_id", "claim_seq"], errors="ignore")
    return freq, sev


# ─────────────────────────────────────────────
# 4. CLEAN CELL VALUES
# ─────────────────────────────────────────────

def strip_spaces(df: pd.DataFrame) -> pd.DataFrame:
    """Strip leading/trailing whitespace from all string cells."""
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda s: s.str.strip())
    return df


def strip_suffix(df: pd.DataFrame) -> pd.DataFrame:
    """Remove trailing _???#### suffix (3 chars + 4 digits) from all string cells."""
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(
        lambda col: col.str.replace(SUFFIX_PATTERN, "", regex=True)
    )
    return df


def clean_cells(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply all cell-level cleaning steps to both dataframes."""
    for transform in [strip_spaces, strip_suffix]:
        freq = transform(freq)
        sev  = transform(sev)
    return freq, sev


# ─────────────────────────────────────────────
# 5. NUMERIC COERCION & ABSOLUTE VALUES
# ─────────────────────────────────────────────

def coerce_numerics(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce numeric-looking columns to float and take absolute values."""
    for col in df.columns:
        converted = pd.to_numeric(df[col], errors="coerce")
        if converted.notna().sum() > 0:          # at least some numeric values
            df[col] = converted.abs()
    return df


# ─────────────────────────────────────────────
# 6. IMPUTE MISSING policy_id IN sev
# ─────────────────────────────────────────────

def impute_sev_policy_id(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    For NaN policy_id rows in sev, look for a freq row with the same
    exposure + production_load and copy its policy_id across.
    Remaining NaNs are printed for manual resolution.
    """
    sev = sev.copy()
    match_cols = ["exposure", "production_load"]

    # Build a lookup: (exposure, production_load) → policy_id from freq
    freq_lookup = (
        freq.dropna(subset=match_cols)
        .drop_duplicates(subset=match_cols)
        .set_index(match_cols)["policy_id"]
    )

    nan_mask = sev["policy_id"].isna()
    if nan_mask.any():
        sev_keys = sev.loc[nan_mask, match_cols]
        imputed  = sev_keys.apply(
            lambda row: freq_lookup.get(tuple(row.values), np.nan), axis=1
        )
        sev.loc[nan_mask, "policy_id"] = imputed.values

    # Report any still-missing policy_ids
    still_nan = sev.loc[sev["policy_id"].isna()].index.tolist()
    if still_nan:
        print("=== sev rows with unresolved NaN policy_id (fix by hand) ===")
        print(sev.loc[still_nan])
    else:
        print("All sev policy_id values successfully imputed.")

    return freq, sev


# ─────────────────────────────────────────────
# 7. CROSS-IMPUTATION (freq ↔ sev via policy_id)
# ─────────────────────────────────────────────

def cross_impute(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    For each shared column and each policy_id:
      - NaN in sev, non-NaN in freq  → copy from freq to sev
      - NaN in freq, non-NaN in sev  → copy from sev to freq
      - Both NaN                     → leave as NaN
      - Both non-NaN but different   → keep originals (no overwrite)
    Uses vectorised merge; does NOT change row order or duplicate rows.
    """
    freq = freq.copy().reset_index(drop=True)
    sev  = sev.copy().reset_index(drop=True)

    # ── freq → sev ──
    freq_sub = freq[["policy_id"] + SHARED_COLS].drop_duplicates("policy_id")
    sev_merged = sev.merge(freq_sub, on="policy_id", how="left", suffixes=("", "_freq"))

    for col in SHARED_COLS:
        freq_col = f"{col}_freq"
        if freq_col in sev_merged.columns:
            fill_mask = sev_merged[col].isna() & sev_merged[freq_col].notna()
            sev_merged.loc[fill_mask, col] = sev_merged.loc[fill_mask, freq_col]
        sev_merged.drop(columns=[f"{col}_freq"], errors="ignore", inplace=True)

    sev = sev_merged[sev.columns].copy()

    # ── sev → freq ──
    sev_sub = sev[["policy_id"] + SHARED_COLS].drop_duplicates("policy_id")
    freq_merged = freq.merge(sev_sub, on="policy_id", how="left", suffixes=("", "_sev"))

    for col in SHARED_COLS:
        sev_col = f"{col}_sev"
        if sev_col in freq_merged.columns:
            fill_mask = freq_merged[col].isna() & freq_merged[sev_col].notna()
            freq_merged.loc[fill_mask, col] = freq_merged.loc[fill_mask, sev_col]
        freq_merged.drop(columns=[f"{col}_sev"], errors="ignore", inplace=True)

    freq = freq_merged[freq.columns].copy()

    return freq, sev


# ─────────────────────────────────────────────
# 8. VALIDITY CHECKER (cross-dataset, Table 0)
# ─────────────────────────────────────────────

def _is_valid(series: pd.Series, col: str) -> pd.Series:
    """Return boolean Series: True where the value meets the column's criteria."""
    if col == "station_id":
        return series.notna()
    elif col == "solar_system":
        return series.notna()
    elif col == "production_load":
        num = pd.to_numeric(series, errors="coerce")
        return num.between(0, 1)
    elif col in ("energy_backup_score", "safety_compliance"):
        num = pd.to_numeric(series, errors="coerce")
        return num.isin([1, 2, 3, 4, 5])
    elif col == "exposure":
        num = pd.to_numeric(series, errors="coerce")
        return num.between(0, 1)
    return pd.Series(True, index=series.index)


def validity_checker(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    For each shared column + policy_id pair:
      - valid in both           → leave as is
      - valid in sev, not freq  → overwrite freq from sev
      - valid in freq, not sev  → overwrite sev from freq
      - invalid in both         → print for manual resolution
    """
    freq = freq.copy()
    sev  = sev.copy()

    checker_cols = ["station_id", "solar_system", "production_load",
                    "energy_backup_score", "safety_compliance", "exposure"]

    conflicts = []

    for col in checker_cols:
        if col not in freq.columns or col not in sev.columns:
            continue

        # Build per-policy_id validity lookup for freq
        freq_valid_map = freq.set_index("policy_id")[col].pipe(
            lambda s: s.where(_is_valid(s, col))
        )
        sev_valid_map = sev.set_index("policy_id")[col].pipe(
            lambda s: s.where(_is_valid(s, col))
        )

        # Align on policy_id
        all_pids = sev["policy_id"].dropna().unique()
        for pid in all_pids:
            if pid not in freq_valid_map.index:
                continue

            f_val  = freq.loc[freq["policy_id"] == pid, col]
            s_val  = sev.loc[sev["policy_id"]  == pid, col]
            f_ok   = _is_valid(f_val, col).all()
            s_ok   = _is_valid(s_val, col).all()

            if f_ok and s_ok:
                pass  # leave as is

            elif s_ok and not f_ok:
                # sev is valid → overwrite freq
                representative = s_val.mode()
                if not representative.empty:
                    freq.loc[freq["policy_id"] == pid, col] = representative.iloc[0]

            elif f_ok and not s_ok:
                # freq is valid → overwrite sev
                representative = f_val.mode()
                if not representative.empty:
                    sev.loc[sev["policy_id"] == pid, col] = representative.iloc[0]

            else:
                # neither is valid
                conflicts.append({"policy_id": pid, "column": col,
                                  "freq_value": f_val.values.tolist(),
                                  "sev_value":  s_val.values.tolist()})

    if conflicts:
        print("=== Validity conflicts – resolve by hand ===")
        print(pd.DataFrame(conflicts).to_string(index=False))
    else:
        print("No validity conflicts detected.")

    return freq, sev


# ─────────────────────────────────────────────
# 9. FREQ COLUMN IMPUTATION (Table 1)
# ─────────────────────────────────────────────

def _impute_col(series: pd.Series, col: str) -> pd.Series:
    """Apply Table-1 imputation rules to a single freq column."""
    s = series.copy()

    if col == "station_id":
        mode_val = s.mode().iloc[0] if not s.mode().empty else np.nan
        s = s.fillna(mode_val)

    elif col == "solar_system":
        mode_val = s.mode().iloc[0] if not s.mode().empty else np.nan
        s = s.fillna(mode_val)

    elif col == "production_load":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.between(0, 1) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "energy_backup_score":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.isin([1, 2, 3, 4, 5]) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "supply_chain_index":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.isin([1, 2, 3, 4, 5]) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "avg_crew_exp":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.between(1, 30) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "maintenance_freq":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.isin([0, 1, 2, 3, 4, 5, 6]) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "safety_compliance":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.isin([1, 2, 3, 4, 5]) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    elif col == "exposure":
        num = pd.to_numeric(s, errors="coerce")
        bad = ~num.between(0, 1) | num.isna()
        s.loc[bad] = num.loc[~bad].median()

    return s


def impute_freq_columns(freq: pd.DataFrame) -> pd.DataFrame:
    """Apply Table-1 imputation rules to all relevant freq columns."""
    freq = freq.copy()
    impute_cols = [
        "station_id", "solar_system", "production_load", "energy_backup_score",
        "supply_chain_index", "avg_crew_exp", "maintenance_freq",
        "safety_compliance", "exposure",
    ]
    for col in impute_cols:
        if col in freq.columns:
            freq[col] = _impute_col(freq[col], col)
    return freq


# ─────────────────────────────────────────────
# 10. AGGREGATE sev → claim_count & claim_amount
# ─────────────────────────────────────────────

def aggregate_sev(sev: pd.DataFrame) -> pd.DataFrame:
    """
    1. Count occurrences of each policy_id → claim_count
    2. Sum claim_amount per policy_id
    3. Merge into a single sev_agg dataframe
    """
    sev = sev.copy()
    sev["claim_amount"] = pd.to_numeric(sev["claim_amount"], errors="coerce")

    claim_count_df  = (sev.groupby("policy_id", sort=False)
                          .size()
                          .reset_index(name="claim_count"))

    claim_amount_df = (sev.groupby("policy_id", sort=False)["claim_amount"]
                          .sum()
                          .reset_index())

    sev_agg = claim_count_df.merge(claim_amount_df, on="policy_id", how="inner")
    return sev_agg


# ─────────────────────────────────────────────
# 11. BUILD business_claims_merged
# ─────────────────────────────────────────────

def build_merged(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    """
    Merge aggregated sev onto freq.
    Policies absent from sev get claim_count = 0 and claim_amount = 0.
    """
    sev_agg = aggregate_sev(sev)
    merged  = freq.merge(sev_agg, on="policy_id", how="left")
    merged["claim_count"]  = merged["claim_count"].fillna(0).astype(int)
    merged["claim_amount"] = merged["claim_amount"].fillna(0.0)
    return merged


# ─────────────────────────────────────────────
# 12. NaN CHECK
# ─────────────────────────────────────────────

def check_nans(df: pd.DataFrame, name: str = "business_claims_merged") -> None:
    """Print per-column NaN counts for the final dataset."""
    nan_counts = df.isna().sum()
    nan_counts = nan_counts[nan_counts > 0]
    if nan_counts.empty:
        print(f"{name}: No NaN values found.")
    else:
        print(f"\n=== NaN summary for {name} ===")
        print(nan_counts.to_string())


# ─────────────────────────────────────────────
# 13. MAIN PIPELINE
# ─────────────────────────────────────────────

def run_pipeline(freq_path: str, sev_path: str, output_path: str = "business_claims_merged.csv") -> pd.DataFrame:
    """
    Execute the full end-to-end data pipeline.

    Parameters
    ----------
    freq_path   : path to the frequency CSV (semicolon-delimited, SA format)
    sev_path    : path to the severity  CSV (semicolon-delimited, SA format)
    output_path : destination path for the output CSV

    Returns
    -------
    business_claims_merged : pd.DataFrame
    """
    # 1. Load
    freq, sev = load_data(freq_path, sev_path)

    # 2. Assign deterministic policy_ids
    freq = assign_policy_ids(freq)

    # 3. Drop unwanted columns
    freq, sev = drop_columns(freq, sev)

    # 4. Cell cleaning (strip spaces + strip _???#### suffix)
    freq, sev = clean_cells(freq, sev)

    # 5. Numeric coercion + absolute values
    freq = coerce_numerics(freq)
    sev  = coerce_numerics(sev)

    # 6. Impute missing policy_id in sev; print unresolved for hand-fix
    freq, sev = impute_sev_policy_id(freq, sev)
    # ── hand-fix assumed to have occurred here ──

    # 7. Cross-impute shared columns between freq and sev
    freq, sev = cross_impute(freq, sev)

    # 8. Validity checker (Table 0 criteria, cross-dataset)
    freq, sev = validity_checker(freq, sev)

    # 9. Freq column imputation (Table 1 criteria)
    freq = impute_freq_columns(freq)

    # 10. Build final merged dataset
    business_claims_merged = build_merged(freq, sev)

    # 11. NaN check
    check_nans(business_claims_merged)

    # 12. Save (create output directory if it doesn't exist)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    business_claims_merged.to_csv(output_path, index=False, sep=";")
    print(f"\nSaved → {output_path}  ({len(business_claims_merged):,} rows × {business_claims_merged.shape[1]} cols)")

    return business_claims_merged


# ─────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    # Always resolve paths relative to THIS script's directory,
    # regardless of where the terminal is when the script is run.
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    MESSY_DIR  = os.path.join(SCRIPT_DIR, "..", "messy_data")

    if len(sys.argv) == 3:
        freq_path, sev_path = sys.argv[1], sys.argv[2]
    else:
        freq_path = os.path.join(MESSY_DIR, "business_claims_freq.csv")
        sev_path  = os.path.join(MESSY_DIR, "business_claims_sev.csv")

    business_claims_merged = run_pipeline(
        freq_path  = freq_path,
        sev_path   = sev_path,
        output_path= os.path.join(SCRIPT_DIR, "business_merged.csv"),
    )