import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLEAN_DIR    = PROJECT_ROOT / "clean_data"

def cache_all_excel(clean_dir: Path):
    """Convert all Excel files in clean_dir to parquet in the same folder."""
    excel_files = list(clean_dir.glob("*.xlsx"))

    if not excel_files:
        print("  ⚠️  No Excel files found in clean_data/")
        return

    for excel_file in excel_files:
        parquet_file = clean_dir / f"{excel_file.stem}.parquet"

        if parquet_file.exists():
            print(f"  ✅ Already cached — skipping : {parquet_file.name}")
            continue

        print(f"  Caching {excel_file.name} → {parquet_file.name} ...")
        df = pd.read_excel(excel_file)
        df.to_parquet(parquet_file, index=False)

    print("\n  Done! All available Excel files have been cached as parquet.")


cache_all_excel(CLEAN_DIR)