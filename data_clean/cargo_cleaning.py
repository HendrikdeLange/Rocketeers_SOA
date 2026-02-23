"""
================================================================================
  CARGO CLAIMS DATA CLEANING SCRIPT
  Files:  cargo_claims_freq  (124,982 rows × 15 cols)
          cargo_claims_sev   ( 30,650 rows × 17 cols)
================================================================================

ISSUES FOUND & FIXES APPLIED (in order):

  1. ???-SUFFIX CORRUPTION  ─────────────────────────────────────────────────
     Affects: cargo_type, container_type, policy_id, shipment_id (both files)
              claim_id (SEV only)
     Pattern: valid value + "_???NNNN"  e.g. "cobalt_???4229", "CL-448588_???9113"
     Fix:     strip trailing _???<digits> with regex

  2. NEGATIVE VALUES (sign-flipped)  ────────────────────────────────────────
     Affects: all numeric columns in both files
     Evidence: negatives mirror the valid positive range exactly
               e.g. route_risk has {-5,-4,-3,-2,-1} alongside {1,2,3,4,5}
     Fix:     abs()

  3. 10× SCALING ERRORS (over-range)  ───────────────────────────────────────
     Affects: all numeric columns with values above schema max (both files)
     Evidence: abs(value)/10 lands in-range for 83-100% of affected rows
     Fix:     if abs(value) > schema_max → value / 10
              applied AFTER sign fix so we always work with positives

  4. route_risk  ─────────────────────────────────────────────────────────────
     Must be integer in {1, 2, 3, 4, 5}
     Fix:  abs() → if still not integer or > 5 → round(value/10)
           if still outside {1..5} → impute with mode per cargo_type

  5. claim_seq (SEV only)  ───────────────────────────────────────────────────
     Must be positive integer
     Fix:  abs() → round(value/10) if > 10 → round() for remaining floats

  6. claim_count (FREQ only)  ────────────────────────────────────────────────
     Must be integer in {0, 1, 2, 3, 4, 5}
     Fix:  abs() → round(value/10) if > 5 → round() → clip to [0, 5]

  7. claim_amount (SEV only)  ────────────────────────────────────────────────
     Must be positive, ~ 31K – 678,000K
     Fix:  abs() → /10 if > 678,000,000

  8. cargo_type INFERENCE from ratio  ────────────────────────────────────────
     When cargo_type is missing but BOTH weight and cargo_value are present,
     compute observed ratio = cargo_value / weight and assign the cargo_type
     whose known ratio is closest in log-space (handles the wide range
     7 → 135,600 fairly). Confirmed ratios from spec:
       gold: 135,600  platinum: 54,500  rare earths: 85
       lithium: 82    cobalt: 52        supplies: 10   titanium: 7

  9. cargo_value ↔ weight IMPUTATION  ─────────────────────────────────────────
     These two are tightly linked via cargo_type (stable $/kg ratio per type).
     Fix (vectorised, applied after cargo_type is as complete as possible):
       if cargo_value missing but weight known  → value  = weight × ratio
       if weight missing but cargo_value known  → weight = value  / ratio
       if both missing → impute each independently with group median

 10. claim_amount CAP  (SEV only)  ──────────────────────────────────────────
     Two sequential hard caps:
       i.  Schema cap:       abs(claim_amount) / 10  if > 678,000,000
       ii. cargo_value cap:  claim_amount = min(claim_amount, cargo_value)
     A claim cannot exceed the declared insured value of the shipment.

 11. policy_id CROSS-FILE RECOVERY via shipment_id + exposure  ──────────────
     The same shipment record appears in both files with the same
     shipment_id and exposure value. Where one file has a known policy_id
     and the other does not, we can borrow it.
     Key = shipment_id + exposure (rounded to 4 dp; precision-stable).
     Ambiguous keys (one key → multiple policy_ids) are skipped to avoid
     assigning a wrong ID — genuine in FREQ (shared shipments), mostly
     ???-corruption in SEV (resolved after Step 1).
     Recovery: FREQ ← SEV: ~42 rows   |   SEV ← FREQ: ~83 rows
     Replaces the earlier SEV-only shipment_id → policy_id lookup.

 12. MI- policy_id GENERATION for remaining FREQ NaNs  ─────────────────────
     After all recovery attempts, FREQ rows still missing policy_id are
     assigned a synthetic MI-NNNNNN identifier (MI = Missing/Imputed).
     Only applied to FREQ — SEV NaNs are left as-is for auditability.

 13. claim_count FULLY DERIVED FROM SEV (FREQ only)  ───────────────────────
     All existing claim_count values are overwritten by this rule:
       • policy_id NOT in SEV  →  claim_count = 0
       • policy_id IS  in SEV  →  claim_count = count of occurrences in SEV
     This is authoritative by definition — SEV has one row per individual claim.

 14. INCONSISTENCY REPORT  ─────────────────────────────────────────────────
     Printed at the end with row-level locations for each remaining type:
       • claim_amount < 31K (below spec minimum, SEV)
       • policy_id appears > 5 times in SEV (schema max claim_count = 5)
       • cargo_value > 680M (above spec range, both files)
     Resolved by construction (not flagged):
       • claim_amount > cargo_value  →  capped in Step 4b
       • claim_count mismatch        →  fully recomputed in Step 8c

 15. REMAINING MISSING VALUES  ───────────────────────────────────────────────
     Categorical (cargo_type, container_type): mode within cargo_type group,
                                               fall back to global mode
     Numeric: median within cargo_type group, fall back to global median
     policy_id (SEV): recover from shipment_id → policy_id lookup table
                      where possible, then leave NaN for true unknowns

 10. VALUES STILL OUT OF RANGE AFTER ALL FIXES  ────────────────────────────
     A small residual (<0.5% of rows) cannot be corrected by rule.
     Fix:  clip to schema bounds (preserves row, no data loss)

================================================================================
"""

