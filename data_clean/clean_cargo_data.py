"""
Cargo Claims Data Pipeline
==========================
Production-quality, vectorised pandas pipeline with modular functions,
minimal printing, and deterministic cleaning steps.
"""

import re
import numpy as np
import pandas as pd


# ── Constants ────────────────────────────────────────────────────────────────

CARGO_VALUE_MAP = {
    "gold":        135_600,
    "platinum":     54_500,
    "cobalt":           52,
    "lithium":          82,
    "rare earths":      85,
    "titanium":          7,
    "supplies":         10,
}

CRITERIA = {
    "cargo_type":        ("notnull", None),
    "cargo_value":       ("range",   (0,    np.inf)),
    "route_risk":        ("isin",    {1, 2, 3, 4, 5}),
    "weight":            ("range",   (0,    np.inf)),
    "distance":          ("range",   (1,    100)),
    "transit_duration":  ("range",   (1,    60)),
    "pilot_experience":  ("range",   (1,    30)),
    "vessel_age":        ("range",   (1,    50)),
    "container_type":    ("notnull", None),
    "solar_radiation":   ("range",   (0,    1)),
    "debris_density":    ("range",   (0,    1)),
    "exposure":          ("range",   (0,    1)),
}

FREQ_FILL_RULES = {
    "cargo_type":       "mode",
    "route_risk":       "median",
    "distance":         "median",
    "transit_duration": "median",
    "pilot_experience": "mode",
    "vessel_age":       "median",
    "container_type":   "mode",
    "solar_radiation":  "median",
    "debris_density":   "median",
    "exposure":         "median",
}

