from data_store import messy_datasets
import pandas as pd
pd.set_option("display.max_columns", None)
from id_fix import IDCleaner
from fill_missing_policy_ids import fill_missing_policy_ids
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
business_claims_sev["policy_id"] = IDCleaner(business_claims_sev["claim_id"], 9).broken_id_fix().get()
print(f"{IDCleaner(business_claims_sev['policy_id'], 9).validate_ids()} in the business_claims_sev policy_id column!")

"""station_id          | Mining platform identifier          | category  | --          | e.g., A1, G3, ...
solar_system        | Solar system identifier             | category  | --          | {Helionis Cluster, Epsilon, Zeta}
energy_backup_score | Adequacy of emergency power systems | category  | --          | {1, 2, 3, 4, 5}
supply_chain_index  | Proportion of inputs sourced        | numeric   | Ratio       | 0 – 1
avg_crew_exp        | Average experience of assigned staff| numeric   | Earth years | 1 – 30
maintenance_freq    | Expected maintenance cycles / year  | numeric   | Number      | 0 – 6
safety_compliance   | Compliance score                    | category  | --          | {1, 2, 3, 4, 5}
exposure            | Period of exposure in Earth years   | numeric   | Ratio       | 0 – 1
claim_count         | Number of claims during exposure    | numeric   | Number      | 0 – 4"""