import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "messy_data"
CACHE_DIR = PROJECT_ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)

def load_or_cache(filename, sheet_name):
    cache_file = CACHE_DIR / f"{Path(filename).stem}_{sheet_name}.parquet"
    if cache_file.exists():
        return pd.read_parquet(cache_file)
    print(f"  Caching {filename} [{sheet_name}]...")
    df = pd.read_excel(DATA_DIR / filename, sheet_name=sheet_name)
    df.to_parquet(cache_file, index=False)
    return df

sources = {
    "business": "srcsc-2026-claims-business-interruption.xlsx",
    "cargo":    "srcsc-2026-claims-cargo.xlsx",
    "equipment": "srcsc-2026-claims-equipment-failure.xlsx",
    "worker":   "srcsc-2026-claims-workers-comp.xlsx",
}

messy_datasets = {
    f"{name}_claims_{sheet}": load_or_cache(filename, sheet)
    for name, filename in sources.items()
    for sheet in ("freq", "sev")
}

print("Messy data successfully loaded!")
