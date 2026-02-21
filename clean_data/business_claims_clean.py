from data_store import messy_datasets
import pandas as pd
pd.set_option("display.max_columns", None)
import re

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

###FIX THE POLICY COLUMN
df = business_claims_freq
pattern = re.compile(r'^BI-\d{6}$')
invalid_format = df[~df["policy_id"].apply(lambda x: bool(pattern.match(str(x))) if pd.notna(x) else False)]
duplicates = df[df["policy_id"].duplicated(keep=False)]
print(f"Invalid format ({len(invalid_format)} rows):")
print(f"\nDuplicates ({len(duplicates)} rows):")
missing = df[df["policy_id"].isna()]
print(f"Missing policy_id ({len(missing)} rows):")

"""ISSUES WITH POLICY COLUMN IN business_claims_freq
    MISSING ENTRIES : 129
    INVALID FORMAT ("BI-098149_???4072") : 288
"""

#The business_claims_sev dataset also has a policy_id collumn
df = business_claims_sev
pattern = re.compile(r'^BI-\d{6}$')
invalid_format = df[~df["policy_id"].apply(lambda x: bool(pattern.match(str(x))) if pd.notna(x) else False)]
duplicates = df[df["policy_id"].duplicated(keep=False)]
print(f"Invalid format ({len(invalid_format)} rows):")
print(f"\nDuplicates ({len(duplicates)} rows):")
missing = df[df["policy_id"].isna()]
print(f"Missing policy_id ({len(missing)} rows):")
print(invalid_format)
"""ISSUES WITH POLICY COLUMN IN business_claims_freq
    MISSING ENTRIES : 16
    INVALID FORMAT ("BI-098149_???4072") : 28
"""

"""
    So one policy id can have multiple claim ids-> there is not supposed to be duplicate claim ids
"""
df = business_claims_sev
pattern = re.compile(r'^BI-C-\d{7}$')
invalid_format = df[~df["claim_id"].apply(lambda x: bool(pattern.match(str(x))) if pd.notna(x) else False)]
duplicates = df[df["claim_id"].duplicated(keep=False)]
print("duplicates")
print(duplicates)
print(f"Invalid format ({len(invalid_format)} rows):")
print(f"\nDuplicates ({len(duplicates)} rows):")
missing = df[df["claim_id"].isna()]
print(f"Missing claim_id ({len(missing)} rows):")
print(invalid_format)
"""ISSUES WITH POLICY COLUMN IN business_claims_freq
    DUPLICATES: 0 YES
    MISSING ENTRIES : 15
    INVALID FORMAT ("BI-C-0001601_???6222") : 33
"""
"""WHAT TO DO WITH POLICY ENTRIES OF FORM: BI-0001601_???6222
        ASSUMPTION
        BI-002322_???9503	A2	Zeta	0.48	5	0.25	2	2	5	0.61	0
        policy_id station_id solar_system  production_load  energy_backup_score  \
9502  BI-009503         A5         Zeta            0.087                  5.0

      supply_chain_index  avg_crew_exp  maintenance_freq  safety_compliance  \
9502               0.802           2.0               3.0                1.0

      exposure  claim_count
9502     0.813          0.0     

"""
print(business_claims_freq[business_claims_freq["policy_id"] == "BI-009503"])