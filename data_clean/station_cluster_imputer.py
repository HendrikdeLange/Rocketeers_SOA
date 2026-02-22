import pandas as pd
import numpy as np


class MissingValueImputer:
    """
    Imputes missing or invalid station_id and solar_system values
    by randomly sampling from provided reference lists.

    Usage
    -----
    imputer = MissingValueImputer(
        station_ids=existing_station_ids,   # list of valid station ids
        solar_systems=["Helionis Cluster", "Epsilon", "Zeta"],  # optional, defaults to spec
    )

    fixed_freq = imputer.impute(business_claims_freq, name="freq")
    fixed_sev  = imputer.impute(business_claims_sev,  name="sev")
    """

    SOLAR_SYSTEMS = ["Helionis Cluster", "Epsilon", "Zeta"]

    def __init__(
        self,
        station_ids: list,
        solar_systems: list = None,
        random_state: int = None,
    ):
        """
        Parameters
        ----------
        station_ids   : list of valid station_id values to sample from
        solar_systems : list of valid solar systems (defaults to the 3 from col_specs)
        random_state  : seed for reproducibility (optional)
        """
        if not station_ids:
            raise ValueError("station_ids list cannot be empty.")

        self.station_ids  = list(station_ids)
        self.solar_systems = list(solar_systems) if solar_systems else self.SOLAR_SYSTEMS
        self.rng          = np.random.default_rng(random_state)

    # ------------------------------------------------------------------ #
    #  Validators (same rules as col_specs)                               #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _is_missing(v) -> bool:
        """True if value is NaN, None, empty string, or whitespace."""
        if v is None:
            return True
        if isinstance(v, float) and np.isnan(v):
            return True
        if isinstance(v, str) and v.strip() == "":
            return True
        return False

    @staticmethod
    def _valid_station_id(v) -> bool:
        import re
        return bool(v and isinstance(v, str) and re.fullmatch(r"[A-Z]\d", str(v).strip()))

    @staticmethod
    def _valid_solar_system(v, valid_set) -> bool:
        return v in valid_set

    # ------------------------------------------------------------------ #
    #  Sampling                                                            #
    # ------------------------------------------------------------------ #
    def _sample_station_id(self) -> str:
        return self.rng.choice(self.station_ids)

    def _sample_solar_system(self) -> str:
        return self.rng.choice(self.solar_systems)

    # ------------------------------------------------------------------ #
    #  Core impute method                                                  #
    # ------------------------------------------------------------------ #
    def impute(self, df: pd.DataFrame, name: str = "dataset") -> pd.DataFrame:
        """
        Impute missing/invalid station_id and solar_system values in df.

        Parameters
        ----------
        df   : the DataFrame to fix (not modified in place)
        name : label used in the audit printout

        Returns
        -------
        fixed DataFrame with no missing/invalid station_id or solar_system
        """
        fixed = df.copy()
        solar_set = set(self.solar_systems)
        log = []

        for idx, row in fixed.iterrows():

            # ── station_id ──────────────────────────────────────────────
            if "station_id" in fixed.columns:
                val = row["station_id"]
                if self._is_missing(val) or not self._valid_station_id(val):
                    new_val = self._sample_station_id()
                    fixed.at[idx, "station_id"] = new_val
                    log.append({
                        "dataset":   name,
                        "row_index": idx,
                        "policy_id": row.get("policy_id", "N/A"),
                        "column":    "station_id",
                        "old_value": val,
                        "new_value": new_val,
                    })

            # ── solar_system ────────────────────────────────────────────
            if "solar_system" in fixed.columns:
                val = row["solar_system"]
                if self._is_missing(val) or not self._valid_solar_system(val, solar_set):
                    new_val = self._sample_solar_system()
                    fixed.at[idx, "solar_system"] = new_val
                    log.append({
                        "dataset":   name,
                        "row_index": idx,
                        "policy_id": row.get("policy_id", "N/A"),
                        "column":    "solar_system",
                        "old_value": val,
                        "new_value": new_val,
                    })

        # ── Audit summary ───────────────────────────────────────────────
        if log:
            print(f"\n=== [{name}] Imputation Log — {len(log)} value(s) filled ===")
            print(pd.DataFrame(log).to_string(index=False))
        else:
            print(f"\n[{name}] No missing or invalid station_id / solar_system values found.")

        return fixed