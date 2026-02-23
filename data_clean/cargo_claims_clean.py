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
from impute_cargo_policy_ids import impute_policy_ids
from cargo_policy_resolver_sev import PolicyResolver
"""======================================================================================
# DATASET SCHEMA: Planetary Cargo Insurance Claims
# ======================================================================================
# Variable Name      | Description                                     | Type      | Units                          | Value Range or Levels
# -------------------|-------------------------------------------------|-----------|--------------------------------|--------------------------------------
# policy_id          | Policy identifier                               | character | --                             | E.g., CL-963974, …
# shipment_id        | Shipment identifier                             | character | --                             | E.g., S-094788, …
# origin             | Planetary/satellite hub where cargo departs     | category  | --                             | {Earth, Mars, Moon, planet A, ...}
# destination        | Planetary/satellite hub for cargo delivery      | category  | --                             | {Earth, Mars, Moon, planet A, ...}
# cargo_type         | Type of goods shipped                           | category  | --                             | {platinum, gold, ...}
# cargo_value        | Declared insured value of shipment              | numeric   | Millions of solar system curr. | ~ 50K – 680,000K
# weight             | Weight of shipment                              | numeric   | Kg (SI)                        | 1.5K – 250K
# route_risk         | Risk classification of transport route          | category  | --                             | {1, 2, 3, 4, 5}
# distance           | Distance of transit route                       | numeric   | Astronomical Units             | 1 – 100
# transit_duration   | Expected travel time                            | numeric   | Earth months                   | 1 – 60
# pilot_experience   | Average flight experience of assigned pilots    | numeric   | Earth years                    | 1 – 30
# vessel_age         | Average age of vessel                           | numeric   | Earth years                    | 1 – 50
# container_type     | Container used                                  | category  | --                             | {high cube, dry van, flat rack, ...}
# solar_radiation    | Hazard index                                    | numeric   | Index                          | 0 – 1
# debris_density     | Frequency of debris or asteroids in route       | numeric   | Index                          | 0 – 1
# exposure           | Period of exposure in Earth years               | numeric   | Ratio                          | 0 – 1
# claim_count        | Number of claims during the exposure period     | numeric   | Number                         | 0 – 5
# claim_amount1      | Claim amount per claim                          | numeric   | [currency]                     | ~ 31K – 678,000K
# ======================================================================================

cargo_claims_freq.columns = ['policy_id', 'shipment_id', 'cargo_type', 'cargo_value', 'weight',
       'route_risk', 'distance', 'transit_duration', 'pilot_experience',
       'vessel_age', 'container_type', 'solar_radiation', 'debris_density',
       'exposure', 'claim_count']

cargo_claims_sev.columns = ['claim_id', 'claim_seq', 'policy_id', 'shipment_id', 'cargo_type',
       'cargo_value', 'weight', 'route_risk', 'distance', 'transit_duration',
       'pilot_experience', 'vessel_age', 'container_type', 'solar_radiation',
       'debris_density', 'exposure', 'claim_amount']

       common_columns = {'container_type', 'vessel_age', 'cargo_value', 'route_risk', 'weight', 
       'debris_density', 'transit_duration', 'shipment_id', 'cargo_type', 'policy_id', 'pilot_experience', 
       'exposure', 'solar_radiation', 'distance'}
"""
cargo_claims_freq = messy_datasets["cargo_claims_freq"]
cargo_claims_sev = messy_datasets["cargo_claims_sev"]

#CL-032806 9	S-981581 8

#Fixing policy_id and shipment_id and claim_id
cargo_claims_freq["policy_id"] = IDCleaner(cargo_claims_freq["policy_id"], 9).broken_id_fix().get()
#print(f"{IDCleaner(cargo_claims_freq['policy_id'], 9).validate_ids()} in the cargo_claims_freq policy_id column!")
cargo_claims_sev["policy_id"] = IDCleaner(cargo_claims_sev["policy_id"], 9).broken_id_fix().get()
#print(f"{IDCleaner(cargo_claims_sev['policy_id'], 9).validate_ids()} in the cargo_claims_sev policy_id column!")

cargo_claims_freq["shipment_id"] = IDCleaner(cargo_claims_freq["shipment_id"], 8).broken_id_fix().get()
#print(f"{IDCleaner(cargo_claims_freq['shipment_id'], 8).validate_ids()} in the cargo_claims_freq shipment_id column!")
cargo_claims_sev["shipment_id"] = IDCleaner(cargo_claims_sev["shipment_id"], 8).broken_id_fix().get()
#print(f"{IDCleaner(cargo_claims_sev['shipment_id'], 8).validate_ids()} in the cargo_claims_sev shipment_id column!") #there are still some NaNs

#CAR-C-0000001

cargo_claims_sev["claim_id"] = IDCleaner(cargo_claims_sev["claim_id"], 13).broken_id_fix().missing_id_fix().get()
print(f"{IDCleaner(cargo_claims_sev['claim_id'], 13).validate_ids()} in the cargo_claims_sev claim_id column!")


#########################
#going to drop missing policy_ids with claim counts of 0
mask = cargo_claims_freq['policy_id'].isna() & (cargo_claims_freq['claim_count'] == 0)
cargo_claims_freq = cargo_claims_freq[~mask]

#impute policy_ids
cargo_claims_freq, cargo_claims_sev = impute_policy_ids(
    cargo_claims_freq,
    cargo_claims_sev,
    match_keys=["exposure", "shipment_id"],  # tweak to your actual columns
)
cargo_claims_freq, cargo_claims_sev = impute_policy_ids(
    cargo_claims_freq,
    cargo_claims_sev,
    match_keys=["shipment_id", "container_type"],  # tweak to your actual columns
)
cargo_claims_freq = cargo_claims_freq.dropna(subset=['policy_id'])

#OKAY policy_id is fixed

#now to fix claim_count and claim_seq
cargo_claims_sev = reassign_claim_seq(cargo_claims_sev) # fixes the claim_seq column in cargo_claims_sev
cargo_claims_freq = update_claim_count(cargo_claims_freq, cargo_claims_sev) # fixes the claim_count column in cargo_claims_freq

#now to fix_sev duplicates
resolver = PolicyResolver(verbose=True)
cargo_claims_sev = resolver.resolve(cargo_claims_sev)














"""
The cargo_claims_sev df has columns ['claim_id', 'claim_seq', 'policy_id', 'shipment_id', 'cargo_type',
       'cargo_value', 'weight', 'route_risk', 'distance', 'transit_duration',
       'pilot_experience', 'vessel_age', 'container_type', 'solar_radiation',
       'debris_density', 'exposure', 'claim_amount']

 correct_cargo_types = ["lithium", "cobalt", "supplies", "rare earths", "titanium", "platinum", "gold"] 
 correct_container_types = ["QuantumCrate Module", "DockArc Freight Case", "DeepSpace Haulbox", "LongHaul Vault Canister",
                            "HardSeal Transit Crate"]
"""



