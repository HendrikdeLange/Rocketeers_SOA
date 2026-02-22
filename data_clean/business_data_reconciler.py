
"""
    I have two datasets with data inconsistencies: both business_claims_freq and business_claims_sev
    Some variables(columns) are in both datasets namely : policy_id , station_id, solar_system, production_load, exposure, 
    energy_backup_score, safety_compliance

    We need to comparee these datasets using policy_id, and decide which variable is best suited as the true value
    How to decide what is the correct value between the two sets? 
    Follow this criteria
    col_specs = {
    "station_id" = eg. A1, G3, F3 etc (1 capital letter + 1 number)
    "solar_system" = {Helionis Cluster, Epsilon, Zeta}
    "production_load":     (0, 1),
    "energy_backup_score": [1, 2, 3, 4, 5],
    "safety_compliance":  [1, 2, 3, 4, 5],
    "exposure":           (0, 1)}
    look in both vars of the respective datatsets and if the vars are not the same, choose the best fitting var using this criteria
    
    create a python class which handles this. 
    The class should return a fixed business_claims_freq and business_claims_sev dataframes
    DO NOT DROP ANY ROWS
    IF BOTH VARS DO NOT MEET CRITERIA, RETURN THE vars in the freq dataset

"""
import pandas as pd
import re