SUFFIX_PATTERN = re.compile(r"_\?{3}\d{4}$")


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
        "policy_id", "shipment_id", "cargo_type", "cargo_value", "weight",
        "route_risk", "distance", "transit_duration", "pilot_experience",
        "vessel_age", "container_type", "solar_radiation", "debris_density",
        "exposure", "claim_count",
    ]
    sev_cols = [
        "claim_id", "claim_seq", "policy_id", "shipment_id", "cargo_type",
        "cargo_value", "weight", "route_risk", "distance", "transit_duration",
        "pilot_experience", "vessel_age", "container_type", "solar_radiation",
        "debris_density", "exposure", "claim_amount",
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
    freq = freq.drop(columns=["claim_count"], errors="ignore")
    sev  = sev.drop(columns=["claim_id", "claim_seq"], errors="ignore")
    return freq, sev


# ── Step 4 – Absolute values on numeric columns ───────────────────────────────

def _abs_numeric(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = df.select_dtypes(include="number").columns
    df = df.copy()
    df[num_cols] = df[num_cols].abs()
    return df


# ── Steps 5-8 – Cross-impute policy_id and shipment_id ───────────────────────

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


# ── Step 11 – Generate missing-ID placeholders in freq ───────────────────────

def generate_missing_policy_ids(freq: pd.DataFrame) -> pd.DataFrame:
    mask  = freq["policy_id"].isna()
    count = mask.sum()
    if count:
        start = 1
        new_ids = [f"MI-{start + i:04d}" for i in range(count)]
        freq = freq.copy()
        freq.loc[mask, "policy_id"] = new_ids
    return freq


# ── Step 12 – General NaN imputation by policy_id ────────────────────────────

def _impute_by_policy(target: pd.DataFrame, source: pd.DataFrame,
                      cols: list[str]) -> pd.DataFrame:
    """For each col, fill NaN in target by looking up the same policy_id in source."""
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
    """Overwrite target[col] entries where target fails and source passes, matched on policy_id."""
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
        # sev ok, freq not → overwrite freq
        freq = _overwrite_col_by_policy(freq, sev,  col, sev_ok,  ~freq_ok)
        # freq ok, sev not → overwrite sev
        sev  = _overwrite_col_by_policy(sev,  freq, col, freq_ok, ~sev_ok)
    return freq, sev


# ── Step 14 – Fill cargo_value / weight from cargo_type ──────────────────────

def _fill_cargo_value_weight(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for cargo, rate in CARGO_VALUE_MAP.items():
        mask_type = df["cargo_type"].str.lower().str.strip() == cargo
        # fill cargo_value from weight
        mask = mask_type & df["cargo_value"].isna() & df["weight"].notna()
        df.loc[mask, "cargo_value"] = df.loc[mask, "weight"] * rate
        # fill weight from cargo_value
        mask = mask_type & df["weight"].isna() & df["cargo_value"].notna()
        df.loc[mask, "weight"] = df.loc[mask, "cargo_value"] / rate
    return df


# ── Step 15 – Freq fallback imputation (mode / median) ───────────────────────

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
        if method == "mode":
            fill_val = freq.loc[~bad_mask, col].mode().iloc[0] if (~bad_mask).any() else np.nan
        else:
            fill_val = freq.loc[~bad_mask, col].median() if (~bad_mask).any() else np.nan
        freq.loc[bad_mask, col] = fill_val
    return freq


# ── Step 16 – Aggregate sev ──────────────────────────────────────────────────

def aggregate_sev(sev: pd.DataFrame) -> pd.DataFrame:
    keys = ["shipment_id", "policy_id"]
    # count before aggregating
    sev = sev.copy()
    sev["_claim_count"] = sev.groupby(keys)["shipment_id"].transform("count")
    non_numeric = sev.select_dtypes(include="object").columns.difference(keys).tolist()
    numeric     = sev.select_dtypes(include="number").columns.difference(["_claim_count"]).tolist()

    agg_dict = {col: "first" for col in non_numeric}
    agg_dict.update({col: "sum" if col == "claim_amount" else "first" for col in numeric})
    agg_dict["_claim_count"] = "first"

    sev_agg = sev.groupby(keys, as_index=False).agg(agg_dict)
    sev_agg = sev_agg.rename(columns={"_claim_count": "claim_count"})
    return sev_agg


# ── Step 17-18 – Merge and final check ───────────────────────────────────────

def merge_datasets(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    merge_keys = ["shipment_id", "policy_id"]

    # Only bring claim_amount and claim_count from sev
    sev_slim = sev[merge_keys + ["claim_amount", "claim_count"]].copy()

    merged = freq.merge(sev_slim, on=merge_keys, how="left")

    # ── freq rows with no matching sev record → claim_amount = 0, claim_count = 0 ──
    no_claim_mask = merged["claim_amount"].isna()
    merged.loc[no_claim_mask, "claim_amount"] = 0.0
    merged.loc[no_claim_mask, "claim_count"]  = 0

    # ── Print policy_ids with NaN weight ─────────────────────────────────────
    nan_weight_ids = merged.loc[merged["weight"].isna(), "policy_id"].dropna().unique()
    if len(nan_weight_ids):
        print(f"\nPolicy IDs with NaN weight ({len(nan_weight_ids)}):\n{sorted(nan_weight_ids)}")

    # ── Generate MI-#### for NaN shipment_id ──────────────────────────────────
    nan_ship_mask = merged["shipment_id"].isna()
    if nan_ship_mask.any():
        # Find the highest existing MI- number across both shipment_id and policy_id
        mi_pattern = re.compile(r"MI-(\d{4})")
        existing_nums = (
            merged[["shipment_id", "policy_id"]]
            .apply(lambda col: col.dropna().str.extract(mi_pattern, expand=False))
            .stack()
            .dropna()
            .astype(int)
        )
        start = int(existing_nums.max()) + 1 if not existing_nums.empty else 1
        new_ids = [f"MI-{start + i:04d}" for i in range(nan_ship_mask.sum())]
        merged.loc[nan_ship_mask, "shipment_id"] = new_ids

    # ── NaN report ────────────────────────────────────────────────────────────
    nan_summary = merged.isna().sum()
    nan_summary = nan_summary[nan_summary > 0]
    if not nan_summary.empty:
        print(f"\nNaN summary in cargo_claims_merged:\n{nan_summary.to_string()}")
    else:
        print("\nNo NaNs detected in cargo_claims_merged.")

    return merged


# ── Main pipeline ─────────────────────────────────────────────────────────────

def run_pipeline(freq_path: str, sev_path: str,
                 output_path: str = "cargo_claims_merged.csv") -> pd.DataFrame:

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
    sev = _cross_impute(sev, freq, key="policy_id", match_on=["shipment_id", "cargo_type"],
                        print_remaining=True,
                        print_label="sev policy_id still NaN after imputation – fix by hand")

    # 6 – Impute freq policy_id from sev
    freq = _cross_impute(freq, sev, key="policy_id", match_on=["shipment_id", "cargo_type"])

    # 7 – Impute sev shipment_id from freq
    sev = _cross_impute(sev, freq, key="shipment_id", match_on=["policy_id", "cargo_type"],
                        print_remaining=True,
                        print_label="sev shipment_id still NaN after imputation – fix by hand")

    # 8 – Impute freq shipment_id from sev
    freq = _cross_impute(freq, sev, key="shipment_id", match_on=["policy_id", "cargo_type"])

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

    # 14 – Fill cargo_value / weight from cargo_type
    freq = _fill_cargo_value_weight(freq)
    sev  = _fill_cargo_value_weight(sev)

    # 15 – Freq fallback imputation (mode / median)
    freq = _freq_fallback_impute(freq)

    # 16 – Aggregate sev
    sev = aggregate_sev(sev)

    # 17-18 – Merge and NaN check
    cargo_claims_merged = merge_datasets(freq, sev)

    # 19 – Save
    cargo_claims_merged.to_csv(output_path, index=False)
    print(f"\nSaved → {output_path}  ({len(cargo_claims_merged):,} rows)")

    # total
    print(f"Total claim_amount: {cargo_claims_merged['claim_amount'].sum():,.2f}")

    return cargo_claims_merged


# ── Entry point ───────────────────────────────────────────────────────────────

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cargo_claims_merged = run_pipeline(
        freq_path=r"messy_data\cargo_claims_freq.csv",
        sev_path=r"messy_data\cargo_claims_sev.csv",
        output_path="cargo_claims_merged.csv",
    )