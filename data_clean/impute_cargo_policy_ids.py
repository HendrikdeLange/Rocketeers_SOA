import pandas as pd
import numpy as np


def impute_policy_ids(
    cargo_claims_freq: pd.DataFrame,
    cargo_claims_sev: pd.DataFrame,
    match_keys: list[str] = ["exposure", "shipment_id"],
    policy_col: str = "policy_id",
    max_iterations: int = 10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Cross-imputes missing policy_ids between cargo_claims_freq and cargo_claims_sev.

    For each missing policy_id in one dataset, it looks for a row in the OTHER dataset
    that matches on `match_keys` and has a non-null policy_id, then fills it in.
    Iterates back and forth until no more matches are found or max_iterations is reached.

    Args:
        cargo_claims_freq:  Frequency claims DataFrame.
        cargo_claims_sev:   Severity claims DataFrame.
        match_keys:         Columns to match on (default: ["exposure", "shipment_id"]).
        policy_col:         Name of the policy ID column (default: "policy_id").
        max_iterations:     Safety cap on the number of back-and-forth passes.

    Returns:
        (freq_imputed, sev_imputed) — copies of the input DataFrames with policy_ids filled.
    """

    freq = cargo_claims_freq.copy()
    sev = cargo_claims_sev.copy()

    def _impute_one_direction(
        target: pd.DataFrame,
        source: pd.DataFrame,
    ) -> tuple[pd.DataFrame, int]:
        """Fill missing policy_ids in `target` using known ones from `source`."""

        # Build a lookup: match_keys -> policy_id (only where policy_id is known)
        source_known = source.dropna(subset=[policy_col])

        # Drop duplicates on match_keys — if multiple policy_ids share the same
        # key combination, we can't reliably pick one, so we skip ambiguous cases.
        source_lookup = (
            source_known
            .groupby(match_keys)[policy_col]
            .nunique()
            .reset_index(name="_n_unique")
            .merge(source_known[match_keys + [policy_col]], on=match_keys)
        )
        unambiguous = source_lookup[source_lookup["_n_unique"] == 1].drop(
            columns="_n_unique"
        ).drop_duplicates(subset=match_keys)

        lookup_map = unambiguous.set_index(match_keys)[policy_col]

        # Rows in target that are missing a policy_id
        missing_mask = target[policy_col].isna()
        if not missing_mask.any():
            return target, 0

        # Try to find a match for each missing row
        missing_rows = target[missing_mask].copy()
        
        # Build a MultiIndex key from the match columns
        missing_keys = pd.MultiIndex.from_frame(missing_rows[match_keys])
        matched_values = missing_keys.map(lookup_map)  # NaN where no match

        filled_count = int(pd.notna(matched_values).sum())

        if filled_count > 0:
            target = target.copy()
            target.loc[missing_mask, policy_col] = matched_values.values

        return target, filled_count

    # --- Iterative back-and-forth imputation ---
    for iteration in range(1, max_iterations + 1):
        freq_missing_before = freq[policy_col].isna().sum()
        sev_missing_before = sev[policy_col].isna().sum()

        # freq  <-- sev
        freq, filled_in_freq = _impute_one_direction(target=freq, source=sev)
        # sev   <-- freq
        sev, filled_in_sev = _impute_one_direction(target=sev, source=freq)

        freq_missing_after = freq[policy_col].isna().sum()
        sev_missing_after = sev[policy_col].isna().sum()

        print(
            f"Iteration {iteration}: "
            f"freq NaNs {freq_missing_before} → {freq_missing_after} "
            f"(filled {filled_in_freq}),  "
            f"sev NaNs  {sev_missing_before} → {sev_missing_after} "
            f"(filled {filled_in_sev})"
        )

        # Stop early if nothing changed
        if filled_in_freq == 0 and filled_in_sev == 0:
            print("No more matches found — stopping early.")
            break

    remaining_freq = freq[policy_col].isna().sum()
    remaining_sev = sev[policy_col].isna().sum()
    print(
        f"\nDone. Remaining NaNs — freq: {remaining_freq}, sev: {remaining_sev}. "
        f"These rows had no matching counterpart in either dataset."
    )

    return freq, sev