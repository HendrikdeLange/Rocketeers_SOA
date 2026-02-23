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
"""
cargo_claims_freq = messy_datasets["cargo_claims_freq"]
cargo_claims_sev = messy_datasets["cargo_claims_sev"]

print(cargo_claims_freq.columns)
print(cargo_claims_sev.columns)