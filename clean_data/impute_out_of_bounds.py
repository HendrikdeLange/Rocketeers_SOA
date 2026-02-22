def impute_out_of_bounds(df, col_specs):
    """
    col_specs: dict where each key is a column name and value is either:
        - a tuple (min, max) for continuous/range columns
        - a list [1, 2, 3, 4, 5] for discrete/set columns
    
    Any value that is NaN or outside the valid range is replaced with the median of the valid range.
    """
    df = df.copy()
    
    for col, spec in col_specs.items():
        if col not in df.columns:
            print(f"Warning: column '{col}' not found in dataframe, skipping.")
            continue
        
        if isinstance(spec, tuple):  # range (min, max)
            low, high = spec
            median_val = (low + high) / 2
            mask = df[col].isna() | (df[col] < low) | (df[col] > high)
        
        elif isinstance(spec, list):  # discrete set
            median_val = sorted(spec)[len(spec) // 2]
            mask = df[col].isna() | (~df[col].isin(spec))
        
        df.loc[mask, col] = median_val
    
    return df
