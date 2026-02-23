import pandas as pd
import os
import glob

source = r"C:\Users\hendr\OneDrive\Documents\Rocketeers_SOA\clean_data\excel_files"
dest = r"C:\Users\hendr\OneDrive\Documents\Rocketeers_SOA\clean_data\csv_files"

os.makedirs(dest, exist_ok=True)

for excel_file in glob.glob(source + "\\*.xlsx"):
    df = pd.read_excel(excel_file)
    csv_name = os.path.basename(excel_file).replace('.xlsx', '.csv')
    df.to_csv(os.path.join(dest, csv_name), index=False)
    print(f"Converted: {os.path.basename(excel_file)}")

print("Done!")