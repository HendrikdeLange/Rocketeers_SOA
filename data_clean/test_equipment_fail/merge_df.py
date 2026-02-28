"""
merge_equipment_claims.py
=========================
Loads the two cleaned datasets, prepares sev by dropping unresolvable
policy_ids and aggregating to one row per policy, then left-merges onto
freq. Policies with no claims receive a claim_amount of 0.

Steps
-----
1.  Load cleaned_freq.csv and cleaned_sev.csv
2.  Drop sev rows where policy_id is NaN or a placeholder (MP-####)
3.  Drop claim_id and claim_seq from sev
4.  Group sev by policy_id and sum claim_amount -> one row per policy
5.  Left-merge freq onto aggregated sev on policy_id
    (every freq row is preserved; unmatched policies get NaN claim_amount)
6.  Where claim_count is null OR 0 in freq, set claim_amount to 0
7.  Save merged_claims.csv

Author : Claude (Anthropic)
"""

# =============================================================================
# CONFIGURATION
# =============================================================================
FREQ_IN    = "cleaned_freq.csv"
SEV_IN     = "cleaned_sev.csv"
MERGED_OUT = "merged_claims.csv"

# Placeholder pattern assigned during cleaning — these rows have no real policy
PLACEHOLDER_PATTERN = r"^MP-\d{4,}$"

# =============================================================================
# Imports
# =============================================================================
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
import numpy as np

# =============================================================================
# Helpers
# =============================================================================

def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}]  {msg}")


def section(title: str) -> None:
    log("")
    log("=" * 68)
    log(title)
    log("=" * 68)

# =============================================================================
# STEP 1 — Loading and Deduplicating freq
# =============================================================================
section("STEP 1 — Loading and Deduplicating cleaned datasets")

for p in [FREQ_IN, SEV_IN]:
    if not Path(p).exists():
        sys.exit(f"ERROR: file not found -> {p}")

freq = pd.read_csv(FREQ_IN, sep=";", decimal=".")
sev  = pd.read_csv(SEV_IN,  sep=";", decimal=".")

# --- NEW: Deduplicate freq right away ---
n_freq_before = len(freq)
# Keep the first occurrence of each policy_id
freq = freq.drop_duplicates(subset=["policy_id"]).reset_index(drop=True)
n_freq_after = len(freq)

log(f"  freq: {n_freq_before:,} rows loaded -> {n_freq_after:,} after deduplication")
log(f"  sev : {len(sev):,} rows x {sev.shape[1]} cols")

if n_freq_before > n_freq_after:
    log(f"  [INFO] Dropped {n_freq_before - n_freq_after:,} duplicate policy rows from freq.")
# =============================================================================
# STEP 2 — Drop unresolvable policy_id rows from sev
# =============================================================================
section("STEP 2 — Dropping rows with missing/placeholder policy_id from sev")

n_before = len(sev)

nan_mask         = sev["policy_id"].isna()
placeholder_mask = sev["policy_id"].str.match(PLACEHOLDER_PATTERN, na=False)
drop_mask        = nan_mask | placeholder_mask

sev = sev[~drop_mask].reset_index(drop=True)

log(f"  NaN policy_id rows dropped        : {int(nan_mask.sum())}")
log(f"  Placeholder (MP-####) rows dropped: {int(placeholder_mask.sum())}")
log(f"  sev rows remaining                : {len(sev):,}  (dropped {n_before - len(sev)})")

# =============================================================================
# STEP 3 — Drop claim_id and claim_seq
# =============================================================================
section("STEP 3 — Dropping claim_id and claim_seq")

cols_to_drop = [c for c in ["claim_id", "claim_seq"] if c in sev.columns]
sev = sev.drop(columns=cols_to_drop)

log(f"  Dropped columns: {cols_to_drop}")
log(f"  sev columns remaining: {sev.columns.tolist()}")

# =============================================================================
# STEP 4 — Group sev by policy_id, sum claim_amount
# =============================================================================
section("STEP 4 — Grouping sev by policy_id, summing claim_amount")

# After dropping claim_id and claim_seq the only remaining sev columns are
# policy_id, equipment_id, equipment_type, equipment_age, solar_system,
# maintenance_int, usage_int, exposure, and claim_amount.
# Grouping on policy_id and summing claim_amount collapses to one row per
# policy — all other repeated columns are discarded since freq is the
# authoritative source for those fields.

sev_agg = (
    sev.groupby("policy_id", as_index=False)["claim_amount"]
    .sum()
    .rename(columns={"claim_amount": "total_claim_amount"})
)

