import pandas as pd
import numpy as np
import re

"""
    Ek het agter gekom dat die missing policy ids in volgorde is, so as iets missing is, vat die vorige entry en +1 
    #SNY DIE LAASTE ENTRIES IN BROKEN ROWS
    BI-021624_???6689 -> BI-021624
"""
class IDCleaner:
    def __init__(self, x_id, entry_length):
        self.x_id = x_id.copy()
        self.entry_length = entry_length

    def broken_id_fix(self):
        mask = self.x_id.str.len() > self.entry_length
        self.x_id[mask] = self.x_id[mask].str[:self.entry_length]
        return self

    def missing_id_fix(self):
        column = self.x_id
        for i in range(len(column)):
            if pd.isna(column[i]) or column[i] == "":
                if i > 0:
                    prev_value = str(column[i-1])
                    if len(prev_value) == self.entry_length:
                        match = re.search(r'(\d+)(?!.*\d)', prev_value)
                        if match:
                            num_part = match.group(1)
                            incremented_num = int(num_part) + 1
                            start, end = match.span(1)
                            new_value = prev_value[:start] + str(incremented_num).zfill(len(num_part)) + prev_value[end:]
                            column[i] = new_value
        return self

    def validate_ids(self):
        issues = []
        for i, value in enumerate(self.x_id):
            if pd.isna(value) or value == "":
                issues.append((i, "missing"))
            elif len(str(value)) != self.entry_length:
                issues.append((i, f"incorrect length ({len(str(value))})"))
        return "No issues found" if not issues else issues

    def get(self):
        return self.x_id