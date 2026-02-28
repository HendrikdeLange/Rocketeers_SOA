# Equipment Failure Claims — Data Cleaning Report

**Generated:** 2026-02-28 15:57:50
**Script:** `clean_equipment_claims.py`

---

## 1. Overview

| | Frequency Dataset | Severity Dataset |
|---|---|---|
| Input file | `data_clean\test_equipment_fail\equipment_failure_claims_freq.csv` | `data_clean\test_equipment_fail\equipment_failure_claims_sev.csv` |
| Output file | `cleaned_freq.csv` | `cleaned_sev.csv` |
| Raw rows | 95,062 | 8,272 |
| Cleaned rows | 95,062 | 8,162 |
| Raw columns | 9 | 11 |
| Cleaned columns | 9 | 11 |

---

## 2. Pipeline Changes vs Previous Version

### Key corrections in this version

| # | What changed | Why |
|---|---|---|
| 1 | `policy_id` cleaning and imputation moved to Steps 3–5 (before everything else) | Downstream cross-imputation and claim_count derivation both rely on a clean policy_id key — running them first maximises coverage |
| 2 | `claim_count` now derived as `COUNT(sev rows per policy_id)` not `max(claim_seq)` | Row count is the correct definition per requirements; max(claim_seq) fails if seq has gaps, duplicates, or NaN |
| 3 | `claim_count` is re-synced after Step 11a drops claim_amount outlier rows | Keeps freq and sev consistent after the drop |

---

## 3. Issues Found & Actions Taken

### 3.1 Non-standard file format

Both CSVs use **semicolons** as delimiter and **commas** as decimal separator.
Loaded with `sep=';'` and `decimal=','`. Output uses `decimal='.'`.

---

### 3.2 policy_id imputation (Steps 3–5)

policy_id is recovered in three stages before any other cleaning occurs.

**Step 3 — Direct equipment_id match:**

| Target | Source | Filled |
| --- | --- | --- |
| freq | unambiguous equipment_id lookup | 17 |
| sev | unambiguous equipment_id lookup | 20 |

**Step 4 — Secondary key combinations:**

| Target | Key Used | Filled |
| --- | --- | --- |
| sev | equipment_id + exposure | 1 |

**Step 5 — Placeholders assigned:**

| Dataset | Column | Count | Range |
| --- | --- | --- | --- |
| freq | policy_id | 207 | MP-0001 ... MP-0207 |
| freq | equipment_id | 221 | ME-0001 ... ME-0221 |
| sev | policy_id | 1 | MP-0208 ... MP-0208 |
| sev | equipment_id | 15 | ME-0222 ... ME-0236 |

---

### 3.3 Corrupted categorical values (Step 6)

| Dataset | Column | Values Cleared |
| --- | --- | --- |
| freq | equipment_type | 0 |
| freq | solar_system | 0 |
| sev | equipment_type | 0 |
| sev | solar_system | 0 |

---

### 3.4 Cross-imputation of shared columns (Step 7)

| Target | Column | Values Filled |
| --- | --- | --- |
| freq | equipment_type | 19 |
| freq | equipment_age | 9 |
| freq | solar_system | 11 |
| freq | maintenance_int | 7 |
| freq | usage_int | 10 |
| freq | exposure | 8 |
| sev | equipment_type | 33 |
| sev | equipment_age | 10 |
| sev | solar_system | 15 |
| sev | maintenance_int | 12 |
| sev | usage_int | 8 |
| sev | exposure | 13 |

---

### 3.5 Negative values (Step 8)

| Dataset | Column | Count |
| --- | --- | --- |
| freq | equipment_age | 144 |
| freq | maintenance_int | 136 |
| freq | usage_int | 137 |
| freq | exposure | 152 |
| freq | claim_count | 12 |
| sev | equipment_age | 15 |
| sev | maintenance_int | 13 |
| sev | usage_int | 13 |
| sev | exposure | 16 |
| sev | claim_amount | 11 |

---

### 3.6 Out-of-range exposure (Step 9)

| Dataset | Values > 1 | Rescued | Set to NaN |
| --- | --- | --- | --- |
| freq | 138 | 138 | 0 |
| sev | 11 | 11 | 0 |

---

### 3.7 claim_count and claim_seq (Step 10)

