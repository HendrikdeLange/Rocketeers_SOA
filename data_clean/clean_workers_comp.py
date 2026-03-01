"""
Workers Comp Claims Data Pipeline
Processes frequency (freq) and severity (sev) datasets through cleaning,
imputation, validation, merging, and export.
"""

import re
import pandas as pd
import numpy as np

# Frequency dataset column list
FREQ_COLS = [
    'policy_id', 'worker_id', 'solar_system', 'station_id', 'occupation', 
    'employment_type', 'experience_yrs', 'accident_history_flag', 
    'psych_stress_index', 'hours_per_week', 'supervision_level', 
    'gravity_level', 'safety_training_index', 'protective_gear_quality', 
    'base_salary', 'exposure', 'claim_count'
]

# Severity dataset column list
SEV_COLS = [
    'claim_id', 'claim_seq', 'policy_id', 'worker_id', 'solar_system', 
    'station_id', 'occupation', 'employment_type', 'experience_yrs', 
    'accident_history_flag', 'psych_stress_index', 'hours_per_week', 
    'supervision_level', 'gravity_level', 'safety_training_index', 
    'protective_gear_quality', 'base_salary', 'exposure', 'injury_type', 
    'injury_cause', 'claim_length', 'claim_amount'
]
# ──────────────────────────────────────────────
# 1. LOAD DATA
# ──────────────────────────────────────────────
def load_data(freq_path: str, sev_path: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load freq and sev datasets from South African (semicolon-delimited) CSV files."""
    freq = pd.read_csv(freq_path, sep=";", names=FREQ_COLS, header=0, dtype=str)
    sev  = pd.read_csv(sev_path,  sep=";", names=SEV_COLS,  header=0, dtype=str)

    # Clean Freq
    freq_numeric_cols = ['experience_yrs', 'accident_history_flag', 
                         'psych_stress_index', 'hours_per_week', 'supervision_level', 
                         'gravity_level', 'safety_training_index', 'protective_gear_quality', 
                         'base_salary', 'exposure', 'claim_count'] 

    for col in freq_numeric_cols:
        # Strip whitespace, replace comma, then convert
        freq[col] = freq[col].str.strip().str.replace(',', '.', regex=False)
        freq[col] = pd.to_numeric(freq[col], errors='coerce')

    # Clean Sev
    sev_numeric_cols = ['experience_yrs', 'accident_history_flag', 'psych_stress_index', 
                        'hours_per_week', 'supervision_level', 'gravity_level', 
                        'safety_training_index', 'protective_gear_quality', 'base_salary', 
                        'exposure', 'claim_length', 'claim_amount'] 

    for col in sev_numeric_cols:
        # FIXED: Ensure you are referencing 'sev' here, not 'freq'
        sev[col] = sev[col].str.strip().str.replace(',', '.', regex=False)
        sev[col] = pd.to_numeric(sev[col], errors='coerce')

    print(f"Total claim_amount: {sev['claim_amount'].sum():,.2f}")
    print(sev.head(10))
    return freq, sev
# ──────────────────────────────────────────────
# 2. STRING CLEANING – strip spaces & cut suffix
# ──────────────────────────────────────────────

_SUFFIX_RE = re.compile(r'_[A-Za-z]{3}\d{4}$')

def _clean_str_series(s: pd.Series) -> pd.Series:
    s = s.str.strip()
    mask = s.str.contains(_SUFFIX_RE, na=False)
    s[mask] = s[mask].str.replace(_SUFFIX_RE, '', regex=True)
    return s

def clean_string_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2: strip + remove trailing _???#### from all non-numeric columns."""
    # include=['object', 'str'] avoids Pandas 4 deprecation warning
    str_cols = df.select_dtypes(include=['object', 'str']).columns
    df[str_cols] = df[str_cols].apply(_clean_str_series)
    return df


# ──────────────────────────────────────────────
# 3. FILL NaN policy_id in freq (e.g. WC-ZET-01021)
# ──────────────────────────────────────────────

_POL_RE = re.compile(r'^([A-Z]{2}-[A-Z]{3}-)(\d+)$')

def _increment_policy_id(pid: str) -> str:
    m = _POL_RE.match(pid)
    if not m:
        raise ValueError(f"Unexpected policy_id format: {pid}")
    prefix, num_str = m.group(1), m.group(2)
    return f"{prefix}{int(num_str) + 1:0{len(num_str)}d}"

def fill_freq_policy_id(freq: pd.DataFrame) -> pd.DataFrame:
    """Step 3: propagate-and-increment policy_id for NaN rows in freq."""
    pid = freq['policy_id'].copy()
    for i in pid[pid.isna()].index:
        prev = pid[:i].dropna()
        if prev.empty:
            raise ValueError("No prior policy_id found before first NaN row.")
        pid.at[i] = _increment_policy_id(prev.iloc[-1])
    freq['policy_id'] = pid
    return freq


# ──────────────────────────────────────────────
# 4. SET worker_id in freq (W-00001 … W-#####)
# ──────────────────────────────────────────────

def assign_freq_worker_id(freq: pd.DataFrame) -> pd.DataFrame:
    """Step 4: overwrite worker_id with sequential W-##### identifiers."""
    freq['worker_id'] = [f"W-{i:05d}" for i in range(1, len(freq) + 1)]
    return freq


# ──────────────────────────────────────────────
# 5. DROP COLUMNS
# ──────────────────────────────────────────────

def drop_columns(freq: pd.DataFrame, sev: pd.DataFrame
                 ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Step 5: drop claim_count from freq; claim_id & claim_seq from sev."""
    freq = freq.drop(columns=['claim_count'], errors='ignore')
    sev  = sev.drop(columns=['claim_id', 'claim_seq'], errors='ignore')
    return freq, sev


# ──────────────────────────────────────────────
# 6. ABSOLUTE VALUES for numeric columns
# ──────────────────────────────────────────────

def _fix_comma_decimals(s: pd.Series) -> pd.Series:
    """
    Replace SA-format comma decimal separator with dot.
    Since the file delimiter is ";", any comma in a numeric column is a decimal
    separator — safe to replace unconditionally with no regex.
    e.g. "0,943" -> "0.943"
    """
    if s.dtype == object:
        return s.str.strip().str.replace(",", ".", regex=False)
    return s



def _cast_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce all columns that look numeric to float."""
    for col in df.columns:
        fixed = _fix_comma_decimals(df[col]) if df[col].dtype == object else df[col]
        converted = pd.to_numeric(fixed, errors='coerce')
        if converted.notna().any():
            df[col] = converted
    return df

def abs_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Step 6: take absolute value of all numeric entries."""
    df = _cast_numeric(df)
    num_cols = df.select_dtypes(include='number').columns
    df[num_cols] = df[num_cols].abs()
    return df


# ──────────────────────────────────────────────
# 7. IMPUTE sev.policy_id from freq via worker_id
# ──────────────────────────────────────────────

def impute_sev_policy_id(sev: pd.DataFrame, freq: pd.DataFrame) -> pd.DataFrame:
    """Step 7: fill NaN policy_id in sev using freq matched on worker_id."""
    freq_map = (freq.dropna(subset=['worker_id', 'policy_id'])
                    .drop_duplicates('worker_id')
                    .set_index('worker_id')['policy_id'])
    mask = sev['policy_id'].isna()
    sev.loc[mask, 'policy_id'] = sev.loc[mask, 'worker_id'].map(freq_map)
    still_nan = sev.loc[sev['policy_id'].isna(), 'worker_id'].tolist()
    if still_nan:
        print("sev policy_id still NaN – fix by hand:", still_nan)
    return sev


# ──────────────────────────────────────────────
# 8. IMPUTE freq.worker_id from sev via policy_id
# ──────────────────────────────────────────────

def impute_freq_worker_id(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    """Step 8: fill NaN worker_id in freq using sev matched on policy_id."""
    sev_map = (sev.dropna(subset=['policy_id', 'worker_id'])
                  .drop_duplicates('policy_id')
                  .set_index('policy_id')['worker_id'])
    mask = freq['worker_id'].isna()
    freq.loc[mask, 'worker_id'] = freq.loc[mask, 'policy_id'].map(sev_map)
    still_nan = freq.loc[freq['worker_id'].isna(), 'policy_id'].tolist()
    if still_nan:
        print("freq worker_id still NaN – fix by hand:", still_nan)
    return freq


# ──────────────────────────────────────────────
# 9. IMPUTE sev.worker_id from freq via policy_id
# ──────────────────────────────────────────────

def impute_sev_worker_id(sev: pd.DataFrame, freq: pd.DataFrame) -> pd.DataFrame:
    """Step 9: fill NaN worker_id in sev using freq matched on policy_id."""
    freq_map = (freq.dropna(subset=['policy_id', 'worker_id'])
                    .drop_duplicates('policy_id')
                    .set_index('policy_id')['worker_id'])
    mask = sev['worker_id'].isna()
    sev.loc[mask, 'worker_id'] = sev.loc[mask, 'policy_id'].map(freq_map)
    still_nan = sev.loc[sev['worker_id'].isna(), 'policy_id'].tolist()
    if still_nan:
        print("sev worker_id still NaN – fix by hand:", still_nan)
    return sev


# ──────────────────────────────────────────────
# 10. CROSS-IMPUTE shared columns by worker_id
# ──────────────────────────────────────────────

_SHARED_COLS = [
    'solar_system', 'station_id', 'occupation', 'employment_type',
    'experience_yrs', 'accident_history_flag', 'psych_stress_index',
    'hours_per_week', 'supervision_level', 'gravity_level',
    'safety_training_index', 'protective_gear_quality', 'base_salary',
    'exposure',
]

def cross_impute_by_worker_id(sev: pd.DataFrame, freq: pd.DataFrame
                              ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Step 10: for each shared column, fill NaN from the other df by worker_id."""
    def _build_map(df: pd.DataFrame, col: str) -> pd.Series:
        return (df.dropna(subset=['worker_id', col])
                  .drop_duplicates('worker_id')
                  .set_index('worker_id')[col])

    shared = [c for c in _SHARED_COLS if c in sev.columns and c in freq.columns]
    for col in shared:
        sev_map  = _build_map(sev,  col)
        freq_map = _build_map(freq, col)

        mask_s = sev['worker_id'].notna() & sev[col].isna()
        sev.loc[mask_s, col] = sev.loc[mask_s, 'worker_id'].map(freq_map)

        mask_f = freq['worker_id'].notna() & freq[col].isna()
        freq.loc[mask_f, col] = freq.loc[mask_f, 'worker_id'].map(sev_map)

    return sev, freq


# ──────────────────────────────────────────────
# 11. CROSS-VALIDATE shared columns by worker_id
# ──────────────────────────────────────────────

_CRITERIA: dict[str, tuple] = {
    'station_id':              ('not_nan',),
    'solar_system':            ('not_nan',),
    'occupation':              ('not_nan',),
    'employment_type':         ('not_nan',),
    'experience_yrs':          ('range', 0, 40),
    'accident_history_flag':   ('isin', [0, 1]),
    'psych_stress_index':      ('isin', [1, 2, 3, 4, 5]),
    'hours_per_week':          ('isin', [20, 25, 30, 40]),
    'supervision_level':       ('range', 0, 1),
    'gravity_level':           ('range', 0.75, 1.50),
    'safety_training_index':   ('isin', [1, 2, 3, 4, 5]),
    'protective_gear_quality': ('isin', [1, 2, 3, 4, 5]),
    'base_salary':             ('range', 20_000, np.inf),
    'exposure':                ('range', 0, 1),
}

def _meets(series: pd.Series, rule: tuple) -> pd.Series:
    """Return boolean mask: True where value passes the rule."""
    kind = rule[0]
    if kind == 'not_nan':
        return series.notna() & (series.astype(str).str.strip() != '')
    if kind == 'range':
        lo, hi = rule[1], rule[2]
        num = pd.to_numeric(_fix_comma_decimals(series), errors='coerce')
        return num.notna() & (num >= lo) & (num <= hi)
    if kind == 'isin':
        num = pd.to_numeric(_fix_comma_decimals(series), errors='coerce')
        return num.isin(rule[1])
    return pd.Series(False, index=series.index)

def cross_validate_by_worker_id(sev: pd.DataFrame, freq: pd.DataFrame
                                ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Step 11: per worker_id, if one df has a valid value and the other doesn't,
    overwrite the invalid one. Uses worker_id join to avoid index misalignment.
    """
    shared = [c for c in _CRITERIA if c in sev.columns and c in freq.columns]

    for col in shared:
        rule = _CRITERIA[col]

        # Build worker_id → valid_value maps from each df
        sev_valid  = sev.loc[_meets(sev[col], rule), ['worker_id', col]]\
                        .dropna(subset=['worker_id'])\
                        .drop_duplicates('worker_id')\
                        .set_index('worker_id')[col]

        freq_valid = freq.loc[_meets(freq[col], rule), ['worker_id', col]]\
                         .dropna(subset=['worker_id'])\
                         .drop_duplicates('worker_id')\
                         .set_index('worker_id')[col]

        # sev value invalid → fill from freq where freq has valid value
        sev_bad_mask = (~_meets(sev[col], rule)) & sev['worker_id'].notna()
        if sev_bad_mask.any():
            sev.loc[sev_bad_mask, col] = sev.loc[sev_bad_mask, 'worker_id'].map(freq_valid)

        # freq value invalid → fill from sev where sev has valid value
        freq_bad_mask = (~_meets(freq[col], rule)) & freq['worker_id'].notna()
        if freq_bad_mask.any():
            freq.loc[freq_bad_mask, col] = freq.loc[freq_bad_mask, 'worker_id'].map(sev_valid)

    return sev, freq


# ──────────────────────────────────────────────
# 12 & 13. FALLBACK IMPUTATION (freq & sev)
# ──────────────────────────────────────────────

_FREQ_RULES: dict[str, tuple] = {
    'station_id':              ('not_nan',              'mode'),
    'solar_system':            ('not_nan',              'mode'),
    'occupation':              ('not_nan',              'mode'),
    'employment_type':         ('not_nan',              'mode'),
    'experience_yrs':          ('range', 0, 40,         'median'),
    'accident_history_flag':   ('isin', [0, 1],         'median'),
    'psych_stress_index':      ('isin', [1,2,3,4,5],    'median'),
    'hours_per_week':          ('isin', [20,25,30,40],  30),
    'supervision_level':       ('range', 0, 1,          'median'),
    'gravity_level':           ('range', 0.75, 1.50,    'median'),
    'safety_training_index':   ('isin', [1,2,3,4,5],    'median'),
    'protective_gear_quality': ('isin', [1,2,3,4,5],    'median'),
    'base_salary':             ('range', 20_000, np.inf,'mean'),
    'exposure':                ('range', 0, 1,          'median'),
}

_SEV_RULES: dict[str, tuple] = {
    **_FREQ_RULES,
    'accident_history_flag':   ('isin', [0, 1],         'mode'),
    'injury_type':             ('not_nan',              'mode'),
    'injury_cause':            ('not_nan',              'mode'),
    'claim_length':            ('range', 3, 1000,       'median'),
}

# Hard-coded last-resort fallbacks if no valid values exist in column
_LAST_RESORT: dict[str, object] = {
    'experience_yrs': 5, 'accident_history_flag': 0, 'psych_stress_index': 3,
    'hours_per_week': 30, 'supervision_level': 0.5, 'gravity_level': 1.0,
    'safety_training_index': 3, 'protective_gear_quality': 3,
    'base_salary': 30_000, 'exposure': 0.5,
}

def _parse_rule(rule_tuple: tuple) -> tuple[tuple, str | int | float]:
    """Split a combined rule tuple into (criteria_tuple, fill_strategy)."""
    *crit, fill = rule_tuple
    return tuple(crit), fill

def _compute_fill(series: pd.Series, col: str, crit: tuple,
                  strategy: str | int | float) -> object:
    num_series = (pd.to_numeric(_fix_comma_decimals(series), errors='coerce')
                  if crit[0] in ('range', 'isin') else series)
    valid = num_series[_meets(num_series, crit)]

    if isinstance(strategy, (int, float)):
        return strategy
    if strategy == 'mode':
        return series.mode().iloc[0] if not series.mode().empty else np.nan
    if strategy == 'median':
        val = valid.median() if not valid.empty else np.nan
    elif strategy == 'mean':
        val = valid.mean() if not valid.empty else np.nan
    else:
        val = np.nan

    # If computed stat is still NaN, use hard-coded last resort
    if pd.isna(val):
        val = _LAST_RESORT.get(col, np.nan)
        if not pd.isna(val):
            print(f"  [fallback] '{col}' had no valid values – using last-resort fill: {val}")
    return val

def apply_fallback_imputation(df: pd.DataFrame,
                              rules: dict[str, tuple]) -> pd.DataFrame:
    """Steps 12/13: for each column, replace invalid/NaN values with fill stat."""
    for col, rule_tuple in rules.items():
        if col not in df.columns:
            continue
        crit, fill_strategy = _parse_rule(rule_tuple)

        if crit[0] in ('range', 'isin'):
            df[col] = pd.to_numeric(_fix_comma_decimals(df[col]), errors='coerce')

        bad_mask = ~_meets(df[col], crit)
        if bad_mask.any():
            fill_val = _compute_fill(df[col], col, crit, fill_strategy)
            df.loc[bad_mask, col] = fill_val
    return df


# ──────────────────────────────────────────────
# 14. DROP sev rows where claim_amount is NaN or 0
# ──────────────────────────────────────────────

def drop_invalid_claim_amounts(sev: pd.DataFrame) -> pd.DataFrame:
    """Step 14: remove rows where claim_amount is NaN or 0."""
    sev['claim_amount'] = pd.to_numeric(_fix_comma_decimals(sev['claim_amount']), errors='coerce')
    return sev[sev['claim_amount'].notna() & (sev['claim_amount'] != 0)].copy()


# ──────────────────────────────────────────────
# 15 & 16. MERGE & NaN CHECK
# ──────────────────────────────────────────────
def merge_datasets(freq: pd.DataFrame, sev: pd.DataFrame) -> pd.DataFrame:
    """
    Merge severity data onto frequency data by worker_id.
    Brings injury_type, injury_cause, claim_length, claim_amount from sev to freq.
    Fills NaN values with 0 for these columns after merge.
    """
    # DIAGNOSTIC: Check initial state
    print("\n" + "="*50)
    print("MERGE DIAGNOSTICS")
    print("="*50)
    
    # 1. Check worker_id relationships
    freq_workers = set(freq['worker_id'].unique())
    sev_workers = set(sev['worker_id'].unique())
    
    print(f"\n1. Worker ID Statistics:")
    print(f"   - Unique workers in freq: {len(freq_workers)}")
    print(f"   - Unique workers in sev: {len(sev_workers)}")
    print(f"   - Workers in both: {len(freq_workers & sev_workers)}")
    print(f"   - Workers only in freq: {len(freq_workers - sev_workers)}")
    print(f"   - Workers only in sev: {len(sev_workers - freq_workers)}")
    
    # 2. Check claim amounts before merge
    print(f"\n2. SEV Claim Amount Statistics (before merge):")
    print(f"   - Total rows in sev: {len(sev)}")
    print(f"   - Total claim_amount: {sev['claim_amount'].sum():,.2f}")
    print(f"   - Mean claim_amount: {sev['claim_amount'].mean():,.2f}")
    print(f"   - Median claim_amount: {sev['claim_amount'].median():,.2f}")
    print(f"   - Min claim_amount: {sev['claim_amount'].min():,.2f}")
    print(f"   - Max claim_amount: {sev['claim_amount'].max():,.2f}")
    
    # 3. Check for multiple claims per worker
    claims_per_worker = sev.groupby('worker_id').size()
    multi_claim_workers = claims_per_worker[claims_per_worker > 1]
    print(f"\n3. Multiple Claims Analysis:")
    print(f"   - Workers with multiple claims: {len(multi_claim_workers)}")
    if len(multi_claim_workers) > 0:
        print(f"   - Distribution of claims per worker:")
        print(claims_per_worker.value_counts().sort_index().to_string())
        
        # Show example of worker with multiple claims
        example_worker = multi_claim_workers.index[0]
        print(f"\n   Example - Worker {example_worker}:")
        example_claims = sev[sev['worker_id'] == example_worker][['claim_amount']]
        print(example_claims.to_string())
    
    # Define columns to bring from sev
    cols_to_bring = ['worker_id', 'injury_type', 'injury_cause', 'claim_length', 'claim_amount']
    
    # Filter only existing columns from sev
    existing_cols = [col for col in cols_to_bring if col in sev.columns]
    sev_sub = sev[existing_cols].copy()
    
    # 4. Check freq before merge
    print(f"\n4. FREQ Statistics (before merge):")
    print(f"   - Total rows in freq: {len(freq)}")
    
    # Merge sev onto freq by worker_id (left join keeps all freq rows)
    merged = freq.merge(sev_sub, on='worker_id', how='left')
    
    # 5. Check merge result
    print(f"\n5. MERGE Result:")
    print(f"   - Rows after merge: {len(merged)}")
    print(f"   - Rows added: {len(merged) - len(freq)}")
    
    # 6. Check for duplication
    if len(merged) > len(freq):
        print(f"   ⚠️  WARNING: Merge created {len(merged) - len(freq)} additional rows!")
        print(f"      This indicates multiple sev rows per worker_id")
        
        # Show which workers are causing duplication
        worker_counts = merged.groupby('worker_id').size()
        duplicated_workers = worker_counts[worker_counts > 1]
        print(f"\n      Workers with multiple rows after merge: {len(duplicated_workers)}")
        if len(duplicated_workers) > 5:
            print(duplicated_workers.head(10).to_string())
    
    # 7. Check claim amounts after merge (before fillna)
    print(f"\n6. Claim Amount After Merge (before fillna):")
    print(f"   - Total claim_amount: {merged['claim_amount'].sum():,.2f}")
    print(f"   - Mean claim_amount: {merged['claim_amount'].mean():,.2f}")
    print(f"   - Null count: {merged['claim_amount'].isna().sum()}")
    
    # Fill NaN values with 0 for the severity columns
    severity_cols = ['injury_type', 'injury_cause', 'claim_length', 'claim_amount']
    for col in severity_cols:
        if col in merged.columns:
            merged[col] = merged[col].fillna(0)
    
    # 8. Final check
    print(f"\n7. FINAL Claim Amount:")
    print(f"   - Total claim_amount: {merged['claim_amount'].sum():,.2f}")
    print(f"   - Ratio to original SEV total: {merged['claim_amount'].sum() / sev['claim_amount'].sum():.2f}x")
    print("="*50 + "\n")
    
    return merged
def check_nans(df: pd.DataFrame, label: str) -> None:
    """Step 16: report NaN counts per column."""
    nan_counts = df.isna().sum()
    nan_counts = nan_counts[nan_counts > 0]
    if nan_counts.empty:
        print(f"[{label}] No NaN values found.")
    else:
        print(f"[{label}] NaN summary:\n{nan_counts.to_string()}\n")


# ──────────────────────────────────────────────
# 17. SAVE
# ──────────────────────────────────────────────

def save_output(df: pd.DataFrame, path: str) -> None:
    """Step 17: save to semicolon-delimited CSV."""
    df.to_csv(path, index=False, sep=";", decimal=",")
    print(f"Saved → {path}")


# ──────────────────────────────────────────────
# MAIN PIPELINE
# ──────────────────────────────────────────────

def run_pipeline(freq_path: str = r"messy_data\workers_claims_freq.csv",
                 sev_path:  str = r"messy_data\workers_claims_sev.csv",
                 out_path:  str = "business_claims_merged.csv") -> pd.DataFrame:

    freq, sev = load_data(freq_path, sev_path)
    freq = clean_string_columns(freq)
    sev  = clean_string_columns(sev)
    freq = fill_freq_policy_id(freq)
    freq = assign_freq_worker_id(freq)
    freq, sev = drop_columns(freq, sev)
    freq = abs_numeric(freq)
    sev  = abs_numeric(sev)
    sev  = impute_sev_policy_id(sev, freq)
    freq = impute_freq_worker_id(freq, sev)
    sev  = impute_sev_worker_id(sev, freq)
    sev, freq = cross_impute_by_worker_id(sev, freq)
    sev, freq = cross_validate_by_worker_id(sev, freq)
    sev  = drop_invalid_claim_amounts(sev)
    freq = apply_fallback_imputation(freq, _FREQ_RULES)
    sev  = apply_fallback_imputation(sev,  _SEV_RULES)
    business_claims_merged = merge_datasets(freq, sev)
    check_nans(business_claims_merged, "business_claims_merged")
    save_output(business_claims_merged, out_path)
    return business_claims_merged


if __name__ == "__main__":
    business_claims_merged = run_pipeline()