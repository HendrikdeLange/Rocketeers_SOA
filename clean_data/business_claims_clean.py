from data_store import messy_datasets
import pandas as pd
pd.set_option("display.max_columns", None)
from id_fix import IDCleaner
from fill_missing_policy_ids import fill_missing_policy_ids
from claim_count_fix import reassign_claim_seq, update_claim_count
from absolute_values import make_absolute
from impute_out_of_bounds import impute_out_of_bounds
from fix_solar_system import fix_solar_system
"""
DATASET DOCUMENTATION: Business Interruption Claims
==================================================
Variable Name       | Description                          | Type      | Units       | Value Range or Levels
-----------------------------------------------------------------------------------------------------------
policy_id           | Policy identifier                   | character | --          | e.g., BI-123456, ...
station_id          | Mining platform identifier          | category  | --          | e.g., A1, G3, ...
solar_system        | Solar system identifier             | category  | --          | {Helionis Cluster, Epsilon, Zeta}
production_load     | Avg utilizati
on rate of capacity    | numeric   | Ratio       | 0 – 1
energy_backup_score | Adequacy of emergency power systems | category  | --          | {1, 2, 3, 4, 5}
supply_chain_index  | Proportion of inputs sourced        | numeric   | Ratio       | 0 – 1
avg_crew_exp        | Average experience of assigned staff| numeric   | Earth years | 1 – 30
maintenance_freq    | Expected maintenance cycles / year  | numeric   | Number      | 0 – 6
safety_compliance   | Compliance score                    | category  | --          | {1, 2, 3, 4, 5}
exposure            | Period of exposure in Earth years   | numeric   | Ratio       | 0 – 1
claim_count         | Number of claims during exposure    | numeric   | Number      | 0 – 4
claim_amount        | Claim amount per claim              | numeric   | [currency]  | ~ 28K – 1,426K
"""

business_claims_freq = messy_datasets["business_claims_freq"]
business_claims_sev  = messy_datasets["business_claims_sev"]
print("Datasets loaded correctly!")


business_claims_freq["policy_id"] = IDCleaner(business_claims_freq["policy_id"], 9).broken_id_fix().missing_id_fix().get()
print(f"{IDCleaner(business_claims_freq['policy_id'], 9).validate_ids()} in the business_claims_freq policy_id column!")

business_claims_sev["claim_id"] = IDCleaner(business_claims_sev["claim_id"], 12).broken_id_fix().missing_id_fix().get()
print(f"{IDCleaner(business_claims_sev['claim_id'], 12).validate_ids()} in the business_claims_sev claim_id column!")

business_claims_sev = fill_missing_policy_ids(business_claims_sev, business_claims_freq)
business_claims_sev["policy_id"] = IDCleaner(business_claims_sev["policy_id"], 9).broken_id_fix().get()
print(f"{IDCleaner(business_claims_sev['policy_id'], 9).validate_ids()} in the business_claims_sev policy_id column!")

"""station_id       | e.g., A1, G3, ...
solar_system        | {Helionis Cluster, Epsilon, Zeta}
energy_backup_score | {1, 2, 3, 4, 5}
supply_chain_index  | 0 – 1
avg_crew_exp        |  1 – 30
maintenance_freq    |  0 – 6
safety_compliance   |{1, 2, 3, 4, 5}
exposure            | 0 – 1
claim_count         | 0 – 4"""

# FIXING claim_count + claim_seq
business_claims_sev = reassign_claim_seq(business_claims_sev) # fixes the claim_seq column in business_claims_sev
business_claims_freq = update_claim_count(business_claims_freq, business_claims_sev) # fixes the claim_count column in business_claims_freq

#FIXING station_id 
business_claims_freq["station_id"] = IDCleaner(business_claims_freq["station_id"], 2).broken_id_fix().get()
#print(f"{IDCleaner(business_claims_freq['station_id'], 2).validate_ids()} in the business_claims_freq station_id column!")
business_claims_sev["station_id"] = IDCleaner(business_claims_sev["station_id"], 2).broken_id_fix().get()
#print(f"{IDCleaner(business_claims_sev['station_id'], 2).validate_ids()} in the business_claims_sev station_id column!")

#Taking absolute values of all numeric variables
business_claims_freq = make_absolute(business_claims_freq)
business_claims_sev = make_absolute(business_claims_sev)

#Set columns which have issues to median value
# --- Usage ---
col_specs = {
    "production_load":     (0, 1),
    "energy_backup_score": [1, 2, 3, 4, 5],
    "supply_chain_index": (0, 1),
    "avg_crew_exp":       (1, 30),
    "maintenance_freq":   (0, 6),
    "safety_compliance":  [1, 2, 3, 4, 5],
    "exposure":           (0, 1)
}

