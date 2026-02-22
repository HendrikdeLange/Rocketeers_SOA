import re

def fix_solar_system(df, col="solar_system"):
    valid = {"Helionis Cluster", "Epsilon", "Zeta"}
    df[col] = df[col].str.replace(r"_\?\?\?\d+$", "", regex=True)
    # nullify anything that still doesn't match after cleaning
    df.loc[~df[col].isin(valid), col] = None
    return df