`claim_count` is defined as the **count of rows in sev for that policy_id**.
Non-integer floats and negatives were nulled first, then every `claim_count`
value was derived (or verified) directly from `COUNT(sev rows per policy_id)`.

| Sub-step | Dataset | Column | Values Affected |
|---|---|---|---|
| Step 10a | freq | claim_count | 18 |
| Step 10a | sev | claim_seq | 12 |
| Step 10b | sev | claim_seq | 11 |
| Step 10c | freq | claim_count | 205 |
| Step 10d | freq | claim_count | 1077 |

---

### 3.8 Percentile capping (Step 11)

| Dataset | Column | Cap Value | Values Capped |
| --- | --- | --- | --- |
| freq | equipment_age | 21.8749 | 948 |
| freq | maintenance_int | 1786.2300 | 946 |
| freq | usage_int | 23.8000 | 941 |
| sev | equipment_age | 23.2530 | 81 |
| sev | maintenance_int | 1792.1366 | 83 |
| sev | usage_int | 23.8700 | 76 |

---

### 3.9 claim_amount — rows dropped above 99th percentile (Step 11a)

| Metric | Value |
|---|---|
| 99th percentile threshold | 296,054.9200 |
| Rows dropped | 83 |
| Rows remaining in sev | 8,162 |
| claim_count rows re-synced in freq | 94 |

**Dropped claim_ids:** `EF-C-0000275`, `EF-C-0000308`, `EF-C-0000353`, `EF-C-0001020`, `EF-C-0001081`, `EF-C-0001114`, `EF-C-0001159`, `EF-C-0001382`, `EF-C-0001401`, `EF-C-0001426`, `EF-C-0001632`, `EF-C-0001653`, `EF-C-0001744`, `EF-C-0001778`, `EF-C-0001834`, `EF-C-0001863`, `EF-C-0001980`, `EF-C-0001992`, `EF-C-0002006`, `EF-C-0002392`, `EF-C-0002407`, `EF-C-0002563`, `EF-C-0002616`, `EF-C-0002686`, `EF-C-0002824`, `EF-C-0002952`, `EF-C-0003038`, `EF-C-0003145`, `EF-C-0003170`, `EF-C-0003216`, `EF-C-0003397`, `nan`, `EF-C-0003541`, `EF-C-0003604`, `EF-C-0003736`, `EF-C-0003793`, `EF-C-0003814`, `EF-C-0003947`, `EF-C-0003979`, `EF-C-0003983`, `EF-C-0004232`, `EF-C-0004339`, `EF-C-0004370`, `EF-C-0004383`, `EF-C-0004546`, `EF-C-0004587`, `EF-C-0004653`, `EF-C-0004657`, `EF-C-0004683`, `EF-C-0004764`, `EF-C-0004766`, `EF-C-0004807`, `EF-C-0004814`, `EF-C-0004896`, `EF-C-0005056`, `EF-C-0005158`, `EF-C-0005185`, `EF-C-0005233`, `EF-C-0005420`, `EF-C-0005430`, `EF-C-0005456`, `EF-C-0005554`, `EF-C-0005610`, `EF-C-0005637`, `EF-C-0005657`, `EF-C-0005747`, `EF-C-0005779`, `EF-C-0005897`, `EF-C-0006062`, `EF-C-0006254`, `EF-C-0006303`, `EF-C-0006382`, `EF-C-0006420`, `EF-C-0006467`, `EF-C-0006467`, `EF-C-0006603`, `EF-C-0006859`, `EF-C-0006966`, `EF-C-0007178`, `EF-C-0007223`, `EF-C-0007243`, `EF-C-0007326`, `EF-C-0007371`

---

## 4. Missing Value Summary

### 4.1 Frequency dataset

| Column | NaN (raw) | NaN (pre-Step-13) | Reduced by |
| --- | --- | --- | --- |
| policy_id | 224 | 0 | 224 |
| equipment_id | 221 | 0 | 221 |
| equipment_type | 239 | 220 | 19 |
| equipment_age | 144 | 279 | -135 |
| solar_system | 234 | 223 | 11 |
| maintenance_int | 154 | 283 | -129 |
| usage_int | 141 | 268 | -127 |
| exposure | 125 | 269 | -144 |
| claim_count | 175 | 0 | 175 |

### 4.2 Severity dataset