business_claims_freq = impute_out_of_bounds(business_claims_freq, col_specs)
business_claims_sev = impute_out_of_bounds(business_claims_sev, col_specs)

#fixing the solar_system
business_claims_freq = fix_solar_system(business_claims_freq)
business_claims_sev = fix_solar_system(business_claims_sev)



df = business_claims_freq

issues = []

# --- station_id: format like A1, G3, etc. (letter + digit(s)) ---
mask = ~df["station_id"].astype(str).str.match(r"^[A-Za-z]\d+$", na=False)
for idx in df[mask].index:
    issues.append({"row": idx, "column": "station_id", "value": df.at[idx, "station_id"], "issue": "Does not match expected format (e.g. A1, G3)"})

# --- solar_system: must be one of 3 values ---
valid_solar = {"Helionis Cluster", "Epsilon", "Zeta"}
mask = ~df["solar_system"].isin(valid_solar)
for idx in df[mask].index:
    issues.append({"row": idx, "column": "solar_system", "value": df.at[idx, "solar_system"], "issue": f"Not in allowed set {valid_solar}"})

# --- energy_backup_score: {1, 2, 3, 4, 5} ---
mask = ~df["energy_backup_score"].isin([1, 2, 3, 4, 5])
for idx in df[mask].index:
    issues.append({"row": idx, "column": "energy_backup_score", "value": df.at[idx, "energy_backup_score"], "issue": "Must be an integer in {1, 2, 3, 4, 5}"})

# --- supply_chain_index: 0 – 1 ---
mask = (df["supply_chain_index"] < 0) | (df["supply_chain_index"] > 1) | df["supply_chain_index"].isna()
for idx in df[mask].index:
    issues.append({"row": idx, "column": "supply_chain_index", "value": df.at[idx, "supply_chain_index"], "issue": "Must be between 0 and 1"})

# --- avg_crew_exp: 1 – 30 ---
mask = (df["avg_crew_exp"] < 1) | (df["avg_crew_exp"] > 30) | df["avg_crew_exp"].isna()
for idx in df[mask].index:
    issues.append({"row": idx, "column": "avg_crew_exp", "value": df.at[idx, "avg_crew_exp"], "issue": "Must be between 1 and 30"})

# --- maintenance_freq: 0 – 6 ---
mask = (df["maintenance_freq"] < 0) | (df["maintenance_freq"] > 6) | df["maintenance_freq"].isna()
for idx in df[mask].index:
    issues.append({"row": idx, "column": "maintenance_freq", "value": df.at[idx, "maintenance_freq"], "issue": "Must be between 0 and 6"})

# --- safety_compliance: {1, 2, 3, 4, 5} ---
mask = ~df["safety_compliance"].isin([1, 2, 3, 4, 5])
for idx in df[mask].index:
    issues.append({"row": idx, "column": "safety_compliance", "value": df.at[idx, "safety_compliance"], "issue": "Must be an integer in {1, 2, 3, 4, 5}"})

# --- exposure: 0 – 1 ---
mask = (df["exposure"] < 0) | (df["exposure"] > 1) | df["exposure"].isna()
for idx in df[mask].index:
    issues.append({"row": idx, "column": "exposure", "value": df.at[idx, "exposure"], "issue": "Must be between 0 and 1"})

# --- claim_count: {0, 1, 2, 3, 4} ---
mask = ~df["claim_count"].isin([0, 1, 2, 3, 4])
for idx in df[mask].index:
    issues.append({"row": idx, "column": "claim_count", "value": df.at[idx, "claim_count"], "issue": "Must be an integer in {0, 1, 2, 3, 4}"})

# --- Display results ---
if issues:
    issues_df = pd.DataFrame(issues).sort_values(["row", "column"]).reset_index(drop=True)
    print(f"\n⚠️  {len(issues_df)} issue(s) found:\n")
    print(issues_df.to_string(index=False))
else:
    print("✅ No issues found — all columns meet specifications.")

"""ADDRESSING ISSUES IN business_claims_freq
    1. TAKE ABSOLUTE value of exposure
    2. send solar_system to IDCleaner.broken_id_fix
    3. if issue, set crew experience to lowest(1)
    4. if maintenance freq is issue, set to lowest (0)
    5. take absolute value of supply chain index
    6. if issue, set safety compliance to lowest (1)
    7. take absolute value of energy_backup_score
    8. send station_id to IDCleaner.broken_id_fix
"""