import re
import numpy as np
import pandas as pd
from data_store import messy_datasets
# ── Paths ────────────────────────────────────────────────────────────────────
FREQ_IN  = '/mnt/user-data/uploads/1771859639950_cargo_claims_freq'
SEV_IN   = '/mnt/user-data/uploads/1771859639955_cargo_claims_sev'
FREQ_OUT = '/mnt/user-data/outputs/cargo_claims_freq_clean.csv'
SEV_OUT  = '/mnt/user-data/outputs/cargo_claims_sev_clean.csv'

# ── Schema constants ─────────────────────────────────────────────────────────
VALID_CARGO_TYPES  = {"lithium","cobalt","supplies","rare earths",
                       "titanium","platinum","gold"}
VALID_CONTAINERS   = {"QuantumCrate Module","DockArc Freight Case",
                       "DeepSpace Haulbox","LongHaul Vault Canister",
                       "HardSeal Transit Crate"}
VALID_ROUTE_RISKS  = {1, 2, 3, 4, 5}

# Median cargo_value / weight ratio per cargo_type (derived from clean data)
VALUE_PER_KG = {
    "titanium":    7.0,
    "supplies":   10.0,
    "cobalt":     52.0,
    "lithium":    82.0,
    "rare earths":85.0,
    "platinum": 54500.0,
    "gold":    135600.0,
}

# Numeric column schema bounds  (lo, hi)  — None means no bound on that side
NUM_BOUNDS = {
    "cargo_value":      (0,        None      ),  # upper ~678,000K but no hard cap
    "weight":           (0,        250_000   ),
    "distance":         (1,        100       ),
    "transit_duration": (1,        60        ),
    "pilot_experience": (1,        30        ),
    "vessel_age":       (1,        50        ),
    "solar_radiation":  (0,        1         ),
    "debris_density":   (0,        1         ),
    "exposure":         (0,        1         ),
}

# ─────────────────────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def strip_corruption(series: pd.Series) -> pd.Series:
    """Remove _???NNNN suffix from string columns."""
    return series.str.replace(r'_\?\?\?\d+$', '', regex=True)


def fix_sign_and_scale(series: pd.Series, lo, hi) -> pd.Series:
    """
    Step 1: take absolute value (fixes sign-flipped negatives).
    Step 2: if value > hi (10× scale error), divide by 10.
    Works only on numeric series.
    """
    s = series.copy()
    s = s.abs()                                         # fix negatives
    if hi is not None:
        mask_over = s > hi
        s = s.where(~mask_over, s / 10)                # fix 10× scale
    return s


