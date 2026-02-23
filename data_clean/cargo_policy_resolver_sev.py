# policy_resolver.py

import pandas as pd


class PolicyResolver:
    """
    Resolves duplicate policy_id entries in a claims DataFrame.

    Usage (from another script):
        from policy_resolver import PolicyResolver

        resolver = PolicyResolver()
        clean_df = resolver(cargo_claims_sev)
    """

    CORRECT_CARGO_TYPES = [
        "lithium", "cobalt", "supplies", "rare earths",
        "titanium", "platinum", "gold"
    ]

    CORRECT_CONTAINER_TYPES = [
        "QuantumCrate Module", "DockArc Freight Case", "DeepSpace Haulbox",
        "LongHaul Vault Canister", "HardSeal Transit Crate"
    ]

    NUMERIC_BOUNDS = {
        "cargo_value":      (50_000,      680_000_000),
        "weight":           (1_500,       250_000),
        "route_risk":       (1,           5),
        "distance":         (1,           100),
        "transit_duration": (1,           60),
        "pilot_experience": (1,           30),
        "vessel_age":       (1,           50),
        "solar_radiation":  (0,           1),
        "debris_density":   (0,           1),
        "exposure":         (0,           1),
        "claim_amount":     (31_000,      678_000_000),
    }

    SHARED_FIELDS = [
        "shipment_id", "cargo_type", "route_risk", "distance",
        "transit_duration", "pilot_experience", "exposure", "solar_radiation"
    ]

    def __init__(self, verbose: bool = True):
        """
        Args:
            verbose: If True, prints warnings and resolution summary.
        """
        self.verbose = verbose
        self.duplicates_log: list[dict] = []

    def _score_row(self, row: pd.Series) -> int:
        """Score a row by how many validity checks it passes — higher is better."""
        score = 0

        if row.get("cargo_type") in self.CORRECT_CARGO_TYPES:
            score += 1
        if row.get("container_type") in self.CORRECT_CONTAINER_TYPES:
            score += 1

        for col, (lo, hi) in self.NUMERIC_BOUNDS.items():
            if col in row.index and pd.notna(row[col]):
                if lo <= row[col] <= hi:
                    score += 1

        return score

    def _check_consistency(self, policy_id, group: pd.DataFrame) -> None:
        """Warn if shared fields are inconsistent across entries for the same policy."""
        if not self.verbose:
            return
        for field in self.SHARED_FIELDS:
            if field in group.columns:
                unique_vals = group[field].dropna().unique()
                if len(unique_vals) > 1:
                    print(
                        f"[WARNING] policy_id={policy_id} | "
                        f"inconsistent '{field}': {unique_vals.tolist()}"
                    )

    def _resolve_group(self, policy_id, group: pd.DataFrame) -> pd.DataFrame:
        """Pick the best row from a group of duplicate policy entries."""
        self._check_consistency(policy_id, group)

        group = group.copy()
        group["_score"] = group.apply(self._score_row, axis=1)
        best = group.nlargest(1, "_score").drop(columns="_score")

        self.duplicates_log.append({
            "policy_id": policy_id,
            "n_claims":  len(group),
            "claim_ids": group["claim_id"].tolist(),
            "scores":    group["_score"].tolist(),
            "chosen":    best["claim_id"].values[0],
        })

        return best

    def _print_summary(self) -> None:
        if not self.verbose:
            return
        print(f"\nResolved {len(self.duplicates_log)} policy_ids with duplicate entries:")
        for log in self.duplicates_log:
            print(
                f"  policy_id={log['policy_id']} | "
                f"{log['n_claims']} claims {log['claim_ids']} | "
                f"scores={log['scores']} | chosen claim_id={log['chosen']}"
            )

    def resolve(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Main resolution method.

        Args:
            df: Raw claims DataFrame with potential duplicate policy_ids.

        Returns:
            Cleaned DataFrame with one row per claim (best entry kept for duplicates).
        """
        self.duplicates_log = []  # reset log on each call
        results = []

        for policy_id, group in df.groupby("policy_id"):
            if len(group) == 1:
                results.append(group)
            else:
                results.append(self._resolve_group(policy_id, group))

        self._print_summary()
        return pd.concat(results, ignore_index=True)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        """Allows the instance to be called directly: resolver(df)."""
        return self.resolve(df)