| Column | NaN (raw) | NaN (pre-Step-13) | Reduced by |
| --- | --- | --- | --- |
| claim_id | 28 | 27 | 1 |
| claim_seq | 13 | 35 | -22 |
| policy_id | 22 | 0 | 22 |
| equipment_id | 15 | 0 | 15 |
| equipment_type | 34 | 1 | 33 |
| equipment_age | 10 | 15 | -5 |
| solar_system | 15 | 0 | 15 |
| maintenance_int | 12 | 13 | -1 |
| usage_int | 9 | 13 | -4 |
| exposure | 13 | 16 | -3 |
| claim_amount | 16 | 27 | -11 |

---

## 5. Fallback Strategies Applied (Step 13)

| Dataset | Column | Strategy | NaN Count |
| --- | --- | --- | --- |
| freq | equipment_type | `mode` | 220 |
| freq | equipment_age | `median` | 279 |
| freq | solar_system | `mode` | 223 |
| freq | maintenance_int | `median` | 283 |
| freq | usage_int | `median` | 268 |
| freq | exposure | `median` | 269 |
| sev | equipment_type | `mode` | 1 |
| sev | equipment_age | `median` | 15 |
| sev | maintenance_int | `median` | 13 |
| sev | usage_int | `median` | 13 |
| sev | exposure | `median` | 16 |
| sev | claim_id | `unknown` | 27 |
| sev | claim_seq | `zero` | 35 |
| sev | claim_amount | `drop` | 27 |

---

## 6. How to Change Fallback Strategies

Edit `UNRESOLVABLE_STRATEGY` at the top of the script and re-run.

| Strategy | Effect |
|---|---|
| `flag` | Keeps NaN; adds `<col>_missing` boolean column |
| `drop` | Drops the entire row |
| `median` | Fills with column median (numeric only) |
| `mode` | Fills with most frequent value |
| `zero` | Fills with 0 (numeric only) |
| `unknown` | Fills with `"UNKNOWN"` (categorical only) |

---

## 7. Full Console Audit Trail