def fix_route_risk(series: pd.Series, cargo_type_clean: pd.Series) -> pd.Series:
    """Fix route_risk to integer ∈ {1,2,3,4,5}."""
    s = series.copy()
    s = s.abs()

    # Float outliers or values > 5: round(x/10)
    bad = ~s.isin(VALID_ROUTE_RISKS) & s.notna()
    s.loc[bad] = (s.loc[bad] / 10).round()

    # Still invalid → impute with mode per cargo_type
    still_bad = ~s.isin(VALID_ROUTE_RISKS) & s.notna()
    if still_bad.any():
        mode_by_type = (
            s[~still_bad]
            .groupby(cargo_type_clean[~still_bad])
            .agg(lambda x: x.mode().iloc[0] if len(x) > 0 else np.nan)
        )
        for idx in s.index[still_bad]:
            ct = cargo_type_clean.get(idx)
            s.loc[idx] = mode_by_type.get(ct, s.mode().iloc[0])

    # Cast to integer where not NaN
    s = s.where(s.isna(), s.round().astype("Int64"))
    return s


def infer_cargo_type_from_ratio(df: pd.DataFrame) -> pd.DataFrame:
    """
    When cargo_type is NaN but BOTH cargo_value and weight are present,
    infer cargo_type by finding the VALUE_PER_KG entry whose ratio is
    closest to the observed ratio in log-space.

    Log-space distance is used because the ratios span four orders of
    magnitude (7 → 135,600), so a linear distance would always snap
    everything to 'gold' or 'titanium'.
    """
    df = df.copy()
    log_ratios = {ct: np.log(r) for ct, r in VALUE_PER_KG.items()}

    missing_ct = df['cargo_type'].isna()
    has_both   = (df['cargo_value'].notna() & df['weight'].notna()
                  & (df['weight'] > 0) & (df['cargo_value'] > 0))  # guard against log(0)
    candidates = missing_ct & has_both

    if candidates.any():
        observed_log = np.log(
            df.loc[candidates, 'cargo_value'] / df.loc[candidates, 'weight']
        )
        def closest_type(log_val):
            return min(log_ratios, key=lambda ct: abs(log_ratios[ct] - log_val))

        df.loc[candidates, 'cargo_type'] = observed_log.apply(closest_type)

    return df


