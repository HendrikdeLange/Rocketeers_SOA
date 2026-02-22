# pip install -r requirements.txt
from data_store import messy_datasets
import pandas as pd
import re
pd.set_option("display.max_columns", None)
from id_fix import IDCleaner
from fill_missing_policy_ids import fill_missing_policy_ids
from claim_count_fix import reassign_claim_seq, update_claim_count
from absolute_values import make_absolute
from impute_out_of_bounds import impute_out_of_bounds
from fix_solar_system import fix_solar_system
from business_data_reconciler import DatasetReconciler
from station_cluster_imputer import MissingValueImputer
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

# FIXING claim_count + claim_seq
business_claims_sev = reassign_claim_seq(business_claims_sev) # fixes the claim_seq column in business_claims_sev
business_claims_freq = update_claim_count(business_claims_freq, business_claims_sev) # fixes the claim_count column in business_claims_freq

#FIXING station_id 
business_claims_freq["station_id"] = IDCleaner(business_claims_freq["station_id"], 2).broken_id_fix().get()
print(f"{IDCleaner(business_claims_freq['station_id'], 2).validate_ids()} in the business_claims_freq station_id column!")
business_claims_sev["station_id"] = IDCleaner(business_claims_sev["station_id"], 2).broken_id_fix().get()
print(f"{IDCleaner(business_claims_sev['station_id'], 2).validate_ids()} in the business_claims_sev station_id column!")

#fixing the solar_system
business_claims_freq = fix_solar_system(business_claims_freq)
business_claims_sev = fix_solar_system(business_claims_sev)

#Taking absolute values of all numeric variables
business_claims_freq = make_absolute(business_claims_freq)
business_claims_sev = make_absolute(business_claims_sev)

#Call the reconciler
reconciler = DatasetReconciler()
business_claims_freq, business_claims_sev = reconciler.reconcile(
    business_claims_freq,
    business_claims_sev#,
    #audit=True,
)


#for missing station_id and solar_systems i will randomly sample from a list
# 1. Collect your existing valid station_ids (from either dataset, or a master list)
existing_station_ids = (
    business_claims_freq["station_id"]
    .dropna()
    .unique()
    .tolist()
)

# 2. Instantiate — solar_systems defaults to the 3 from col_specs
imputer = MissingValueImputer(
    station_ids=existing_station_ids,
    random_state=42,       
)

# 3. Send each dataset separately
business_claims_freq = imputer.impute(business_claims_freq, name="freq")
business_claims_sev  = imputer.impute(business_claims_sev,  name="sev")



#Set columns which have issues to median value
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


""" DONE"""

