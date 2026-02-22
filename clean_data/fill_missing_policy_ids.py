def fill_missing_policy_ids(sev_df, freq_df):
    missing_mask = sev_df["policy_id"].isna()
    
    for i in sev_df[missing_mask].index:
        station = sev_df.loc[i, "station_id"]
        solar = sev_df.loc[i, "solar_system"]
        production_load = sev_df.loc[i, "production_load"]
        
        match = freq_df[
            (freq_df["station_id"] == station) &
            (freq_df["solar_system"] == solar) &
            (freq_df["claim_count"] != 0) &
            (freq_df["production_load"] == production_load)
        ]
        
        if not match.empty:
            sev_df.loc[i, "policy_id"] = match.iloc[0]["policy_id"]
        else:
            print(f"No match found for index {i} — station: {station}, solar system: {solar}")
    
    return sev_df