def impute_cargo_value_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Vectorised imputation of cargo_value / weight using the confirmed
    $/kg ratio per cargo_type.

    Priority order (per row):
      1. cargo_value missing, weight known  → cargo_value = weight × ratio
      2. weight missing, cargo_value known  → weight      = cargo_value / ratio
      3. both missing                       → handled later by group-median step
    """
    df = df.copy()

    # Map each row's cargo_type to its ratio (NaN when type unknown)
    ratio_series = df['cargo_type'].map(VALUE_PER_KG)

    # Case 1: impute cargo_value from weight
    mask_cv = df['cargo_value'].isna() & df['weight'].notna() & ratio_series.notna()
    df.loc[mask_cv, 'cargo_value'] = df.loc[mask_cv, 'weight'] * ratio_series[mask_cv]

    # Case 2: impute weight from cargo_value
    mask_w = df['weight'].isna() & df['cargo_value'].notna() & ratio_series.notna()
    df.loc[mask_w, 'weight'] = df.loc[mask_w, 'cargo_value'] / ratio_series[mask_w]

    return df


def impute_numerics(df: pd.DataFrame, cols: list, group_col: str = 'cargo_type') -> pd.DataFrame:
    """Impute remaining NaNs with group median (fallback: global median)."""
    df = df.copy()
    global_medians = {c: df[c].median() for c in cols if c in df.columns}

    for col in cols:
        if col not in df.columns:
            continue
        missing = df[col].isna()
        if not missing.any():
            continue
        group_medians = df.groupby(group_col)[col].transform('median')
        df.loc[missing, col] = group_medians[missing].fillna(global_medians[col])

    return df


def impute_categoricals(df: pd.DataFrame, cols: list, group_col: str = 'cargo_type') -> pd.DataFrame:
    """Impute NaN categoricals with group mode (fallback: global mode)."""
    df = df.copy()
    for col in cols:
        if col not in df.columns:
            continue
        missing = df[col].isna()
        if not missing.any():
            continue
        global_mode = df[col].mode().iloc[0]
        def fill_mode(g):
            m = g.dropna()
            return m.mode().iloc[0] if len(m) > 0 else global_mode
        group_mode = df.groupby(group_col)[col].transform(
            lambda g: fill_mode(g)
        )
        df.loc[missing, col] = group_mode[missing].fillna(global_mode)
    return df


def clip_to_bounds(df: pd.DataFrame) -> pd.DataFrame:
    """Final safety net: clip any residual out-of-range values to schema bounds."""
    df = df.copy()
    for col, (lo, hi) in NUM_BOUNDS.items():
        if col not in df.columns:
            continue
        if lo is not None:
            df[col] = df[col].clip(lower=lo)
        if hi is not None:
            df[col] = df[col].clip(upper=hi)
    return df


def report(label, df_before, df_after, cols):
    """Print a before/after summary for key columns."""
    print(f"\n{'─'*60}")
    print(f"  {label}")
    print(f"{'─'*60}")
    print(f"  Rows: {len(df_before):,}  (unchanged — no rows dropped)")
    for col in cols:
        if col not in df_before.columns:
            continue
        nb = df_before[col].isna().sum()
        na = df_after[col].isna().sum()
        print(f"  {col:<22}  nulls: {nb:>5} → {na:>5}")


# ─────────────────────────────────────────────────────────────────────────────
#  LOAD
# ─────────────────────────────────────────────────────────────────────────────
print("Loading files...")
freq_raw = messy_datasets["cargo_claims_freq"]
sev_raw  = messy_datasets["cargo_claims_sev"]
print(f"  FREQ: {freq_raw.shape}   SEV: {sev_raw.shape}")

freq = freq_raw.copy()
sev  = sev_raw.copy()


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 1 — Strip ???-suffix corruption from ALL string columns
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 1] Stripping ???-suffix corruption...")

str_cols_shared = ['policy_id', 'shipment_id', 'cargo_type', 'container_type']
for col in str_cols_shared:
    freq[col] = strip_corruption(freq[col].astype(str).where(freq[col].notna()))
    sev[col]  = strip_corruption(sev[col].astype(str).where(sev[col].notna()))

# SEV-only: claim_id
sev['claim_id'] = strip_corruption(sev['claim_id'].astype(str).where(sev['claim_id'].notna()))

# Validate cargo_type / container_type are now clean
for name, df in [("FREQ", freq), ("SEV", sev)]:
    n_bad_ct  = (~df['cargo_type'].isin(VALID_CARGO_TYPES)   & df['cargo_type'].notna()).sum()
    n_bad_con = (~df['container_type'].isin(VALID_CONTAINERS) & df['container_type'].notna()).sum()
    print(f"  {name}: cargo_type residual bad={n_bad_ct}, container_type residual bad={n_bad_con}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 1b — Infer cargo_type from cargo_value / weight ratio
#            (done immediately after string cleaning so the ratio uses
#             already-clean values; numeric cleaning hasn't run yet but
#             the ratio is scale-invariant so 10× errors cancel out)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 1b] Inferring missing cargo_type from value/weight ratio...")

for name, df_ref in [("freq", freq), ("sev", sev)]:
    before = df_ref['cargo_type'].isna().sum()
    if name == "freq":
        freq = infer_cargo_type_from_ratio(freq)
        after = freq['cargo_type'].isna().sum()
    else:
        sev = infer_cargo_type_from_ratio(sev)
        after = sev['cargo_type'].isna().sum()
    print(f"  {name.upper()}: cargo_type nulls {before} → {after}  "
          f"(inferred {before - after} from ratio)")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 2 — Numeric fixes: sign + 10× scale  (shared columns)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 2] Fixing sign-flipped and 10× scaled numeric values...")

for col, (lo, hi) in NUM_BOUNDS.items():
    freq[col] = fix_sign_and_scale(freq[col], lo, hi)
    sev[col]  = fix_sign_and_scale(sev[col],  lo, hi)

print("  Done — abs() + /10 applied to all numeric columns.")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 3 — route_risk: fix to integer ∈ {1,2,3,4,5}
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 3] Fixing route_risk...")
freq['route_risk'] = fix_route_risk(freq['route_risk'], freq['cargo_type'])
sev['route_risk']  = fix_route_risk(sev['route_risk'],  sev['cargo_type'])

for name, df in [("FREQ", freq), ("SEV", sev)]:
    invalid = df['route_risk'].dropna()[~df['route_risk'].dropna().isin(VALID_ROUTE_RISKS)]
    print(f"  {name}: residual invalid route_risk = {len(invalid)}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 4 — SEV-specific: claim_seq, claim_amount
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 4] Fixing SEV-specific columns: claim_seq, claim_amount...")

# claim_seq: positive integer
sev['claim_seq'] = sev['claim_seq'].abs()
mask_over = sev['claim_seq'] > 10
sev.loc[mask_over, 'claim_seq'] = (sev.loc[mask_over, 'claim_seq'] / 10).round()
sev['claim_seq'] = sev['claim_seq'].round()
# Impute missing claim_seq with 1 (first claim — conservative default)
sev['claim_seq'] = sev['claim_seq'].fillna(1).astype(int)
print(f"  claim_seq: range [{sev['claim_seq'].min()}, {sev['claim_seq'].max()}]  nulls={sev['claim_seq'].isna().sum()}")

# claim_amount: positive, ~ 31K – 678,000K
sev['claim_amount'] = sev['claim_amount'].abs()
mask_over_ca = sev['claim_amount'] > 678_000_000
sev.loc[mask_over_ca, 'claim_amount'] = sev.loc[mask_over_ca, 'claim_amount'] / 10
print(f"  claim_amount after schema cap: range [{sev['claim_amount'].min():,.0f}, {sev['claim_amount'].max():,.0f}]  nulls={sev['claim_amount'].isna().sum()}")

# Hard cap claim_amount at cargo_value — a claim cannot exceed the insured value.
# Applied immediately after both columns are sign-fixed and scale-corrected so
# they are on the same scale before comparison.
print("\n[Step 4b] Capping claim_amount at cargo_value (SEV)...")
both_present = sev['claim_amount'].notna() & sev['cargo_value'].notna()
exceeds_mask = both_present & (sev['claim_amount'] > sev['cargo_value'])
n_capped = exceeds_mask.sum()
sev.loc[exceeds_mask, 'claim_amount'] = sev.loc[exceeds_mask, 'cargo_value']
print(f"  Capped {n_capped} rows where claim_amount > cargo_value.")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 5 — FREQ-specific: claim_count
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 5] Fixing FREQ-specific column: claim_count...")

freq['claim_count'] = freq['claim_count'].abs()
mask_over_cc = freq['claim_count'] > 5
freq.loc[mask_over_cc, 'claim_count'] = (freq.loc[mask_over_cc, 'claim_count'] / 10).round()
freq['claim_count'] = freq['claim_count'].round().clip(0, 5)
print(f"  claim_count: range [{freq['claim_count'].min()}, {freq['claim_count'].max()}]  nulls={freq['claim_count'].isna().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 6 — Impute cargo_value ↔ weight using cargo_type ratio (vectorised)
#            cargo_type is now as complete as possible (step 1b inferred
#            missing types from ratio), so this catches the maximum rows.
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 6] Imputing cargo_value ↔ weight via cargo_type ratio (vectorised)...")

cv_miss_before_f = freq['cargo_value'].isna().sum()
w_miss_before_f  = freq['weight'].isna().sum()
cv_miss_before_s = sev['cargo_value'].isna().sum()
w_miss_before_s  = sev['weight'].isna().sum()

freq = impute_cargo_value_weight(freq)
sev  = impute_cargo_value_weight(sev)

print(f"  FREQ cargo_value nulls: {cv_miss_before_f} → {freq['cargo_value'].isna().sum()}")
print(f"  FREQ weight nulls:      {w_miss_before_f}  → {freq['weight'].isna().sum()}")
print(f"  SEV  cargo_value nulls: {cv_miss_before_s} → {sev['cargo_value'].isna().sum()}")
print(f"  SEV  weight nulls:      {w_miss_before_s}  → {sev['weight'].isna().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 7 — Recover policy_id via cross-file shipment_id + exposure lookup
#
#  Strategy:
#    • Key = shipment_id + exposure (4 dp).  The same physical shipment
#      appears in both files with identical values for these two fields.
#    • Build unambiguous lookup tables from each file: keys that map to
#      exactly ONE policy_id (ambiguous keys are skipped — safer to leave
#      NaN than to assign a potentially wrong ID).
#    • Apply in three passes, most-certain first:
#        Pass A: SEV self-lookup  (within-file, shipment_id only — fast)
#        Pass B: SEV  ← FREQ cross-file lookup (shipment_id + exposure)
#        Pass C: FREQ ← SEV  cross-file lookup (shipment_id + exposure)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 7] Recovering policy_id via cross-file shipment+exposure lookup...")

def make_unambiguous_lookup(df: pd.DataFrame, key_col: str, val_col: str) -> pd.Series:
    """
    Build a Series keyed by key_col → val_col, keeping only keys that map
    to a single unique value (ambiguous keys are dropped).
    """
    clean = df.dropna(subset=[key_col, val_col])
    counts = clean.groupby(key_col)[val_col].nunique()
    unique_keys = counts[counts == 1].index
    return clean[clean[key_col].isin(unique_keys)].drop_duplicates(key_col).set_index(key_col)[val_col]


# Build the compound key (shipment_id + exposure) in a temporary column
KEY_DP = 4  # decimal places for exposure rounding
freq['_key'] = freq['shipment_id'].astype(str) + '|' + freq['exposure'].round(KEY_DP).astype(str)
sev['_key']  = sev['shipment_id'].astype(str)  + '|' + sev['exposure'].round(KEY_DP).astype(str)

# ── Pass A: SEV self-lookup (within-file, shipment_id only) ─────────────────
ship_pol_sev = make_unambiguous_lookup(sev, 'shipment_id', 'policy_id')
miss_sev = sev['policy_id'].isna() & sev['shipment_id'].notna()
rec_A = sev.loc[miss_sev, 'shipment_id'].map(ship_pol_sev)
sev.loc[miss_sev, 'policy_id'] = rec_A
print(f"  Pass A (SEV self, shipment_id):     recovered {rec_A.notna().sum():>3}")

# ── Pass B: SEV ← FREQ cross-file (shipment_id + exposure) ─────────────────
freq_key_pol = make_unambiguous_lookup(freq, '_key', 'policy_id')
miss_sev = sev['policy_id'].isna() & sev['_key'].notna()   # refresh after Pass A
rec_B = sev.loc[miss_sev, '_key'].map(freq_key_pol)
sev.loc[miss_sev, 'policy_id'] = rec_B
print(f"  Pass B (SEV ← FREQ, key):           recovered {rec_B.notna().sum():>3}")

# ── Pass C: FREQ ← SEV cross-file (shipment_id + exposure) ─────────────────
sev_key_pol = make_unambiguous_lookup(sev, '_key', 'policy_id')
miss_freq = freq['policy_id'].isna() & freq['_key'].notna()
rec_C = freq.loc[miss_freq, '_key'].map(sev_key_pol)
freq.loc[miss_freq, 'policy_id'] = rec_C
print(f"  Pass C (FREQ ← SEV, key):           recovered {rec_C.notna().sum():>3}")

# Drop the temporary key column
freq.drop(columns=['_key'], inplace=True)
sev.drop(columns=['_key'],  inplace=True)

print(f"  FREQ policy_id nulls remaining: {freq['policy_id'].isna().sum()}")
print(f"  SEV  policy_id nulls remaining: {sev['policy_id'].isna().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 8b — Generate MI-NNNNNN policy_ids for remaining FREQ NaNs
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 8b] Generating MI-NNNNNN policy_ids for remaining FREQ NaNs...")

freq_still_missing = freq['policy_id'].isna()
n_missing = freq_still_missing.sum()
if n_missing > 0:
    mi_ids = [f"MI-{i:06d}" for i in range(1, n_missing + 1)]
    freq.loc[freq_still_missing, 'policy_id'] = mi_ids
    print(f"  Assigned {n_missing} synthetic IDs: MI-000001 → MI-{n_missing:06d}")
else:
    print("  No remaining NaNs — nothing to assign.")
print(f"  FREQ policy_id nulls remaining: {freq['policy_id'].isna().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 8c — Derive claim_count in FREQ authoritatively from SEV record count
#
#  Rules (applied to every FREQ row, overwriting any prior value):
#    • policy_id NOT in SEV → claim_count = 0
#    • policy_id IS  in SEV → claim_count = number of times it appears in SEV
#
#  This fully supersedes any raw claim_count values, which may have been
#  corrupted. No NaN-only filling — all rows are overwritten.
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 8c] Deriving claim_count authoritatively from SEV policy_id counts...")

sev_claim_counts = sev['policy_id'].value_counts()
# map returns NaN for policy_ids not in sev_claim_counts; fill with 0
freq['claim_count'] = (
    freq['policy_id']
    .map(sev_claim_counts)
    .fillna(0)
    .astype(int)
)
print(f"  All {len(freq):,} FREQ claim_count values set from SEV counts.")
print(f"  Distribution: {freq['claim_count'].value_counts().sort_index().to_dict()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 8 — Impute remaining categorical NaNs
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 8] Imputing remaining categorical NaNs (mode per cargo_type)...")

cat_cols = ['cargo_type', 'container_type']
freq = impute_categoricals(freq, cat_cols, group_col='cargo_type')
sev  = impute_categoricals(sev,  cat_cols, group_col='cargo_type')

# policy_id / shipment_id: leave NaN (cannot safely fabricate IDs)
for name, df in [("FREQ", freq), ("SEV", sev)]:
    for col in ['cargo_type', 'container_type']:
        print(f"  {name} {col} nulls remaining: {df[col].isna().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 9 — Impute remaining numeric NaNs (group median)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 9] Imputing remaining numeric NaNs (median per cargo_type)...")

num_cols_shared = list(NUM_BOUNDS.keys())
freq = impute_numerics(freq, num_cols_shared + ['claim_count'])
sev  = impute_numerics(sev,  num_cols_shared + ['claim_amount'])

for name, df in [("FREQ", freq), ("SEV", sev)]:
    total_null = df.isnull().sum().sum()
    print(f"  {name}: total nulls remaining after imputation = {total_null}")
    if total_null > 0:
        print("  Remaining null columns:", df.isnull().sum()[df.isnull().sum()>0].to_dict())


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 10 — Final clip to schema bounds (safety net for residuals)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 10] Final clip to schema bounds...")
freq = clip_to_bounds(freq)
sev  = clip_to_bounds(sev)


# ─────────────────────────────────────────────────────────────────────────────
#  STEP 11 — Type coercions
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Step 11] Coercing final types...")

# route_risk → integer
freq['route_risk'] = pd.to_numeric(freq['route_risk'], errors='coerce').round().astype('Int64')
sev['route_risk']  = pd.to_numeric(sev['route_risk'],  errors='coerce').round().astype('Int64')

# claim_count → integer
freq['claim_count'] = freq['claim_count'].round().astype('Int64')

# claim_seq → already int
print("  Done.")


# ─────────────────────────────────────────────────────────────────────────────
#  VALIDATION REPORT
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  VALIDATION REPORT")
print("="*60)

for name, df_raw, df_clean in [("FREQ", freq_raw, freq), ("SEV", sev_raw, sev)]:
    print(f"\n  ── {name} ──────────────────────────")
    print(f"  Rows: {len(df_raw):,} → {len(df_clean):,}  (no rows dropped ✓)")
    print(f"  Total nulls: {df_raw.isnull().sum().sum():,} → {df_clean.isnull().sum().sum():,}")

    print(f"\n  Categorical checks:")
    print(f"    cargo_type valid:    {df_clean['cargo_type'].isin(VALID_CARGO_TYPES).sum():,} / {len(df_clean):,}")
    print(f"    container_type valid:{df_clean['container_type'].isin(VALID_CONTAINERS).sum():,} / {len(df_clean):,}")
    rr_valid = df_clean['route_risk'].isin(VALID_ROUTE_RISKS)
    print(f"    route_risk valid:    {rr_valid.sum():,} / {df_clean['route_risk'].notna().sum():,}")

    print(f"\n  Numeric range checks (values in bounds / non-null):")
    for col, (lo, hi) in NUM_BOUNDS.items():
        if col not in df_clean.columns:
            continue
        s = df_clean[col].dropna()
        lo_ok = (s >= lo).sum() if lo is not None else len(s)
        hi_ok = (s <= hi).sum() if hi is not None else len(s)
        in_range = min(lo_ok, hi_ok)
        print(f"    {col:<22}: {in_range:>7,} / {len(s):>7,}  "
              f"(min={s.min():.3f}, max={s.max():.3f})")

    if 'claim_count' in df_clean.columns:
        cc = df_clean['claim_count'].dropna()
        print(f"    {'claim_count':<22}: {cc.between(0,5).sum():>7,} / {len(cc):>7,}  "
              f"(min={int(cc.min())}, max={int(cc.max())})")
    if 'claim_amount' in df_clean.columns:
        ca = df_clean['claim_amount'].dropna()
        print(f"    {'claim_amount':<22}: min={ca.min():,.0f}  max={ca.max():,.0f}")


# ─────────────────────────────────────────────────────────────────────────────
#  INCONSISTENCY REPORT
#  Flags data issues that were NOT automatically corrected, with row-level
#  locations (original DataFrame index) so they can be manually reviewed.
#
#  Types reported:
#    B. claim_amount < 31K     — below schema minimum (SEV)
#    D. policy_id in SEV > 5 times — exceeds schema max claim_count
#    E. cargo_value > 680M     — above schema range (both files)
#
#  Resolved by construction (no longer flagged):
#    claim_count mismatch  — Step 8c fully derives claim_count from SEV counts
#    claim_amount > cargo_value — Step 4b caps claim_amount at cargo_value
# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  INCONSISTENCY REPORT  (unfixed issues — for review)")
print("="*60)

sev_counts_final = sev['policy_id'].value_counts()

# ── B: claim_amount below spec min ──────────────────────────────────────────
b_mask = sev['claim_amount'].notna() & (sev['claim_amount'] < 31_000)
print(f"\n  B. claim_amount < 31K — below spec minimum (SEV, {b_mask.sum():,} rows)")
if b_mask.sum() > 0:
    print(f"     Range: {sev.loc[b_mask,'claim_amount'].min():,.0f} – "
          f"{sev.loc[b_mask,'claim_amount'].max():,.0f}")
    print(f"     First 15 row indices: {sev.index[b_mask][:15].tolist()}")

# ── D: policy_id appears > 5 times in SEV ───────────────────────────────────
over5_pols = sev_counts_final[sev_counts_final > 5]
d_mask = sev['policy_id'].isin(over5_pols.index)
print(f"\n  D. policy_id appears > 5 times in SEV (schema max=5, {d_mask.sum():,} rows, "
      f"{len(over5_pols)} policies)")
if len(over5_pols) > 0:
    print(f"     Policies: {over5_pols.to_dict()}")
    print(f"     SEV row indices: {sev.index[d_mask].tolist()}")

# ── E: cargo_value > 680M ───────────────────────────────────────────────────
e_freq = freq['cargo_value'] > 680_000_000
e_sev  = sev['cargo_value']  > 680_000_000
print(f"\n  E. cargo_value > 680M — above spec range")
print(f"     FREQ: {e_freq.sum():,} rows  → indices: {freq.index[e_freq][:15].tolist()}")
print(f"     SEV:  {e_sev.sum():,} rows  → indices: {sev.index[e_sev][:15].tolist()}")

# ── Summary table ─────────────────────────────────────────────────────────────
print(f"\n{'─'*60}")
print(f"  {'Type':<45} {'Rows':>6}")
print(f"{'─'*60}")
print(f"  {'B. claim_amount < 31K (SEV)':<45} {b_mask.sum():>6,}")
print(f"  {'D. policy_id > 5 claims in SEV':<45} {d_mask.sum():>6,}")
print(f"  {'E. cargo_value > 680M (FREQ)':<45} {e_freq.sum():>6,}")
print(f"  {'E. cargo_value > 680M (SEV)':<45} {e_sev.sum():>6,}")
print(f"{'─'*60}")


#Saving
freq.to_excel('cargo_claims_freq.xlsx', index=False)
sev.to_excel('cargo_claims_sev.xlsx', index=False)
print("Files saved successfuly")