```
[15:57:44]  
[15:57:44]  ====================================================================
[15:57:44]  STEP 1 — Loading raw datasets
[15:57:44]  ====================================================================
[15:57:45]    freq loaded : 95,062 rows x 9 columns
[15:57:45]    sev  loaded : 8,272 rows  x 11 columns
[15:57:45]  
[15:57:45]  ====================================================================
[15:57:45]  STEP 2 — Standardising column names
[15:57:45]  ====================================================================
[15:57:45]    freq columns : policy_id, equipment_id, equipment_type, equipment_age, solar_system, maintenance_int, usage_int, exposure, claim_count
[15:57:45]    sev  columns : claim_id, claim_seq, policy_id, equipment_id, equipment_type, equipment_age, solar_system, maintenance_int, usage_int, exposure, claim_amount
[15:57:45]  
[15:57:45]  ====================================================================
[15:57:45]  STEP 3 — Cross-imputing policy_id between datasets (key: equipment_id)
[15:57:45]  ====================================================================
[15:57:45]    Rule: only fill when equipment_id maps to exactly 1 unique policy_id
[15:57:45]    [freq <- sev] policy_id: 17 filled via equipment_id match | 207 still missing
[15:57:46]    [sev <- freq] policy_id: 20 filled via equipment_id match | 2 still missing
[15:57:46]  
[15:57:46]  ====================================================================
[15:57:46]  STEP 4 — Imputing missing policy_id via secondary key combinations
[15:57:46]  ====================================================================
[15:57:46]    Key 1: equipment_id + exposure  (rounded to 4 dp)
[15:57:46]    Key 2: equipment_id + equipment_type  (categorical fallback)
[15:57:46]    Rule : only fill when key maps to exactly 1 unique policy_id
[15:57:47]    [freq] policy_id: no secondary key matches found (207 still missing -> MP-#### in Step 5)
[15:57:47]    [sev <- freq] policy_id: 1 filled via (equipment_id + exposure)
[15:57:48]    [sev] policy_id: 1 recovered | 1 remain (-> MP-#### in Step 5)
[15:57:48]  
[15:57:48]  ====================================================================
[15:57:48]  STEP 5 — Assigning placeholder IDs for still-missing policy_id / equipment_id
[15:57:48]  ====================================================================
[15:57:48]    policy_id    placeholders: MP-0001, MP-0002, ...
[15:57:48]    equipment_id placeholders: ME-0001, ME-0002, ...
[15:57:48]    [freq] policy_id   : 207 NaN -> MP-0001 ... MP-0207
[15:57:48]    [freq] equipment_id: 221 NaN -> ME-0001 ... ME-0221
[15:57:48]    [sev] policy_id   : 1 NaN -> MP-0208 ... MP-0208
[15:57:48]    [sev] equipment_id: 15 NaN -> ME-0222 ... ME-0236
[15:57:48]  
[15:57:48]  ====================================================================
[15:57:48]  STEP 6 — Fixing corrupted categorical values (_???XXXX noise)
[15:57:48]  ====================================================================
[15:57:48]    Rule: strip suffix; set non-canonical residuals to NaN
[15:57:49]    [freq] equipment_type: 0 non-canonical cleared | NaN 239 -> 239
[15:57:49]    [freq] solar_system  : 0 non-canonical cleared | NaN 234 -> 234
[15:57:49]    [sev] equipment_type: 0 non-canonical cleared | NaN 34 -> 34
[15:57:49]    [sev] solar_system  : 0 non-canonical cleared | NaN 15 -> 15
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 7 — Cross-imputing shared columns (key: policy_id + equipment_id)
[15:57:49]  ====================================================================
[15:57:49]    Columns: equipment_type, equipment_age, solar_system, maintenance_int, usage_int, exposure
[15:57:49]    [freq <- sev] 'equipment_type': filled 19 NaN values
[15:57:49]    [freq <- sev] 'equipment_age': filled 9 NaN values
[15:57:49]    [freq <- sev] 'solar_system': filled 11 NaN values
[15:57:49]    [freq <- sev] 'maintenance_int': filled 7 NaN values
[15:57:49]    [freq <- sev] 'usage_int': filled 10 NaN values
[15:57:49]    [freq <- sev] 'exposure': filled 8 NaN values
[15:57:49]    [sev <- freq] 'equipment_type': filled 33 NaN values
[15:57:49]    [sev <- freq] 'equipment_age': filled 10 NaN values
[15:57:49]    [sev <- freq] 'solar_system': filled 15 NaN values
[15:57:49]    [sev <- freq] 'maintenance_int': filled 12 NaN values
[15:57:49]    [sev <- freq] 'usage_int': filled 8 NaN values
[15:57:49]    [sev <- freq] 'exposure': filled 13 NaN values
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 8 — Converting invalid negative values to NaN
[15:57:49]  ====================================================================
[15:57:49]    Rule: all listed fields must be >= 0
[15:57:49]    [freq] 'equipment_age': 144 negative values -> NaN
[15:57:49]    [freq] 'maintenance_int': 136 negative values -> NaN
[15:57:49]    [freq] 'usage_int': 137 negative values -> NaN
[15:57:49]    [freq] 'exposure': 152 negative values -> NaN
[15:57:49]    [freq] 'claim_count': 12 negative values -> NaN
[15:57:49]    [sev] 'equipment_age': 15 negative values -> NaN
[15:57:49]    [sev] 'maintenance_int': 13 negative values -> NaN
[15:57:49]    [sev] 'usage_int': 13 negative values -> NaN
[15:57:49]    [sev] 'exposure': 16 negative values -> NaN
[15:57:49]    [sev] 'claim_amount': 11 negative values -> NaN
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 9 — Fixing out-of-range exposure values (valid range: 0 to 1)
[15:57:49]  ====================================================================
[15:57:49]    [freq] exposure: 138 values > 1 | 138 rescaled (div 10/100) | 0 -> NaN
[15:57:49]    [sev] exposure: 11 values > 1 | 11 rescaled (div 10/100) | 0 -> NaN
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 10 — Fixing claim_count (freq) and claim_seq (sev)
[15:57:49]  ====================================================================
[15:57:49]    [freq] claim_count: 18 non-integer floats -> NaN
[15:57:49]    [sev] claim_seq: 12 non-integer floats -> NaN
[15:57:49]    [sev] claim_seq: 11 negative values -> NaN
[15:57:49]    [freq] Deriving claim_count = COUNT(sev rows) per policy_id ...
[15:57:49]    [freq] claim_count: 45 derived from sev row count | 160 set to 0 (no sev rows for policy)
[15:57:49]    [freq] Verifying all claim_count values against sev row counts ...
[15:57:49]    [freq] claim_count: 1077 values corrected to match sev row count
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 11 — Capping continuous variables at 99th percentile
[15:57:49]  ====================================================================
[15:57:49]    Columns: equipment_age, maintenance_int, usage_int (both datasets)
[15:57:49]    Percentile computed on non-null, non-negative values only
[15:57:49]    [freq] 'equipment_age': 99th pct = 21.8749 | 948 values capped
[15:57:49]    [freq] 'maintenance_int': 99th pct = 1786.2300 | 946 values capped
[15:57:49]    [freq] 'usage_int': 99th pct = 23.8000 | 941 values capped
[15:57:49]    [sev] 'equipment_age': 99th pct = 23.2530 | 81 values capped
[15:57:49]    [sev] 'maintenance_int': 99th pct = 1792.1366 | 83 values capped
[15:57:49]    [sev] 'usage_int': 99th pct = 23.8700 | 76 values capped
[15:57:49]  
[15:57:49]  ====================================================================
[15:57:49]  STEP 11a — Dropping sev rows where claim_amount > 99th percentile
[15:57:49]  ====================================================================
[15:57:49]    [sev] claim_amount: threshold = 296,054.9200 | 83 rows dropped | 8,189 rows remain
[15:57:49]    [sev] dropped claim_ids: EF-C-0000275, EF-C-0000308, EF-C-0000353, EF-C-0001020, EF-C-0001081, EF-C-0001114, EF-C-0001159, EF-C-0001382, EF-C-0001401, EF-C-0001426 ... (+73 more)
[15:57:49]    [freq] Re-syncing claim_count after sev row drops ...
[15:57:50]    [freq] claim_count: 94 values updated to reflect dropped sev rows
[15:57:50]  
[15:57:50]  ====================================================================
[15:57:50]  STEP 12 — Casting claim_count and claim_seq to Int64
[15:57:50]  ====================================================================
[15:57:50]    [freq] claim_count -> Int64
[15:57:50]    [sev]  claim_seq   -> Int64
[15:57:50]    [sev]  claim_amount already numeric (float64)
[15:57:50]  
[15:57:50]  ====================================================================
[15:57:50]  STEP 13 — Applying fallback strategies for remaining NaN values
[15:57:50]  ====================================================================
[15:57:50]    [freq] 'equipment_type': 220 NaN remain -> strategy = 'mode'
[15:57:50]      Filled with mode = ReglAggregators
[15:57:50]    [freq] 'equipment_age': 279 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 10.0010
[15:57:50]    [freq] 'solar_system': 223 NaN remain -> strategy = 'mode'
[15:57:50]      Filled with mode = Epsilon
[15:57:50]    [freq] 'maintenance_int': 283 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 951.6000
[15:57:50]    [freq] 'usage_int': 268 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 12.0100
[15:57:50]    [freq] 'exposure': 269 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 0.4990
[15:57:50]    [sev] 'equipment_type': 1 NaN remain -> strategy = 'mode'
[15:57:50]      Filled with mode = ReglAggregators
[15:57:50]    [sev] 'equipment_age': 15 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 11.6415
[15:57:50]    [sev] 'maintenance_int': 13 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 1049.1250
[15:57:50]    [sev] 'usage_int': 13 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 15.0400
[15:57:50]    [sev] 'exposure': 16 NaN remain -> strategy = 'median'
[15:57:50]      Filled with median = 0.6140
[15:57:50]    [sev] 'claim_id': 27 NaN remain -> strategy = 'unknown'
[15:57:50]      Filled with 'UNKNOWN'
[15:57:50]    [sev] 'claim_seq': 35 NaN remain -> strategy = 'zero'
[15:57:50]      Filled with 0
[15:57:50]    [sev] 'claim_amount': 27 NaN remain -> strategy = 'drop'
[15:57:50]      Dropped 27 rows
[15:57:50]  
[15:57:50]  ====================================================================
[15:57:50]  STEP 14 — Saving cleaned datasets
[15:57:50]  ====================================================================
[15:57:50]    Saved -> cleaned_freq.csv  (95,062 rows x 9 cols)
[15:57:50]    Saved -> cleaned_sev.csv   (8,162 rows  x 11 cols)
[15:57:50]  
[15:57:50]  ====================================================================
[15:57:50]  STEP 15 — Generating Markdown audit report
[15:57:50]  ====================================================================
```

---

*Report generated by `clean_equipment_claims.py`*