log(f"  sev rows before grouping : {len(sev):,}")
log(f"  Unique policy_ids in sev : {sev['policy_id'].nunique():,}")
log(f"  sev rows after grouping  : {len(sev_agg):,}  (one row per policy)")
log(f"  Total claim_amount (sev) : {sev['claim_amount'].sum():,.2f}")
log(f"  Total after aggregation  : {sev_agg['total_claim_amount'].sum():,.2f}  (should match)")

# =============================================================================
# STEP 5 — Left-merge freq onto aggregated sev
# =============================================================================
section("STEP 5 — Left-merging freq onto aggregated sev on policy_id")
log("  Join type: LEFT from freq — all freq rows preserved")

merged = freq.merge(sev_agg, on="policy_id", how="left")

n_matched   = int(merged["total_claim_amount"].notna().sum())
n_unmatched = int(merged["total_claim_amount"].isna().sum())

log(f"  Merged rows              : {len(merged):,}")
log(f"  Matched (have sev data)  : {n_matched:,}")
log(f"  Unmatched (no sev rows)  : {n_unmatched:,}  (will receive claim_amount = 0)")

# =============================================================================
# STEP 6 — Set claim_amount = 0 where claim_count is null or 0
# =============================================================================
section("STEP 6 — Enforcing claim_amount = 0 where claim_count is null or 0")

# Rule: a policy with no claims (claim_count null or 0) cannot have a
# positive claim amount. Set to 0 in both cases to keep the data consistent.
no_claims_mask = merged["claim_count"].isna() | (merged["claim_count"] == 0)

# Also null out claim_amount for any unmatched rows (NaN from left join)
# that weren't already caught by the claim_count rule
unmatched_mask = merged["total_claim_amount"].isna()

zero_mask = no_claims_mask | unmatched_mask
n_zeroed  = int(zero_mask.sum())

merged.loc[zero_mask, "total_claim_amount"] = 0.0

log(f"  Rows with claim_count null or 0  : {int(no_claims_mask.sum()):,}")
log(f"  Additional unmatched rows zeroed : {int((unmatched_mask & ~no_claims_mask).sum()):,}")
log(f"  Total rows set to 0              : {n_zeroed:,}")
log(f"  Total claim_amount in merged     : {merged['total_claim_amount'].sum():,.2f}")

# Final dtype — total_claim_amount should be float throughout
merged["total_claim_amount"] = merged["total_claim_amount"].astype(float)

# =============================================================================
# STEP 7 — Save
# =============================================================================
section("STEP 7 — Saving merged dataset")

merged.to_csv(MERGED_OUT, sep=";", decimal=".", index=False)

log(f"  Saved -> {MERGED_OUT}")
log(f"  Final shape: {len(merged):,} rows x {merged.shape[1]} cols")
log(f"  Columns: {merged.columns.tolist()}")

# Quick sanity checks
section("Sanity Checks")

# 1. Row count should equal freq row count (left join)
assert len(merged) == len(freq), (
    f"FAIL: merged has {len(merged)} rows but freq has {len(freq)}"
)
log(f"  [PASS] Row count matches freq ({len(merged):,} rows)")

# 2. No negative claim amounts
neg = (merged["total_claim_amount"] < 0).sum()
assert neg == 0, f"FAIL: {neg} negative claim_amount values in merged"
log(f"  [PASS] No negative total_claim_amount values")

# 3. No NaN in total_claim_amount
nan_amt = merged["total_claim_amount"].isna().sum()
assert nan_amt == 0, f"FAIL: {nan_amt} NaN in total_claim_amount"
log(f"  [PASS] No NaN in total_claim_amount")

# 4. Policies with claim_count = 0 all have total_claim_amount = 0
zero_count_nonzero_amt = (
    (merged["claim_count"] == 0) & (merged["total_claim_amount"] > 0)
).sum()
assert zero_count_nonzero_amt == 0, (
    f"FAIL: {zero_count_nonzero_amt} rows have claim_count=0 but total_claim_amount>0"
)
log(f"  [PASS] All claim_count=0 rows have total_claim_amount=0")

# 5. Total claim amount preserved vs sev source
sev_total  = sev["claim_amount"].sum()
mrgd_total = merged["total_claim_amount"].sum()
diff_pct   = abs(mrgd_total - sev_total) / sev_total * 100 if sev_total else 0
status     = "PASS" if diff_pct < 0.01 else "WARN"
log(f"  [{status}] claim_amount total: sev = {sev_total:,.2f} | "
    f"merged = {mrgd_total:,.2f} | diff = {diff_pct:.4f}%")

section("COMPLETE")
log(f"  Output: {MERGED_OUT}  ({len(merged):,} rows x {merged.shape[1]} cols)")