class DatasetReconciler:
    """
    Step 1 — Internal sev reconciliation:
        For rows sharing the same policy_id in sev, resolve column conflicts
        so all rows end up with a single consistent value per shared column.

    Step 2 — Cross-dataset reconciliation:
        Compare freq vs (now-consistent) sev and pick the best value per cell.

    Decision priority (both steps):
        valid value found  → use it
        multiple valid     → use first valid found
        none valid         → keep freq value (cross) / keep first row value (internal)
    """

    SHARED_COLS = [
        "station_id",
        "solar_system",
        "production_load",
        "energy_backup_score",
        "safety_compliance",
        "exposure",
    ]

    # ------------------------------------------------------------------ #
    #  Validators                                                          #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _valid_station_id(v) -> bool:
        return bool(v and isinstance(v, str) and re.fullmatch(r"[A-Z]\d", v.strip()))

    @staticmethod
    def _valid_solar_system(v) -> bool:
        return v in {"Helionis Cluster", "Epsilon", "Zeta"}

    @staticmethod
    def _valid_open_unit_interval(v) -> bool:
        try:
            f = float(v)
            return 0.0 <= f <= 1.0   # inclusive [0, 1]
        except (TypeError, ValueError):
            return False

    @staticmethod
    def _valid_likert_5(v) -> bool:
        try:
            return int(v) in {1, 2, 3, 4, 5} and float(v) == int(v)
        except (TypeError, ValueError):
            return False

    def __init__(self):
        self._validators = {
            "station_id":          self._valid_station_id,
            "solar_system":        self._valid_solar_system,
            "production_load":     self._valid_open_unit_interval,
            "energy_backup_score": self._valid_likert_5,
            "safety_compliance":   self._valid_likert_5,
            "exposure":            self._valid_open_unit_interval,
        }

    # ------------------------------------------------------------------ #
    #  Helpers                                                             #
    # ------------------------------------------------------------------ #
    def _first_valid(self, col: str, values: pd.Series):
        """
        Return the first value in `values` that passes validation,
        or None if none pass.
        """
        validate = self._validators[col]
        for v in values:
            if validate(v):
                return v
        return None

    def _pick_best_value(self, col: str, freq_val, sev_val):
        """
        Cross-dataset picker.
        Priority: sev valid → freq valid → freq fallback.
        """
        validate = self._validators[col]
        if validate(sev_val):
            return sev_val, "sev"
        if validate(freq_val):
            return freq_val, "freq"
        return freq_val, "fallback"

    @staticmethod
    def _scalar_equal(a, b) -> bool:
        try:
            return bool(a == b)
        except (ValueError, TypeError):
            return False

    # ------------------------------------------------------------------ #
    #  Step 1 — Internal sev reconciliation                               #
    # ------------------------------------------------------------------ #
    def _reconcile_sev_internally(
        self,
        sev: pd.DataFrame,
        audit: bool = False,
    ) -> pd.DataFrame:
        """
        For every group of rows sharing the same policy_id in sev:
            - For each shared column, collect all values in the group.
            - If they are not all identical, pick the first valid one.
            - If none are valid, keep the value from the first row (no data loss).
            - Write the resolved value back to every row in the group.
        """
        fixed_sev = sev.copy()
        audit_log = []

        cols_present = [c for c in self.SHARED_COLS if c in sev.columns]

        for pid, group_idx in fixed_sev.groupby("policy_id").groups.items():
            if len(group_idx) == 1:
                continue  # single row — nothing to reconcile

            group = fixed_sev.loc[group_idx]

            for col in cols_present:
                col_values = group[col]

                # Check if all values in the group are already identical
                unique_vals = col_values.unique()
                if len(unique_vals) == 1:
                    continue  # consistent — no action needed

                # Multiple different values — pick the best valid one
                best_val = self._first_valid(col, col_values)

                if best_val is None:
                    # No valid value found → fall back to first row's value
                    best_val = col_values.iloc[0]
                    source   = "fallback (first row)"
                else:
                    source = "first valid"

                if audit:
                    audit_log.append({
                        "policy_id":     pid,
                        "column":        col,
                        "values_found":  list(col_values),
                        "chosen":        best_val,
                        "source":        source,
                    })

                # Write resolved value to every row in the group
                fixed_sev.loc[group_idx, col] = best_val

        if audit and audit_log:
            print("\n=== [Step 1] Internal SEV Reconciliation Log ===")
            print(pd.DataFrame(audit_log).to_string(index=False))
            print(f"\nTotal column groups reconciled: {len(audit_log)}\n")
        elif audit:
            print("[Step 1] No internal sev inconsistencies found.\n")

        return fixed_sev

    # ------------------------------------------------------------------ #
    #  Step 2 — Cross-dataset reconciliation                              #
    # ------------------------------------------------------------------ #
    def reconcile(
        self,
        freq: pd.DataFrame,
        sev: pd.DataFrame,
        audit: bool = False,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Parameters
        ----------
        freq  : business_claims_freq DataFrame
        sev   : business_claims_sev  DataFrame
        audit : print decision logs for both reconciliation steps

        Returns
        -------
        (fixed_freq, fixed_sev) — no rows dropped from either dataset.
        """
        # ── Step 1: clean up sev internally first ──────────────────────
        fixed_sev = self._reconcile_sev_internally(sev, audit=audit)

        # ── Step 2: cross-dataset reconciliation ───────────────────────
        fixed_freq = freq.copy()
        audit_log  = []

        # After step 1, all rows with the same policy_id are consistent,
        # so .first() safely gives us a single representative scalar per pid.
        sev_lookup = fixed_sev.groupby("policy_id").first()

        cols_present = [
            c for c in self.SHARED_COLS
            if c in freq.columns and c in sev.columns
        ]

        for idx, freq_row in freq.iterrows():
            pid      = freq_row["policy_id"]
            freq_val_map = freq_row[cols_present]

            if pid not in sev_lookup.index:
                continue

            for col in cols_present:
                freq_val = freq_row[col]
                sev_val  = sev_lookup.at[pid, col]

                if self._scalar_equal(freq_val, sev_val):
                    continue  # identical — no action needed

                best_val, source = self._pick_best_value(col, freq_val, sev_val)

                # Patch freq
                fixed_freq.at[idx, col] = best_val

                # Patch all matching sev rows
                fixed_sev.loc[fixed_sev["policy_id"] == pid, col] = best_val

                if audit:
                    audit_log.append({
                        "policy_id":  pid,
                        "column":     col,
                        "freq_value": freq_val,
                        "sev_value":  sev_val,
                        "chosen":     best_val,
                        "source":     source,
                    })

        if audit and audit_log:
            print("=== [Step 2] Cross-Dataset Reconciliation Log ===")
            print(pd.DataFrame(audit_log).to_string(index=False))
            print(f"\nTotal cells reconciled: {len(audit_log)}\n")
        elif audit:
            print("[Step 2] No cross-dataset inconsistencies found.\n")

        return fixed_freq, fixed_sev