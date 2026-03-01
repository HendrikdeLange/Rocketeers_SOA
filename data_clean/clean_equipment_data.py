"""
Equipment Claims Data Pipeline
================================
Production-quality, vectorised pandas pipeline with modular functions,
minimal printing, and deterministic cleaning steps.
"""

import re
import numpy as np
import pandas as pd


# ── Constants ────────────────────────────────────────────────────────────────

CRITERIA = {
    "equipment_type":  ("notnull", None),
    "equipment_age":   ("range",   (0,   np.inf)),
    "solar_system":    ("notnull", None),
    "maintenance_int": ("range",   (100, 5000)),
    "usage_int":       ("range",   (0,   24)),
    "exposure":        ("range",   (0,   1)),
}

# method: "mode" | "median" | "mean"
FREQ_FILL_RULES = {
    "equipment_type":  "mode",
    "equipment_age":   "median",
    "solar_system":    "mode",
    "maintenance_int": "mean",
    "usage_int":       "mean",
    "exposure":        "median",
}

SUFFIX_PATTERN = re.compile(r"_\?{3}\d{4}$")
MI_PATTERN     = re.compile(r"MI-(\d{4})")


# ── Step 1 – Load data ───────────────────────────────────────────────────────

def _read_sa_csv(path: str, **kwargs) -> pd.DataFrame:
    """Read a South-African-format CSV (semicolon-delimited, comma decimals)."""
    return (
        pd.read_csv(path, sep=";", decimal=",", **kwargs)
        .pipe(lambda df: df.apply(
            lambda col: col.map(lambda x: str(x).replace(",", ".") if isinstance(x, str) else x)
            if col.dtype == object else col
        ))
    )


