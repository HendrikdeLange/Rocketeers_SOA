import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "messy-data"


business_claims_freq = pd.read_excel(DATA_DIR / "srcsc-2026-claims-business-interruption.xlsx" , sheetname=freq)
business_claims_sev = pd.read_excel(DATA_DIR / "srcsc-2026-claims-business-interruption.xlsx" , sheetname=sev)
cargo_claims_freq = pd.read_excel(DATA_DIR / "srcsc-2026-claims-cargo.xlsx", sheetname=freq)
cargo_claims_sev = pd.read_excel(DATA_DIR / "srcsc-2026-claims-cargo.xlsx" , sheetname=sev)
equipment_claims_freq = pd.read_excel(DATA_DIR / "srcsc-2026-claims-equipment-failure.xlsx", sheetname=freq)
equipment_claims_sev = pd.read_excel(DATA_DIR / "srcsc-2026-claims-equipment-failure.xlsx", sheetname=sev)
worker_claims_freq = pd.read_excel(DATA_DIR / "srcsc-2026-claims-workers-comp.xlsx", sheetname=freq)
worker_claims_sev = pd.read_excel(DATA_DIR / "srcsc-2026-claims-workers-comp.xlsx", sheetname=sev)


# Central registry
messy_datasets = {
    business_claims_freq : business_claims_freq,
    business_claims_sev : business_claims_sev,
    cargo_claims_freq : cargo_claims_freq,
    cargo_claims_sev : cargo_claims_sev,
    equipment_claims_freq : equipment_claims_freq,
    equipment_claims_sev : equipment_claims_sev,
    worker_claims_freq : worker_claims_freq,
    worker_claims_sev : worker_claims_sev
}
