import pandas as pd
import numpy as np
import re

"""
    Ek het agter gekom dat die missing policy ids in volgorde is, so as iets missing is, vat die vorige entry en +1 
"""

def missing_id_fix(x_id, entry_length):
    column = x_id.copy()
    
    for i in range(len(column)):
        if pd.isna(column[i]) or column[i] == "":
            if i > 0:
                prev_value = str(column[i-1])
                if len(prev_value)== entry_length:
               
                    match = re.search(r'(\d+)(?!.*\d)', prev_value)
                
                    if match:
                        num_part = match.group(1)
                        incremented_num = int(num_part) + 1
                    
                        start, end = match.span(1)
                        new_value = prev_value[:start] + str(incremented_num).zfill(len(num_part)) + prev_value[end:]
                        column[i] = new_value
                    
    return column

def validate_ids(x_id, entry_length):
    issues = []
    
    for i, value in enumerate(x_id):
        if pd.isna(value) or value == "":
            issues.append((i, "missing"))
        elif len(str(value)) != entry_length:
            issues.append((i, f"incorrect length ({len(str(value))})"))
    
    if not issues:
        return "No issues found"
    
    return issues