def load_data(freq_path: str, sev_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    freq_cols = [
        "policy_id", "equipment_id", "equipment_type", "equipment_age",
        "solar_system", "maintenance_int", "usage_int", "exposure", "claim_counts",
    ]
    sev_cols = [
        "claim_id", "claim_seq", "policy_id", "equipment_id", "equipment_type",
        "equipment_age", "solar_system", "maintenance_int", "usage_int",
        "exposure", "claim_amount",
    ]
    freq = _read_sa_csv(freq_path, names=freq_cols, header=0)
    sev  = _read_sa_csv(sev_path,  names=sev_cols,  header=0)
    return freq, sev


# ── Step 2 – Clean string columns ────────────────────────────────────────────

def _clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Strip whitespace and remove trailing _???#### suffixes from object cols."""
    obj_cols = df.select_dtypes(include="object").columns
    df = df.copy()
    df[obj_cols] = df[obj_cols].apply(lambda col: col.str.strip())
    df[obj_cols] = df[obj_cols].apply(
        lambda col: col.str.replace(SUFFIX_PATTERN, "", regex=True)
    )
    return df


# ── Step 3 – Drop unwanted columns ───────────────────────────────────────────

def drop_columns(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    freq = freq.drop(columns=["claim_counts"], errors="ignore")
    sev  = sev.drop(columns=["claim_id", "claim_seq"], errors="ignore")
    return freq, sev


# ── Step 4 – Absolute values on numeric columns ───────────────────────────────

def _abs_numeric(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = df.select_dtypes(include="number").columns
    df = df.copy()
    df[num_cols] = df[num_cols].abs()
    return df


# ── Steps 5-8 – Cross-impute policy_id and equipment_id ─────────────────────

def _build_lookup(src: pd.DataFrame, key: str, match_on: list[str]) -> pd.Series:
    """Return a Series indexed by tuple(match_on) → key value (first non-null)."""
    valid = src.dropna(subset=[key] + match_on)
    return valid.groupby(match_on)[key].first()


def _cross_impute(target: pd.DataFrame, source: pd.DataFrame,
                  key: str, match_on: list[str],
                  print_remaining: bool = False,
                  print_label: str = "") -> pd.DataFrame:
    lookup = _build_lookup(source, key, match_on)
    mask = target[key].isna()
    if mask.any():
        idx_vals = target.loc[mask, match_on].apply(tuple, axis=1)
        imputed  = idx_vals.map(lookup)
        target   = target.copy()
        target.loc[mask, key] = target.loc[mask, key].fillna(imputed)

    if print_remaining and print_label:
        still_nan = target.loc[target[key].isna(), match_on + [key]]
        if not still_nan.empty:
            print(f"\n{print_label}:\n{still_nan.to_string(index=True)}")
    return target


# ── Step 9 – Policy IDs in sev not in freq ───────────────────────────────────

def report_sev_only_policies(sev: pd.DataFrame, freq: pd.DataFrame) -> None:
    sev_ids  = set(sev["policy_id"].dropna())
    freq_ids = set(freq["policy_id"].dropna())
    only_sev = sorted(sev_ids - freq_ids)
    print(f"\nPolicy IDs in sev but NOT in freq ({len(only_sev)}):\n{only_sev}")


# ── Step 11 – Generate MI-#### placeholders for missing freq policy_ids ───────

def generate_missing_policy_ids(freq: pd.DataFrame) -> pd.DataFrame:
    mask  = freq["policy_id"].isna()
    count = mask.sum()
    if count:
        new_ids = [f"MI-{i + 1:04d}" for i in range(count)]
        freq = freq.copy()
        freq.loc[mask, "policy_id"] = new_ids
    return freq


# ── Step 12 – General NaN imputation by policy_id ────────────────────────────

def _impute_by_policy(target: pd.DataFrame, source: pd.DataFrame,
                      cols: list[str]) -> pd.DataFrame:
    target = target.copy()
    src_lookup = source.dropna(subset=["policy_id"]).groupby("policy_id")[cols].first()
    for col in cols:
        if col not in target.columns or col not in src_lookup.columns:
            continue
        mask = target[col].isna() & target["policy_id"].notna()
        if mask.any():
            target.loc[mask, col] = (
                target.loc[mask, "policy_id"]
                .map(src_lookup[col])
                .combine_first(target.loc[mask, col])
            )
    return target


def cross_impute_by_policy(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    shared_cols = [c for c in freq.columns if c in sev.columns and c != "policy_id"]
    freq = _impute_by_policy(freq, sev,  shared_cols)
    sev  = _impute_by_policy(sev,  freq, shared_cols)
    return freq, sev


# ── Step 13 – Criteria checker and cross-overwrite ───────────────────────────

def _meets_criteria(series: pd.Series, rule: tuple) -> pd.Series:
    kind, param = rule
    if kind == "notnull":
        return series.notna()
    if kind == "range":
        lo, hi = param
        return series.between(lo, hi, inclusive="both")
    if kind == "isin":
        return series.isin(param)
    return pd.Series(True, index=series.index)


def _overwrite_col_by_policy(target: pd.DataFrame, source: pd.DataFrame,
                              col: str, source_ok_mask: pd.Series,
                              target_bad_mask: pd.Series) -> pd.DataFrame:
    rows_to_fix = target_bad_mask & target["policy_id"].notna()
    if not rows_to_fix.any():
        return target
    good_source = source.loc[source_ok_mask & source["policy_id"].notna()].copy()
    src_lookup  = good_source.groupby("policy_id")[col].first()
    target = target.copy()
    target.loc[rows_to_fix, col] = (
        target.loc[rows_to_fix, "policy_id"]
        .map(src_lookup)
        .combine_first(target.loc[rows_to_fix, col])
    )
    return target


def run_criteria_checker(freq: pd.DataFrame, sev: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    for col, rule in CRITERIA.items():
        if col not in freq.columns or col not in sev.columns:
            continue
        freq_ok = _meets_criteria(freq[col], rule)
        sev_ok  = _meets_criteria(sev[col],  rule)
        freq = _overwrite_col_by_policy(freq, sev,  col, sev_ok,  ~freq_ok)
        sev  = _overwrite_col_by_policy(sev,  freq, col, freq_ok, ~sev_ok)
    return freq, sev


# ── Step 14 – Freq fallback imputation (mode / median / mean) ────────────────

def _freq_fallback_impute(freq: pd.DataFrame) -> pd.DataFrame:
    freq = freq.copy()
    for col, method in FREQ_FILL_RULES.items():
        if col not in freq.columns:
            continue
        rule = CRITERIA.get(col)
        if rule is None:
            continue
        bad_mask = ~_meets_criteria(freq[col], rule)
        if not bad_mask.any():
            continue
        valid = freq.loc[~bad_mask, col]
        if method == "mode":
            fill_val = valid.mode().iloc[0] if not valid.empty else np.nan
        elif method == "mean":
            fill_val = valid.mean() if not valid.empty else np.nan
        else:  # median
            fill_val = valid.median() if not valid.empty else np.nan
        freq.loc[bad_mask, col] = fill_val
    return freq


# ── Step 15 – Aggregate sev ──────────────────────────────────────────────────

def aggregate_sev(sev: pd.DataFrame) -> pd.DataFrame:
    keys = ["equipment_id", "policy_id"]
    sev = sev.copy()
    sev["_claim_count"] = sev.groupby(keys)["equipment_id"].transform("count")
    non_numeric = sev.select_dtypes(include="object").columns.difference(keys).tolist()
    numeric     = sev.select_dtypes(include="number").columns.difference(["_claim_count"]).tolist()

    agg_dict = {col: "first" for col in non_numeric}
    agg_dict.update({col: "sum" if col == "claim_amount" else "first" for col in numeric})
    agg_dict["_claim_count"] = "first"

    sev_agg = sev.groupby(keys, as_index=False).agg(agg_dict)
    sev_agg = sev_agg.rename(columns={"_claim_count": "claim_count"})
    return sev_agg


# ── Step 16-17 – Merge and final checks ──────────────────────────────────────

def merge_datasets(freq: pd.DataFrame, sev: pd.DataFrame,
                   sev_claim_total: float) -> pd.DataFrame:
    merge_keys = ["equipment_id", "policy_id"]

    # Only bring claim_amount and claim_count from sev
    sev_slim = sev[merge_keys + ["claim_amount", "claim_count"]].copy()

    merged = freq.merge(sev_slim, on=merge_keys, how="left")

    # freq rows with no matching sev record → claim_amount = 0, claim_count = 0
    no_claim_mask = merged["claim_amount"].isna()
    merged.loc[no_claim_mask, "claim_amount"] = 0.0
    merged.loc[no_claim_mask, "claim_count"]  = 0

    # ── Generate MI-#### for NaN equipment_id ────────────────────────────────
    nan_equip_mask = merged["equipment_id"].isna()
    if nan_equip_mask.any():
        existing_nums = (
            merged[["equipment_id", "policy_id"]]
            .apply(lambda col: col.dropna().str.extract(MI_PATTERN, expand=False))
            .stack()
            .dropna()
            .astype(int)
        )
        start = int(existing_nums.max()) + 1 if not existing_nums.empty else 1
        new_ids = [f"MI-{start + i:04d}" for i in range(nan_equip_mask.sum())]
        merged.loc[nan_equip_mask, "equipment_id"] = new_ids

    # ── Step 18 – Input vs output claim_amount reconciliation ────────────────
    merged_claim_total = merged["claim_amount"].sum()
    print(f"\nClaim amount reconciliation:"
          f"\n  Input  sev  claim_amount total : {sev_claim_total:,.2f}"
          f"\n  Output merged claim_amount total: {merged_claim_total:,.2f}"
          f"\n  Difference                      : {merged_claim_total - sev_claim_total:,.2f}")

    # ── NaN report ────────────────────────────────────────────────────────────
    nan_summary = merged.isna().sum()
    nan_summary = nan_summary[nan_summary > 0]
    if not nan_summary.empty:
        print(f"\nNaN summary in equipment_claims_merged:\n{nan_summary.to_string()}")
    else:
        print("\nNo NaNs detected in equipment_claims_merged.")

    return merged


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(freq_path: str, sev_path: str,
                 output_path: str = "equipment_claims_merged.csv") -> pd.DataFrame:

    # 1 – Load
    freq, sev = load_data(freq_path, sev_path)

    # 2 – Clean string columns
    freq = _clean_string_columns(freq)
    sev  = _clean_string_columns(sev)

    # 3 – Drop columns
    freq, sev = drop_columns(freq, sev)

    # 4 – Absolute values
    freq = _abs_numeric(freq)
    sev  = _abs_numeric(sev)

    # 5 – Impute sev policy_id from freq
    sev = _cross_impute(sev, freq, key="policy_id", match_on=["equipment_id", "equipment_type"],
                        print_remaining=True,
                        print_label="sev policy_id still NaN after imputation – fix by hand")

    # 6 – Impute freq policy_id from sev
    freq = _cross_impute(freq, sev, key="policy_id", match_on=["equipment_id", "equipment_type"])

    # 7 – Impute sev equipment_id from freq
    sev = _cross_impute(sev, freq, key="equipment_id", match_on=["policy_id", "equipment_type"],
                        print_remaining=True,
                        print_label="sev equipment_id still NaN after imputation – fix by hand")

    # 8 – Impute freq equipment_id from sev
    freq = _cross_impute(freq, sev, key="equipment_id", match_on=["policy_id", "equipment_type"])

    # 9 – Report policies in sev not in freq
    report_sev_only_policies(sev, freq)

    # 10 – Drop zero claim_amount rows in sev
    sev = sev.loc[sev["claim_amount"] != 0].copy()

    # 11 – Generate MI-#### for still-missing freq policy_ids
    freq = generate_missing_policy_ids(freq)

    # 12 – General cross-imputation by policy_id
    freq, sev = cross_impute_by_policy(freq, sev)

    # 13 – Criteria checker and cross-overwrite
    freq, sev = run_criteria_checker(freq, sev)

    # 14 – Freq fallback imputation (mode / median / mean)
    freq = _freq_fallback_impute(freq)

    # 15 – Aggregate sev; capture input total before aggregation
    sev_claim_total = sev["claim_amount"].sum()
    sev = aggregate_sev(sev)

    # 16-17 – Merge, NaN check, reconciliation
    equipment_claims_merged = merge_datasets(freq, sev, sev_claim_total)

    # 18 – Save
    equipment_claims_merged.to_csv(output_path, index=False)
    print(f"\nSaved → {output_path}  ({len(equipment_claims_merged):,} rows)")

    return equipment_claims_merged


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    equipment_claims_merged = run_pipeline(
        freq_path=r"messy_data\equipment_claims_freq.csv",
        sev_path=r"messy_data\equipment_claims_sev.csv",
        output_path="equipment_claims_merged.csv",
    )