def reassign_claim_seq(df):
    df = df.sort_values(["policy_id", "claim_id"]).copy()
    df["claim_seq"] = df.groupby("policy_id").cumcount() + 1
    return df

def update_claim_count(freq_df, sev_df):
    policy_summary = (
        sev_df.groupby("policy_id")
        .agg(total_claims=("claim_seq", "max"))
        .reset_index()
    )
    freq_df["claim_count"] = freq_df["policy_id"].map(
        policy_summary.set_index("policy_id")["total_claims"]
    ).fillna(0).astype(int)
    return freq_df