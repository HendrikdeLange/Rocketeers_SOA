from data_store import messy_datasets
import pandas as pd
pd.set_option("display.max_columns", None)
import re
from missing_policy_fix import missing_id_fix, validate_ids
"""
DATASET DOCUMENTATION: Business Interruption Claims
==================================================
Variable Name       | Description                          | Type      | Units       | Value Range or Levels
-----------------------------------------------------------------------------------------------------------
policy_id           | Policy identifier                   | character | --          | e.g., BI-123456, ...
station_id          | Mining platform identifier          | category  | --          | e.g., A1, G3, ...
solar_system        | Solar system identifier             | category  | --          | {Helionis Cluster, Epsilon, Zeta}
production_load     | Avg utilization rate of capacity    | numeric   | Ratio       | 0 – 1
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

business_claims_freq["policy_id"] = missing_id_fix(business_claims_freq["policy_id"], 9)
summary = validate_ids(business_claims_freq["policy_id"], 9)
print(summary)

result = validate_ids(business_claims_freq["policy_id"], 9)

if result != "No issues found":
    indices = [i for i, _ in result]
    non_zero = business_claims_freq.loc[indices, "claim_count"] != 0
    print(business_claims_freq.loc[indices][non_zero.values])
