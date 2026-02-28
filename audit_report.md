# Equipment Failure Claims — Audit Report

**Generated:** 2026-02-28 15:39:24
**Script:** `audit_equipment_claims.py`

| File | Path |
|---|---|
| Raw frequency | `data_clean\test_equipment_fail\equipment_failure_claims_freq.csv` |
| Raw severity | `data_clean\test_equipment_fail\equipment_failure_claims_sev.csv` |
| Cleaned frequency | `cleaned_freq.csv` |
| Cleaned severity | `cleaned_sev.csv` |

---

## Summary of All Checks

| Check | Status | Detail |
| --- | --- | --- |
| cleaned_freq: no NaN values | ✅ PASS | All data columns are fully populated. |
| cleaned_sev: no NaN values | ✅ PASS | All data columns are fully populated. |
| Claim amount total: raw (no-neg) = 738,762,470.79 | cleaned = 688,799,002.02 | diff = -49, | ❌ FAIL | Difference of -6.763% exceeds threshold. Investigate row-level changes below. |
| claim_amount NaN: raw = 16 | cleaned = 0 | ✅ PASS | No NaN in cleaned claim_amount. |
| Row-level changes: 1765 capped | 2 negatives nulled | ✅ PASS | 1765 claim_amount values were capped at the 99th percentile.
2 claim_amount values were negative and set to NaN. |
| [RAW] 54 policy_id(s) in sev but not in freq (0.8% of sev policies) | ⚠️ WARN | Sample orphaned IDs: EF-025700, EF-028268_???3303, EF-062403, EF-064334, EF-069893, EF-070602, EF-085083, EF-085793_???6 |
| [CLEANED] 39 policy_id(s) in sev but not in freq (0.6% of sev policies) | ⚠️ WARN | Sample orphaned IDs: EF-025700, EF-028268_???3303, EF-064334, EF-085793_???6763, EF-169926_???4703, EF-194033_???2401, E |

---

## A. NaN Audit — Cleaned Files

Checks every data column (excluding auto-generated `_missing` flag columns)
for remaining `NaN` values after the cleaning pipeline.

### A.1 NaN counts per column

| File | Column | NaN Count | % of Rows | Note |
| --- | --- | --- | --- | --- |
| cleaned_freq | — | 0 | 0 | No NaN values |
| cleaned_sev | — | 0 | 0 | No NaN values |



---

## B. Claim Amount Reconciliation

Compares `claim_amount` totals between the raw and cleaned severity files.
The cleaned total is expected to be **slightly lower** than the raw
(negatives-excluded) total due to 99th percentile capping.

### B.1 Totals

| Metric | Value |
| --- | --- |
| Raw total (excl. negatives) | 738,762,470.79 |
| Raw total (incl. negatives) | 737,830,531.79 |
| Cleaned total | 688,799,002.02 |
| Difference (cleaned − raw) | -49,963,468.77 |
| Difference % | -6.763% |
| NaN in raw claim_amount | 16 |
| NaN in cleaned claim_amount | 0 |

> The raw total **excluding negatives** is the correct baseline for comparison
> because negative values are erroneous and were removed during cleaning.

### B.2 Row-level changes

Rows where `claim_amount` changed between raw and cleaned:

| claim_id | Raw Amount | Cleaned Amount | Delta | Reason |
| --- | --- | --- | --- | --- |
| EF-C-0000051 | 108666.0 | 67504.0 | -41162.0 | capped at 99th pct |
| EF-C-0000051 | 67504.0 | 108666.0 | 41162.0 | adjusted (other) |
| EF-C-0000052 | 57951.0 | 40820.0 | -17131.0 | capped at 99th pct |
| EF-C-0000052 | 40820.0 | 57951.0 | 17131.0 | adjusted (other) |
| EF-C-0000057 | 46774.0 | 75730.0 | 28956.0 | adjusted (other) |
| EF-C-0000057 | 75730.0 | 46774.0 | -28956.0 | capped at 99th pct |
| EF-C-0000058 | 144987.0 | 73272.0 | -71715.0 | capped at 99th pct |
| EF-C-0000058 | 73272.0 | 144987.0 | 71715.0 | adjusted (other) |
| EF-C-0000084 | 106642.0 | 72232.0 | -34410.0 | capped at 99th pct |
| EF-C-0000084 | 72232.0 | 106642.0 | 34410.0 | adjusted (other) |
| EF-C-0000085 | 75042.0 | 36828.0 | -38214.0 | capped at 99th pct |
| EF-C-0000085 | 36828.0 | 75042.0 | 38214.0 | adjusted (other) |
| EF-C-0000091 | 17988.0 | 40307.0 | 22319.0 | adjusted (other) |
| EF-C-0000091 | 40307.0 | 17988.0 | -22319.0 | capped at 99th pct |
| EF-C-0000092 | 12761.0 | 71344.0 | 58583.0 | adjusted (other) |
| EF-C-0000092 | 71344.0 | 12761.0 | -58583.0 | capped at 99th pct |
| EF-C-0000147 | 226066.0 | 41567.0 | -184499.0 | capped at 99th pct |
| EF-C-0000147 | 41567.0 | 226066.0 | 184499.0 | adjusted (other) |
| EF-C-0000148 | 147585.0 | 148802.0 | 1217.0 | adjusted (other) |
| EF-C-0000148 | 148802.0 | 147585.0 | -1217.0 | capped at 99th pct |
| EF-C-0000172 | 88597.0 | 202042.0 | 113445.0 | adjusted (other) |
| EF-C-0000172 | 202042.0 | 88597.0 | -113445.0 | capped at 99th pct |
| EF-C-0000173 | 37948.0 | 64216.0 | 26268.0 | adjusted (other) |
| EF-C-0000173 | 64216.0 | 37948.0 | -26268.0 | capped at 99th pct |
| EF-C-0000176 | 46863.0 | 62194.0 | 15331.0 | adjusted (other) |
| EF-C-0000176 | 62194.0 | 46863.0 | -15331.0 | capped at 99th pct |
| EF-C-0000197 | 221973.0 | 140646.0 | -81327.0 | capped at 99th pct |
| EF-C-0000197 | 221973.0 | 119258.0 | -102715.0 | capped at 99th pct |
| EF-C-0000197 | 140646.0 | 221973.0 | 81327.0 | adjusted (other) |
| EF-C-0000197 | 140646.0 | 119258.0 | -21388.0 | capped at 99th pct |
| EF-C-0000197 | 119258.0 | 221973.0 | 102715.0 | adjusted (other) |
| EF-C-0000197 | 119258.0 | 140646.0 | 21388.0 | adjusted (other) |
| EF-C-0000198 | 143636.0 | 145472.0 | 1836.0 | adjusted (other) |
| EF-C-0000198 | 143636.0 | 68485.0 | -75151.0 | capped at 99th pct |
| EF-C-0000198 | 145472.0 | 143636.0 | -1836.0 | capped at 99th pct |
| EF-C-0000198 | 145472.0 | 68485.0 | -76987.0 | capped at 99th pct |
| EF-C-0000198 | 68485.0 | 143636.0 | 75151.0 | adjusted (other) |
| EF-C-0000198 | 68485.0 | 145472.0 | 76987.0 | adjusted (other) |
| EF-C-0000199 | 185808.0 | 156722.0 | -29086.0 | capped at 99th pct |
| EF-C-0000199 | 185808.0 | 74149.0 | -111659.0 | capped at 99th pct |
| EF-C-0000199 | 156722.0 | 185808.0 | 29086.0 | adjusted (other) |
| EF-C-0000199 | 156722.0 | 74149.0 | -82573.0 | capped at 99th pct |
| EF-C-0000199 | 74149.0 | 185808.0 | 111659.0 | adjusted (other) |
| EF-C-0000199 | 74149.0 | 156722.0 | 82573.0 | adjusted (other) |
| EF-C-0000209 | 46019.0 | 79125.0 | 33106.0 | adjusted (other) |
| EF-C-0000209 | 79125.0 | 46019.0 | -33106.0 | capped at 99th pct |
| EF-C-0000210 | 102223.0 | 56263.0 | -45960.0 | capped at 99th pct |
| EF-C-0000210 | 56263.0 | 102223.0 | 45960.0 | adjusted (other) |
| EF-C-0000218 | 28581.0 | 134506.0 | 105925.0 | adjusted (other) |
| EF-C-0000218 | 28581.0 | 65616.0 | 37035.0 | adjusted (other) |
| EF-C-0000218 | 134506.0 | 28581.0 | -105925.0 | capped at 99th pct |
| EF-C-0000218 | 134506.0 | 65616.0 | -68890.0 | capped at 99th pct |
| EF-C-0000218 | 65616.0 | 28581.0 | -37035.0 | capped at 99th pct |
| EF-C-0000218 | 65616.0 | 134506.0 | 68890.0 | adjusted (other) |
| EF-C-0000219 | 56975.0 | 61742.0 | 4767.0 | adjusted (other) |
| EF-C-0000219 | 56975.0 | 44013.0 | -12962.0 | capped at 99th pct |
| EF-C-0000219 | 61742.0 | 56975.0 | -4767.0 | capped at 99th pct |
| EF-C-0000219 | 61742.0 | 44013.0 | -17729.0 | capped at 99th pct |
| EF-C-0000219 | 44013.0 | 56975.0 | 12962.0 | adjusted (other) |
| EF-C-0000219 | 44013.0 | 61742.0 | 17729.0 | adjusted (other) |
| EF-C-0000220 | 59096.0 | 64800.0 | 5704.0 | adjusted (other) |
| EF-C-0000220 | 59096.0 | 83732.0 | 24636.0 | adjusted (other) |
| EF-C-0000220 | 64800.0 | 59096.0 | -5704.0 | capped at 99th pct |
| EF-C-0000220 | 64800.0 | 83732.0 | 18932.0 | adjusted (other) |
| EF-C-0000220 | 83732.0 | 59096.0 | -24636.0 | capped at 99th pct |
| EF-C-0000220 | 83732.0 | 64800.0 | -18932.0 | capped at 99th pct |
| EF-C-0000224 | 201094.0 | 72766.0 | -128328.0 | capped at 99th pct |
| EF-C-0000224 | 72766.0 | 201094.0 | 128328.0 | adjusted (other) |
| EF-C-0000225 | 29943.0 | 66279.0 | 36336.0 | adjusted (other) |
| EF-C-0000225 | 66279.0 | 29943.0 | -36336.0 | capped at 99th pct |
| EF-C-0000228 | 241443.0 | 54813.0 | -186630.0 | capped at 99th pct |
| EF-C-0000228 | 54813.0 | 241443.0 | 186630.0 | adjusted (other) |
| EF-C-0000229 | 78415.0 | 131708.0 | 53293.0 | adjusted (other) |
| EF-C-0000229 | 131708.0 | 78415.0 | -53293.0 | capped at 99th pct |
| EF-C-0000236 | 119018.0 | 81464.0 | -37554.0 | capped at 99th pct |
| EF-C-0000236 | 81464.0 | 119018.0 | 37554.0 | adjusted (other) |
| EF-C-0000237 | 63856.0 | 249998.0 | 186142.0 | adjusted (other) |
| EF-C-0000237 | 249998.0 | 63856.0 | -186142.0 | capped at 99th pct |
| EF-C-0000242 | 41298.0 | 54093.0 | 12795.0 | adjusted (other) |
| EF-C-0000242 | 54093.0 | 41298.0 | -12795.0 | capped at 99th pct |
| EF-C-0000243 | 38913.0 | 63954.0 | 25041.0 | adjusted (other) |
| EF-C-0000243 | 63954.0 | 38913.0 | -25041.0 | capped at 99th pct |
| EF-C-0000260 | 50705.0 | 73653.0 | 22948.0 | adjusted (other) |
| EF-C-0000260 | 73653.0 | 50705.0 | -22948.0 | capped at 99th pct |
| EF-C-0000261 | 64014.0 | 29660.0 | -34354.0 | capped at 99th pct |
| EF-C-0000261 | 29660.0 | 64014.0 | 34354.0 | adjusted (other) |
| EF-C-0000281 | 82588.0 | 81144.0 | -1444.0 | capped at 99th pct |
| EF-C-0000281 | 81144.0 | 82588.0 | 1444.0 | adjusted (other) |
| EF-C-0000282 | 108579.0 | 245454.0 | 136875.0 | adjusted (other) |
| EF-C-0000282 | 108579.0 | 104730.0 | -3849.0 | capped at 99th pct |
| EF-C-0000282 | 245454.0 | 108579.0 | -136875.0 | capped at 99th pct |
| EF-C-0000282 | 245454.0 | 104730.0 | -140724.0 | capped at 99th pct |
| EF-C-0000282 | 104730.0 | 108579.0 | 3849.0 | adjusted (other) |
| EF-C-0000282 | 104730.0 | 245454.0 | 140724.0 | adjusted (other) |
| EF-C-0000283 | 92243.0 | 80405.0 | -11838.0 | capped at 99th pct |
| EF-C-0000283 | 92243.0 | 83374.0 | -8869.0 | capped at 99th pct |
| EF-C-0000283 | 80405.0 | 92243.0 | 11838.0 | adjusted (other) |
| EF-C-0000283 | 80405.0 | 83374.0 | 2969.0 | adjusted (other) |
| EF-C-0000283 | 83374.0 | 92243.0 | 8869.0 | adjusted (other) |
| EF-C-0000283 | 83374.0 | 80405.0 | -2969.0 | capped at 99th pct |
| EF-C-0000285 | 70215.0 | 59737.0 | -10478.0 | capped at 99th pct |
| EF-C-0000285 | 59737.0 | 70215.0 | 10478.0 | adjusted (other) |
| EF-C-0000286 | 74510.0 | 59008.0 | -15502.0 | capped at 99th pct |
| EF-C-0000286 | 59008.0 | 74510.0 | 15502.0 | adjusted (other) |
| EF-C-0000328 | 82068.0 | 76490.0 | -5578.0 | capped at 99th pct |
| EF-C-0000328 | 76490.0 | 82068.0 | 5578.0 | adjusted (other) |
| EF-C-0000329 | 52378.0 | 58951.0 | 6573.0 | adjusted (other) |
| EF-C-0000329 | 58951.0 | 52378.0 | -6573.0 | capped at 99th pct |
| EF-C-0000331 | 152031.0 | 80715.0 | -71316.0 | capped at 99th pct |
| EF-C-0000331 | 80715.0 | 152031.0 | 71316.0 | adjusted (other) |
| EF-C-0000332 | 87805.0 | 68457.0 | -19348.0 | capped at 99th pct |
| EF-C-0000332 | 68457.0 | 87805.0 | 19348.0 | adjusted (other) |
| EF-C-0000333 | 108677.0 | 62145.0 | -46532.0 | capped at 99th pct |
| EF-C-0000333 | 62145.0 | 108677.0 | 46532.0 | adjusted (other) |
| EF-C-0000334 | 74756.0 | 69594.0 | -5162.0 | capped at 99th pct |
| EF-C-0000334 | 69594.0 | 74756.0 | 5162.0 | adjusted (other) |
| EF-C-0000342 | 125521.0 | 190573.0 | 65052.0 | adjusted (other) |
| EF-C-0000342 | 125521.0 | 37218.0 | -88303.0 | capped at 99th pct |
| EF-C-0000342 | 190573.0 | 125521.0 | -65052.0 | capped at 99th pct |
| EF-C-0000342 | 190573.0 | 37218.0 | -153355.0 | capped at 99th pct |
| EF-C-0000342 | 37218.0 | 125521.0 | 88303.0 | adjusted (other) |
| EF-C-0000342 | 37218.0 | 190573.0 | 153355.0 | adjusted (other) |
| EF-C-0000343 | 80161.0 | 50203.0 | -29958.0 | capped at 99th pct |
| EF-C-0000343 | 80161.0 | 202272.0 | 122111.0 | adjusted (other) |
| EF-C-0000343 | 50203.0 | 80161.0 | 29958.0 | adjusted (other) |
| EF-C-0000343 | 50203.0 | 202272.0 | 152069.0 | adjusted (other) |
| EF-C-0000343 | 202272.0 | 80161.0 | -122111.0 | capped at 99th pct |
| EF-C-0000343 | 202272.0 | 50203.0 | -152069.0 | capped at 99th pct |
| EF-C-0000344 | 42150.0 | 82818.0 | 40668.0 | adjusted (other) |
| EF-C-0000344 | 42150.0 | 68204.0 | 26054.0 | adjusted (other) |
| EF-C-0000344 | 82818.0 | 42150.0 | -40668.0 | capped at 99th pct |
| EF-C-0000344 | 82818.0 | 68204.0 | -14614.0 | capped at 99th pct |
| EF-C-0000344 | 68204.0 | 42150.0 | -26054.0 | capped at 99th pct |
| EF-C-0000344 | 68204.0 | 82818.0 | 14614.0 | adjusted (other) |
| EF-C-0000426 | 58251.0 | 57310.0 | -941.0 | capped at 99th pct |
| EF-C-0000426 | 57310.0 | 58251.0 | 941.0 | adjusted (other) |
| EF-C-0000427 | 109276.0 | 146650.0 | 37374.0 | adjusted (other) |
| EF-C-0000427 | 146650.0 | 109276.0 | -37374.0 | capped at 99th pct |
| EF-C-0000429 | 56970.0 | 44488.0 | -12482.0 | capped at 99th pct |
| EF-C-0000429 | 44488.0 | 56970.0 | 12482.0 | adjusted (other) |
| EF-C-0000430 | 41543.0 | 32452.0 | -9091.0 | capped at 99th pct |
| EF-C-0000430 | 32452.0 | 41543.0 | 9091.0 | adjusted (other) |
| EF-C-0000448 | 70100.0 | 59630.0 | -10470.0 | capped at 99th pct |
| EF-C-0000448 | 59630.0 | 70100.0 | 10470.0 | adjusted (other) |
| EF-C-0000449 | 40322.0 | 39194.0 | -1128.0 | capped at 99th pct |
| EF-C-0000449 | 39194.0 | 40322.0 | 1128.0 | adjusted (other) |
| EF-C-0000465 | 102519.0 | 59023.0 | -43496.0 | capped at 99th pct |
| EF-C-0000465 | 59023.0 | 102519.0 | 43496.0 | adjusted (other) |
| EF-C-0000466 | 28917.0 | 32539.0 | 3622.0 | adjusted (other) |
| EF-C-0000466 | 32539.0 | 28917.0 | -3622.0 | capped at 99th pct |
| EF-C-0000470 | 46169.0 | 107339.0 | 61170.0 | adjusted (other) |
| EF-C-0000470 | 107339.0 | 46169.0 | -61170.0 | capped at 99th pct |
| EF-C-0000471 | 96467.0 | 60918.0 | -35549.0 | capped at 99th pct |
| EF-C-0000471 | 60918.0 | 96467.0 | 35549.0 | adjusted (other) |
| EF-C-0000500 | 38993.0 | 32971.0 | -6022.0 | capped at 99th pct |
| EF-C-0000500 | 32971.0 | 38993.0 | 6022.0 | adjusted (other) |
| EF-C-0000501 | 43852.0 | 64811.0 | 20959.0 | adjusted (other) |
| EF-C-0000501 | 64811.0 | 43852.0 | -20959.0 | capped at 99th pct |
| EF-C-0000533 | 167426.0 | 157116.0 | -10310.0 | capped at 99th pct |
| EF-C-0000533 | 167426.0 | 64710.0 | -102716.0 | capped at 99th pct |
| EF-C-0000533 | 157116.0 | 167426.0 | 10310.0 | adjusted (other) |
| EF-C-0000533 | 157116.0 | 64710.0 | -92406.0 | capped at 99th pct |
| EF-C-0000533 | 64710.0 | 167426.0 | 102716.0 | adjusted (other) |
| EF-C-0000533 | 64710.0 | 157116.0 | 92406.0 | adjusted (other) |
| EF-C-0000534 | 143924.0 | 19898.0 | -124026.0 | capped at 99th pct |
| EF-C-0000534 | 143924.0 | 86018.0 | -57906.0 | capped at 99th pct |
| EF-C-0000534 | 19898.0 | 143924.0 | 124026.0 | adjusted (other) |
| EF-C-0000534 | 19898.0 | 86018.0 | 66120.0 | adjusted (other) |
| EF-C-0000534 | 86018.0 | 143924.0 | 57906.0 | adjusted (other) |
| EF-C-0000534 | 86018.0 | 19898.0 | -66120.0 | capped at 99th pct |
| EF-C-0000535 | 29555.0 | 92042.0 | 62487.0 | adjusted (other) |
| EF-C-0000535 | 29555.0 | 89617.0 | 60062.0 | adjusted (other) |
| EF-C-0000535 | 92042.0 | 29555.0 | -62487.0 | capped at 99th pct |
| EF-C-0000535 | 92042.0 | 89617.0 | -2425.0 | capped at 99th pct |
| EF-C-0000535 | 89617.0 | 29555.0 | -60062.0 | capped at 99th pct |
| EF-C-0000535 | 89617.0 | 92042.0 | 2425.0 | adjusted (other) |
| EF-C-0000613 | 39366.0 | 143087.0 | 103721.0 | adjusted (other) |
| EF-C-0000613 | 143087.0 | 39366.0 | -103721.0 | capped at 99th pct |
| EF-C-0000614 | 55990.0 | 91178.0 | 35188.0 | adjusted (other) |
| EF-C-0000614 | 91178.0 | 55990.0 | -35188.0 | capped at 99th pct |
| EF-C-0000639 | 169205.0 | 169240.0 | 35.0 | adjusted (other) |
| EF-C-0000639 | 169240.0 | 169205.0 | -35.0 | capped at 99th pct |
| EF-C-0000640 | 124502.0 | 108051.0 | -16451.0 | capped at 99th pct |
| EF-C-0000640 | 108051.0 | 124502.0 | 16451.0 | adjusted (other) |
| EF-C-0000659 | 80574.0 | 71069.0 | -9505.0 | capped at 99th pct |
| EF-C-0000659 | 71069.0 | 80574.0 | 9505.0 | adjusted (other) |
| EF-C-0000660 | 247576.0 | 149848.0 | -97728.0 | capped at 99th pct |
| EF-C-0000660 | 149848.0 | 247576.0 | 97728.0 | adjusted (other) |
| EF-C-0000670 | 148464.0 | 221133.0 | 72669.0 | adjusted (other) |
| EF-C-0000670 | 221133.0 | 148464.0 | -72669.0 | capped at 99th pct |
| EF-C-0000671 | 117222.0 | 122127.0 | 4905.0 | adjusted (other) |
| EF-C-0000671 | 122127.0 | 117222.0 | -4905.0 | capped at 99th pct |
| EF-C-0000684 | 41261.0 | 72185.0 | 30924.0 | adjusted (other) |
| EF-C-0000684 | 72185.0 | 41261.0 | -30924.0 | capped at 99th pct |
| EF-C-0000685 | 26563.0 | 72290.0 | 45727.0 | adjusted (other) |
| EF-C-0000685 | 72290.0 | 26563.0 | -45727.0 | capped at 99th pct |
| EF-C-0000740 | 165046.0 | 132249.0 | -32797.0 | capped at 99th pct |
| EF-C-0000740 | 132249.0 | 165046.0 | 32797.0 | adjusted (other) |
| EF-C-0000741 | 78009.0 | 93396.0 | 15387.0 | adjusted (other) |
| EF-C-0000741 | 93396.0 | 78009.0 | -15387.0 | capped at 99th pct |
| EF-C-0000758 | 91153.0 | 157260.0 | 66107.0 | adjusted (other) |
| EF-C-0000758 | 157260.0 | 91153.0 | -66107.0 | capped at 99th pct |
| EF-C-0000759 | 55412.0 | 94394.0 | 38982.0 | adjusted (other) |
| EF-C-0000759 | 94394.0 | 55412.0 | -38982.0 | capped at 99th pct |
| EF-C-0000762 | 47503.0 | 39562.0 | -7941.0 | capped at 99th pct |
| EF-C-0000762 | 39562.0 | 47503.0 | 7941.0 | adjusted (other) |
| EF-C-0000763 | 72344.0 | 92704.0 | 20360.0 | adjusted (other) |
| EF-C-0000763 | 92704.0 | 72344.0 | -20360.0 | capped at 99th pct |
| EF-C-0000775 | 40406.0 | 50338.0 | 9932.0 | adjusted (other) |
| EF-C-0000775 | 50338.0 | 40406.0 | -9932.0 | capped at 99th pct |
| EF-C-0000776 | 91797.0 | 107959.0 | 16162.0 | adjusted (other) |
| EF-C-0000776 | 107959.0 | 91797.0 | -16162.0 | capped at 99th pct |
| EF-C-0000787 | 109165.0 | 165590.0 | 56425.0 | adjusted (other) |
| EF-C-0000787 | 165590.0 | 109165.0 | -56425.0 | capped at 99th pct |
| EF-C-0000788 | 48788.0 | 52648.0 | 3860.0 | adjusted (other) |
| EF-C-0000788 | 52648.0 | 48788.0 | -3860.0 | capped at 99th pct |
| EF-C-0000810 | 54875.0 | 18686.0 | -36189.0 | capped at 99th pct |
| EF-C-0000810 | 18686.0 | 54875.0 | 36189.0 | adjusted (other) |
| EF-C-0000811 | 57709.0 | 109690.0 | 51981.0 | adjusted (other) |
| EF-C-0000811 | 109690.0 | 57709.0 | -51981.0 | capped at 99th pct |
| EF-C-0000849 | 61050.0 | 73690.0 | 12640.0 | adjusted (other) |
| EF-C-0000849 | 73690.0 | 61050.0 | -12640.0 | capped at 99th pct |
| EF-C-0000850 | 63863.0 | 106314.0 | 42451.0 | adjusted (other) |
| EF-C-0000850 | 106314.0 | 63863.0 | -42451.0 | capped at 99th pct |
| EF-C-0000883 | 148879.0 | 76017.0 | -72862.0 | capped at 99th pct |
| EF-C-0000883 | 76017.0 | 148879.0 | 72862.0 | adjusted (other) |
| EF-C-0000884 | 113067.0 | 98711.0 | -14356.0 | capped at 99th pct |
| EF-C-0000884 | 98711.0 | 113067.0 | 14356.0 | adjusted (other) |
| EF-C-0000902 | 109879.0 | 39321.0 | -70558.0 | capped at 99th pct |
| EF-C-0000902 | 39321.0 | 109879.0 | 70558.0 | adjusted (other) |
| EF-C-0000948 | 40074.0 | 37288.0 | -2786.0 | capped at 99th pct |
| EF-C-0000948 | 37288.0 | 40074.0 | 2786.0 | adjusted (other) |
| EF-C-0000949 | 50607.0 | 36898.0 | -13709.0 | capped at 99th pct |
| EF-C-0000949 | 36898.0 | 50607.0 | 13709.0 | adjusted (other) |
| EF-C-0000960 | 15250.0 | 41371.0 | 26121.0 | adjusted (other) |
| EF-C-0000960 | 41371.0 | 15250.0 | -26121.0 | capped at 99th pct |
| EF-C-0000961 | 78667.0 | 72278.0 | -6389.0 | capped at 99th pct |
| EF-C-0000961 | 72278.0 | 78667.0 | 6389.0 | adjusted (other) |
| EF-C-0000970 | 24772.0 | 56320.0 | 31548.0 | adjusted (other) |
| EF-C-0000970 | 56320.0 | 24772.0 | -31548.0 | capped at 99th pct |
| EF-C-0000971 | 117565.0 | 31566.0 | -85999.0 | capped at 99th pct |
| EF-C-0000971 | 31566.0 | 117565.0 | 85999.0 | adjusted (other) |
| EF-C-0000974 | 94920.0 | 156888.0 | 61968.0 | adjusted (other) |
| EF-C-0000974 | 156888.0 | 94920.0 | -61968.0 | capped at 99th pct |
| EF-C-0000975 | 57834.0 | 123817.0 | 65983.0 | adjusted (other) |
| EF-C-0000975 | 123817.0 | 57834.0 | -65983.0 | capped at 99th pct |
| EF-C-0000986 | 41656.0 | 38540.0 | -3116.0 | capped at 99th pct |
| EF-C-0000986 | 38540.0 | 41656.0 | 3116.0 | adjusted (other) |
| EF-C-0000987 | 91325.0 | 31322.0 | -60003.0 | capped at 99th pct |
| EF-C-0000987 | 31322.0 | 91325.0 | 60003.0 | adjusted (other) |
| EF-C-0001024 | 13668.0 | 20326.0 | 6658.0 | adjusted (other) |
| EF-C-0001024 | 20326.0 | 13668.0 | -6658.0 | capped at 99th pct |
| EF-C-0001025 | 91472.0 | 54708.0 | -36764.0 | capped at 99th pct |
| EF-C-0001025 | 54708.0 | 91472.0 | 36764.0 | adjusted (other) |
| EF-C-0001052 | 71674.0 | 33154.0 | -38520.0 | capped at 99th pct |
| EF-C-0001052 | 33154.0 | 71674.0 | 38520.0 | adjusted (other) |
| EF-C-0001053 | 64487.0 | 30106.0 | -34381.0 | capped at 99th pct |
| EF-C-0001053 | 30106.0 | 64487.0 | 34381.0 | adjusted (other) |
| EF-C-0001060 | 43104.0 | 76203.0 | 33099.0 | adjusted (other) |
| EF-C-0001060 | 76203.0 | 43104.0 | -33099.0 | capped at 99th pct |
| EF-C-0001061 | 42474.0 | 40803.0 | -1671.0 | capped at 99th pct |
| EF-C-0001061 | 40803.0 | 42474.0 | 1671.0 | adjusted (other) |
| EF-C-0001076 | 48507.0 | 64732.0 | 16225.0 | adjusted (other) |
| EF-C-0001076 | 48507.0 | 71876.0 | 23369.0 | adjusted (other) |
| EF-C-0001076 | 64732.0 | 48507.0 | -16225.0 | capped at 99th pct |
| EF-C-0001076 | 64732.0 | 71876.0 | 7144.0 | adjusted (other) |
| EF-C-0001076 | 71876.0 | 48507.0 | -23369.0 | capped at 99th pct |
| EF-C-0001076 | 71876.0 | 64732.0 | -7144.0 | capped at 99th pct |
| EF-C-0001077 | 50985.0 | 21372.0 | -29613.0 | capped at 99th pct |
| EF-C-0001077 | 50985.0 | 93333.0 | 42348.0 | adjusted (other) |
| EF-C-0001077 | 21372.0 | 50985.0 | 29613.0 | adjusted (other) |
| EF-C-0001077 | 21372.0 | 93333.0 | 71961.0 | adjusted (other) |
| EF-C-0001077 | 93333.0 | 50985.0 | -42348.0 | capped at 99th pct |
| EF-C-0001077 | 93333.0 | 21372.0 | -71961.0 | capped at 99th pct |
| EF-C-0001078 | 33863.0 | 169058.0 | 135195.0 | adjusted (other) |
| EF-C-0001078 | 33863.0 | 70610.0 | 36747.0 | adjusted (other) |
| EF-C-0001078 | 169058.0 | 33863.0 | -135195.0 | capped at 99th pct |
| EF-C-0001078 | 169058.0 | 70610.0 | -98448.0 | capped at 99th pct |
| EF-C-0001078 | 70610.0 | 33863.0 | -36747.0 | capped at 99th pct |
| EF-C-0001078 | 70610.0 | 169058.0 | 98448.0 | adjusted (other) |
| EF-C-0001080 | 91588.0 | 47935.0 | -43653.0 | capped at 99th pct |
| EF-C-0001080 | 47935.0 | 91588.0 | 43653.0 | adjusted (other) |
| EF-C-0001081 | 358539.0 | 112194.0 | -246345.0 | capped at 99th pct |
| EF-C-0001082 | 72170.0 | 159948.0 | 87778.0 | adjusted (other) |
| EF-C-0001082 | 159948.0 | 72170.0 | -87778.0 | capped at 99th pct |
| EF-C-0001083 | 90942.0 | 105066.0 | 14124.0 | adjusted (other) |
| EF-C-0001083 | 105066.0 | 90942.0 | -14124.0 | capped at 99th pct |
| EF-C-0001098 | 32066.0 | 50253.0 | 18187.0 | adjusted (other) |
| EF-C-0001098 | 50253.0 | 32066.0 | -18187.0 | capped at 99th pct |
| EF-C-0001099 | 79434.0 | 36372.0 | -43062.0 | capped at 99th pct |
| EF-C-0001099 | 36372.0 | 79434.0 | 43062.0 | adjusted (other) |
| EF-C-0001111 | 106938.0 | 84717.0 | -22221.0 | capped at 99th pct |
| EF-C-0001111 | 84717.0 | 106938.0 | 22221.0 | adjusted (other) |
| EF-C-0001112 | 128438.0 | 89931.0 | -38507.0 | capped at 99th pct |
| EF-C-0001112 | 89931.0 | 128438.0 | 38507.0 | adjusted (other) |
| EF-C-0001129 | 99848.0 | 44135.0 | -55713.0 | capped at 99th pct |
| EF-C-0001129 | 44135.0 | 99848.0 | 55713.0 | adjusted (other) |
| EF-C-0001130 | 31033.0 | 84761.0 | 53728.0 | adjusted (other) |
| EF-C-0001130 | 84761.0 | 31033.0 | -53728.0 | capped at 99th pct |
| EF-C-0001154 | 54530.0 | 118440.0 | 63910.0 | adjusted (other) |
| EF-C-0001154 | 118440.0 | 54530.0 | -63910.0 | capped at 99th pct |
| EF-C-0001155 | 62473.0 | 70879.0 | 8406.0 | adjusted (other) |
| EF-C-0001155 | 70879.0 | 62473.0 | -8406.0 | capped at 99th pct |
| EF-C-0001162 | 65885.0 | 77998.0 | 12113.0 | adjusted (other) |
| EF-C-0001162 | 77998.0 | 65885.0 | -12113.0 | capped at 99th pct |
| EF-C-0001163 | 146341.0 | 94593.0 | -51748.0 | capped at 99th pct |
| EF-C-0001163 | 94593.0 | 146341.0 | 51748.0 | adjusted (other) |
| EF-C-0001182 | 27991.0 | 17740.0 | -10251.0 | capped at 99th pct |
| EF-C-0001182 | 17740.0 | 27991.0 | 10251.0 | adjusted (other) |
| EF-C-0001183 | 41054.0 | 33715.0 | -7339.0 | capped at 99th pct |
| EF-C-0001183 | 33715.0 | 41054.0 | 7339.0 | adjusted (other) |
| EF-C-0001201 | 137871.0 | 160725.0 | 22854.0 | adjusted (other) |
| EF-C-0001201 | 160725.0 | 137871.0 | -22854.0 | capped at 99th pct |
| EF-C-0001202 | 104290.0 | 181444.0 | 77154.0 | adjusted (other) |
| EF-C-0001202 | 181444.0 | 104290.0 | -77154.0 | capped at 99th pct |
| EF-C-0001206 | 33552.0 | 205666.0 | 172114.0 | adjusted (other) |
| EF-C-0001206 | 205666.0 | 33552.0 | -172114.0 | capped at 99th pct |
| EF-C-0001207 | 21836.0 | 106092.0 | 84256.0 | adjusted (other) |
| EF-C-0001207 | 106092.0 | 21836.0 | -84256.0 | capped at 99th pct |
| EF-C-0001232 | 38560.0 | 36344.0 | -2216.0 | capped at 99th pct |
| EF-C-0001232 | 36344.0 | 38560.0 | 2216.0 | adjusted (other) |
| EF-C-0001233 | 50422.0 | 80339.0 | 29917.0 | adjusted (other) |
| EF-C-0001233 | 80339.0 | 50422.0 | -29917.0 | capped at 99th pct |
| EF-C-0001260 | 33290.0 | 23902.0 | -9388.0 | capped at 99th pct |
| EF-C-0001260 | 23902.0 | 33290.0 | 9388.0 | adjusted (other) |
| EF-C-0001261 | 18423.0 | 50761.0 | 32338.0 | adjusted (other) |
| EF-C-0001261 | 50761.0 | 18423.0 | -32338.0 | capped at 99th pct |
| EF-C-0001326 | 47937.0 | 67657.0 | 19720.0 | adjusted (other) |
| EF-C-0001326 | 67657.0 | 47937.0 | -19720.0 | capped at 99th pct |
| EF-C-0001327 | 49822.0 | 40500.0 | -9322.0 | capped at 99th pct |
| EF-C-0001327 | 40500.0 | 49822.0 | 9322.0 | adjusted (other) |
| EF-C-0001331 | 63430.0 | 50490.0 | -12940.0 | capped at 99th pct |
| EF-C-0001331 | 50490.0 | 63430.0 | 12940.0 | adjusted (other) |
| EF-C-0001332 | 35009.0 | 64081.0 | 29072.0 | adjusted (other) |
| EF-C-0001332 | 64081.0 | 35009.0 | -29072.0 | capped at 99th pct |
| EF-C-0001348 | 90689.0 | 46824.0 | -43865.0 | capped at 99th pct |
| EF-C-0001348 | 46824.0 | 90689.0 | 43865.0 | adjusted (other) |
| EF-C-0001349 | 39074.0 | 105329.0 | 66255.0 | adjusted (other) |
| EF-C-0001349 | 105329.0 | 39074.0 | -66255.0 | capped at 99th pct |
| EF-C-0001367 | 44189.0 | 49305.0 | 5116.0 | adjusted (other) |
| EF-C-0001367 | 49305.0 | 44189.0 | -5116.0 | capped at 99th pct |
| EF-C-0001368 | 145363.0 | 116310.0 | -29053.0 | capped at 99th pct |
| EF-C-0001368 | 116310.0 | 145363.0 | 29053.0 | adjusted (other) |
| EF-C-0001369 | 33481.0 | 113218.0 | 79737.0 | adjusted (other) |
| EF-C-0001369 | 113218.0 | 33481.0 | -79737.0 | capped at 99th pct |
| EF-C-0001370 | 30752.0 | 18716.0 | -12036.0 | capped at 99th pct |
| EF-C-0001370 | 18716.0 | 30752.0 | 12036.0 | adjusted (other) |
| EF-C-0001375 | 36283.0 | 73389.0 | 37106.0 | adjusted (other) |
| EF-C-0001375 | 73389.0 | 36283.0 | -37106.0 | capped at 99th pct |
| EF-C-0001376 | 155339.0 | 130318.0 | -25021.0 | capped at 99th pct |
| EF-C-0001376 | 130318.0 | 155339.0 | 25021.0 | adjusted (other) |
| EF-C-0001377 | 116657.0 | 67658.0 | -48999.0 | capped at 99th pct |
| EF-C-0001377 | 67658.0 | 116657.0 | 48999.0 | adjusted (other) |
| EF-C-0001383 | 42199.0 | 77635.0 | 35436.0 | adjusted (other) |
| EF-C-0001383 | 77635.0 | 42199.0 | -35436.0 | capped at 99th pct |
| EF-C-0001384 | 151005.0 | 71088.0 | -79917.0 | capped at 99th pct |
| EF-C-0001384 | 71088.0 | 151005.0 | 79917.0 | adjusted (other) |
| EF-C-0001404 | 22280.0 | 14676.0 | -7604.0 | capped at 99th pct |
| EF-C-0001404 | 14676.0 | 22280.0 | 7604.0 | adjusted (other) |
| EF-C-0001405 | 31103.0 | 16087.0 | -15016.0 | capped at 99th pct |
| EF-C-0001405 | 16087.0 | 31103.0 | 15016.0 | adjusted (other) |
| EF-C-0001410 | 59261.0 | 45054.0 | -14207.0 | capped at 99th pct |
| EF-C-0001410 | 45054.0 | 59261.0 | 14207.0 | adjusted (other) |
| EF-C-0001411 | 55371.0 | 273392.0 | 218021.0 | adjusted (other) |
| EF-C-0001411 | 273392.0 | 55371.0 | -218021.0 | capped at 99th pct |
| EF-C-0001419 | 71108.0 | 79011.0 | 7903.0 | adjusted (other) |
| EF-C-0001419 | 79011.0 | 71108.0 | -7903.0 | capped at 99th pct |
| EF-C-0001420 | 148092.0 | 173502.0 | 25410.0 | adjusted (other) |
| EF-C-0001420 | 173502.0 | 148092.0 | -25410.0 | capped at 99th pct |
| EF-C-0001479 | 107422.0 | 69510.0 | -37912.0 | capped at 99th pct |
| EF-C-0001479 | 69510.0 | 107422.0 | 37912.0 | adjusted (other) |
| EF-C-0001497 | 30329.0 | 173409.0 | 143080.0 | adjusted (other) |
| EF-C-0001497 | 173409.0 | 30329.0 | -143080.0 | capped at 99th pct |
| EF-C-0001498 | 94637.0 | 119796.0 | 25159.0 | adjusted (other) |
| EF-C-0001498 | 119796.0 | 94637.0 | -25159.0 | capped at 99th pct |
| EF-C-0001533 | 92045.0 | 44686.0 | -47359.0 | capped at 99th pct |
| EF-C-0001533 | 44686.0 | 92045.0 | 47359.0 | adjusted (other) |
| EF-C-0001534 | 99765.0 | 95248.0 | -4517.0 | capped at 99th pct |
| EF-C-0001534 | 95248.0 | 99765.0 | 4517.0 | adjusted (other) |
| EF-C-0001550 | 61942.0 | 53159.0 | -8783.0 | capped at 99th pct |
| EF-C-0001550 | 53159.0 | 61942.0 | 8783.0 | adjusted (other) |
| EF-C-0001551 | 85887.0 | 84959.0 | -928.0 | capped at 99th pct |
| EF-C-0001551 | 84959.0 | 85887.0 | 928.0 | adjusted (other) |
| EF-C-0001564 | 110275.0 | 81440.0 | -28835.0 | capped at 99th pct |
| EF-C-0001564 | 81440.0 | 110275.0 | 28835.0 | adjusted (other) |
| EF-C-0001565 | 94252.0 | 102635.0 | 8383.0 | adjusted (other) |
| EF-C-0001565 | 102635.0 | 94252.0 | -8383.0 | capped at 99th pct |
| EF-C-0001577 | 75625.0 | 105251.0 | 29626.0 | adjusted (other) |
| EF-C-0001577 | 105251.0 | 75625.0 | -29626.0 | capped at 99th pct |
| EF-C-0001578 | 89874.0 | 64352.0 | -25522.0 | capped at 99th pct |
| EF-C-0001578 | 64352.0 | 89874.0 | 25522.0 | adjusted (other) |
| EF-C-0001580 | 62351.0 | 21414.0 | -40937.0 | capped at 99th pct |
| EF-C-0001580 | 21414.0 | 62351.0 | 40937.0 | adjusted (other) |
| EF-C-0001581 | 79995.0 | 22353.0 | -57642.0 | capped at 99th pct |
| EF-C-0001581 | 22353.0 | 79995.0 | 57642.0 | adjusted (other) |
| EF-C-0001591 | 95774.0 | 99502.0 | 3728.0 | adjusted (other) |
| EF-C-0001591 | 99502.0 | 95774.0 | -3728.0 | capped at 99th pct |
| EF-C-0001592 | 95481.0 | 89830.0 | -5651.0 | capped at 99th pct |
| EF-C-0001592 | 89830.0 | 95481.0 | 5651.0 | adjusted (other) |
| EF-C-0001670 | 167856.0 | 161981.0 | -5875.0 | capped at 99th pct |
| EF-C-0001670 | 161981.0 | 167856.0 | 5875.0 | adjusted (other) |
| EF-C-0001671 | 87085.0 | 84237.0 | -2848.0 | capped at 99th pct |
| EF-C-0001671 | 84237.0 | 87085.0 | 2848.0 | adjusted (other) |
| EF-C-0001672 | 71685.0 | 108884.0 | 37199.0 | adjusted (other) |
| EF-C-0001672 | 108884.0 | 71685.0 | -37199.0 | capped at 99th pct |
| EF-C-0001673 | 64114.0 | 96866.0 | 32752.0 | adjusted (other) |
| EF-C-0001673 | 96866.0 | 64114.0 | -32752.0 | capped at 99th pct |
| EF-C-0001676 | 102081.0 | 187045.0 | 84964.0 | adjusted (other) |
| EF-C-0001676 | 187045.0 | 102081.0 | -84964.0 | capped at 99th pct |
| EF-C-0001677 | 111511.0 | 67816.0 | -43695.0 | capped at 99th pct |
| EF-C-0001677 | 67816.0 | 111511.0 | 43695.0 | adjusted (other) |
| EF-C-0001683 | 62064.0 | 173959.0 | 111895.0 | adjusted (other) |
| EF-C-0001683 | 173959.0 | 62064.0 | -111895.0 | capped at 99th pct |
| EF-C-0001684 | 68493.0 | 120575.0 | 52082.0 | adjusted (other) |
| EF-C-0001684 | 120575.0 | 68493.0 | -52082.0 | capped at 99th pct |
| EF-C-0001687 | 215408.0 | 164628.0 | -50780.0 | capped at 99th pct |
| EF-C-0001687 | 164628.0 | 215408.0 | 50780.0 | adjusted (other) |
| EF-C-0001688 | 52299.0 | 174057.0 | 121758.0 | adjusted (other) |
| EF-C-0001688 | 174057.0 | 52299.0 | -121758.0 | capped at 99th pct |
| EF-C-0001701 | 59603.0 | 43271.0 | -16332.0 | capped at 99th pct |
| EF-C-0001701 | 43271.0 | 59603.0 | 16332.0 | adjusted (other) |
| EF-C-0001702 | 44902.0 | 19433.0 | -25469.0 | capped at 99th pct |
| EF-C-0001702 | 19433.0 | 44902.0 | 25469.0 | adjusted (other) |
| EF-C-0001726 | 20496.0 | 48547.0 | 28051.0 | adjusted (other) |
| EF-C-0001726 | 48547.0 | 20496.0 | -28051.0 | capped at 99th pct |
| EF-C-0001727 | 44741.0 | 9183.0 | -35558.0 | capped at 99th pct |
| EF-C-0001727 | 9183.0 | 44741.0 | 35558.0 | adjusted (other) |
| EF-C-0001737 | 42270.0 | 283214.0 | 240944.0 | adjusted (other) |
| EF-C-0001737 | 283214.0 | 42270.0 | -240944.0 | capped at 99th pct |
| EF-C-0001738 | 54360.0 | 26690.0 | -27670.0 | capped at 99th pct |
| EF-C-0001738 | 26690.0 | 54360.0 | 27670.0 | adjusted (other) |
| EF-C-0001794 | 48698.0 | 25185.0 | -23513.0 | capped at 99th pct |
| EF-C-0001794 | 25185.0 | 48698.0 | 23513.0 | adjusted (other) |
| EF-C-0001795 | 49417.0 | 56213.0 | 6796.0 | adjusted (other) |
| EF-C-0001795 | 56213.0 | 49417.0 | -6796.0 | capped at 99th pct |
| EF-C-0001799 | 82769.0 | 104520.0 | 21751.0 | adjusted (other) |
| EF-C-0001799 | 104520.0 | 82769.0 | -21751.0 | capped at 99th pct |
| EF-C-0001800 | 84137.0 | 56354.0 | -27783.0 | capped at 99th pct |
| EF-C-0001800 | 56354.0 | 84137.0 | 27783.0 | adjusted (other) |
| EF-C-0001821 | 71853.0 | 58054.0 | -13799.0 | capped at 99th pct |
| EF-C-0001821 | 58054.0 | 71853.0 | 13799.0 | adjusted (other) |
| EF-C-0001822 | 167654.0 | 80504.0 | -87150.0 | capped at 99th pct |
| EF-C-0001822 | 80504.0 | 167654.0 | 87150.0 | adjusted (other) |
| EF-C-0001837 | 123068.0 | 76779.0 | -46289.0 | capped at 99th pct |
| EF-C-0001837 | 76779.0 | 123068.0 | 46289.0 | adjusted (other) |
| EF-C-0001838 | 163769.0 | 80347.0 | -83422.0 | capped at 99th pct |
| EF-C-0001838 | 80347.0 | 163769.0 | 83422.0 | adjusted (other) |
| EF-C-0001840 | 223376.0 | 76020.0 | -147356.0 | capped at 99th pct |
| EF-C-0001840 | 76020.0 | 223376.0 | 147356.0 | adjusted (other) |
| EF-C-0001841 | 92880.0 | 79567.0 | -13313.0 | capped at 99th pct |
| EF-C-0001841 | 79567.0 | 92880.0 | 13313.0 | adjusted (other) |
| EF-C-0001851 | 68602.0 | 93074.0 | 24472.0 | adjusted (other) |
| EF-C-0001851 | 93074.0 | 68602.0 | -24472.0 | capped at 99th pct |
| EF-C-0001860 | 41996.0 | 74074.0 | 32078.0 | adjusted (other) |
| EF-C-0001860 | 74074.0 | 41996.0 | -32078.0 | capped at 99th pct |
| EF-C-0001861 | 46874.0 | 37119.0 | -9755.0 | capped at 99th pct |
| EF-C-0001861 | 37119.0 | 46874.0 | 9755.0 | adjusted (other) |
| EF-C-0001865 | 46309.0 | 44492.0 | -1817.0 | capped at 99th pct |
| EF-C-0001865 | 44492.0 | 46309.0 | 1817.0 | adjusted (other) |
| EF-C-0001866 | 153794.0 | 199031.0 | 45237.0 | adjusted (other) |
| EF-C-0001866 | 199031.0 | 153794.0 | -45237.0 | capped at 99th pct |
| EF-C-0001872 | 109761.0 | 84623.0 | -25138.0 | capped at 99th pct |
| EF-C-0001872 | 84623.0 | 109761.0 | 25138.0 | adjusted (other) |
| EF-C-0001873 | 53072.0 | 89106.0 | 36034.0 | adjusted (other) |
| EF-C-0001873 | 89106.0 | 53072.0 | -36034.0 | capped at 99th pct |
| EF-C-0001874 | 49529.0 | 44659.0 | -4870.0 | capped at 99th pct |
| EF-C-0001874 | 44659.0 | 49529.0 | 4870.0 | adjusted (other) |
| EF-C-0001875 | 61534.0 | 47263.0 | -14271.0 | capped at 99th pct |
| EF-C-0001875 | 47263.0 | 61534.0 | 14271.0 | adjusted (other) |
| EF-C-0001889 | 36857.0 | 30656.0 | -6201.0 | capped at 99th pct |
| EF-C-0001889 | 30656.0 | 36857.0 | 6201.0 | adjusted (other) |
| EF-C-0001890 | 41415.0 | 36023.0 | -5392.0 | capped at 99th pct |
| EF-C-0001890 | 36023.0 | 41415.0 | 5392.0 | adjusted (other) |
| EF-C-0001953 | 101649.0 | 108587.0 | 6938.0 | adjusted (other) |
| EF-C-0001953 | 108587.0 | 101649.0 | -6938.0 | capped at 99th pct |
| EF-C-0001954 | 106946.0 | 53104.0 | -53842.0 | capped at 99th pct |
| EF-C-0001954 | 53104.0 | 106946.0 | 53842.0 | adjusted (other) |
| EF-C-0001967 | 25279.0 | 38132.0 | 12853.0 | adjusted (other) |
| EF-C-0001967 | 38132.0 | 25279.0 | -12853.0 | capped at 99th pct |
| EF-C-0001968 | 42102.0 | 33381.0 | -8721.0 | capped at 99th pct |
| EF-C-0001968 | 33381.0 | 42102.0 | 8721.0 | adjusted (other) |
| EF-C-0001983 | 29176.0 | 52276.0 | 23100.0 | adjusted (other) |
| EF-C-0001983 | 52276.0 | 29176.0 | -23100.0 | capped at 99th pct |
| EF-C-0001984 | 47370.0 | 17314.0 | -30056.0 | capped at 99th pct |
| EF-C-0001984 | 17314.0 | 47370.0 | 30056.0 | adjusted (other) |
| EF-C-0001987 | 74394.0 | 43344.0 | -31050.0 | capped at 99th pct |
| EF-C-0001987 | 43344.0 | 74394.0 | 31050.0 | adjusted (other) |
| EF-C-0001988 | 46747.0 | 161261.0 | 114514.0 | adjusted (other) |
| EF-C-0001988 | 161261.0 | 46747.0 | -114514.0 | capped at 99th pct |
| EF-C-0001997 | 57959.0 | 33995.0 | -23964.0 | capped at 99th pct |
| EF-C-0001997 | 57959.0 | 42232.0 | -15727.0 | capped at 99th pct |
| EF-C-0001997 | 33995.0 | 57959.0 | 23964.0 | adjusted (other) |
| EF-C-0001997 | 33995.0 | 42232.0 | 8237.0 | adjusted (other) |
| EF-C-0001997 | 42232.0 | 57959.0 | 15727.0 | adjusted (other) |
| EF-C-0001997 | 42232.0 | 33995.0 | -8237.0 | capped at 99th pct |
| EF-C-0001998 | 88830.0 | 41496.0 | -47334.0 | capped at 99th pct |
| EF-C-0001998 | 88830.0 | 22436.0 | -66394.0 | capped at 99th pct |
| EF-C-0001998 | 41496.0 | 88830.0 | 47334.0 | adjusted (other) |
| EF-C-0001998 | 41496.0 | 22436.0 | -19060.0 | capped at 99th pct |
| EF-C-0001998 | 22436.0 | 88830.0 | 66394.0 | adjusted (other) |
| EF-C-0001998 | 22436.0 | 41496.0 | 19060.0 | adjusted (other) |
| EF-C-0001999 | 70729.0 | 32492.0 | -38237.0 | capped at 99th pct |
| EF-C-0001999 | 70729.0 | 107738.0 | 37009.0 | adjusted (other) |
| EF-C-0001999 | 32492.0 | 70729.0 | 38237.0 | adjusted (other) |
| EF-C-0001999 | 32492.0 | 107738.0 | 75246.0 | adjusted (other) |
| EF-C-0001999 | 107738.0 | 70729.0 | -37009.0 | capped at 99th pct |
| EF-C-0001999 | 107738.0 | 32492.0 | -75246.0 | capped at 99th pct |
| EF-C-0002045 | 116855.0 | 114071.0 | -2784.0 | capped at 99th pct |
| EF-C-0002045 | 114071.0 | 116855.0 | 2784.0 | adjusted (other) |
| EF-C-0002046 | 127906.0 | 137925.0 | 10019.0 | adjusted (other) |
| EF-C-0002046 | 137925.0 | 127906.0 | -10019.0 | capped at 99th pct |
| EF-C-0002099 | 82177.0 | 27147.0 | -55030.0 | capped at 99th pct |
| EF-C-0002099 | 27147.0 | 82177.0 | 55030.0 | adjusted (other) |
| EF-C-0002100 | 92012.0 | 30583.0 | -61429.0 | capped at 99th pct |
| EF-C-0002100 | 30583.0 | 92012.0 | 61429.0 | adjusted (other) |
| EF-C-0002105 | 130854.0 | 122679.0 | -8175.0 | capped at 99th pct |
| EF-C-0002105 | 122679.0 | 130854.0 | 8175.0 | adjusted (other) |
| EF-C-0002106 | 134142.0 | 225658.0 | 91516.0 | adjusted (other) |
| EF-C-0002106 | 225658.0 | 134142.0 | -91516.0 | capped at 99th pct |
| EF-C-0002117 | 79444.0 | 87629.0 | 8185.0 | adjusted (other) |
| EF-C-0002117 | 87629.0 | 79444.0 | -8185.0 | capped at 99th pct |
| EF-C-0002118 | 76282.0 | 109267.0 | 32985.0 | adjusted (other) |
| EF-C-0002118 | 109267.0 | 76282.0 | -32985.0 | capped at 99th pct |
| EF-C-0002126 | 49753.0 | 27333.0 | -22420.0 | capped at 99th pct |
| EF-C-0002126 | 27333.0 | 49753.0 | 22420.0 | adjusted (other) |
| EF-C-0002127 | 72751.0 | 54886.0 | -17865.0 | capped at 99th pct |
| EF-C-0002127 | 54886.0 | 72751.0 | 17865.0 | adjusted (other) |
| EF-C-0002154 | 59978.0 | 31659.0 | -28319.0 | capped at 99th pct |
| EF-C-0002154 | 31659.0 | 59978.0 | 28319.0 | adjusted (other) |
| EF-C-0002155 | 88996.0 | 48885.0 | -40111.0 | capped at 99th pct |
| EF-C-0002155 | 48885.0 | 88996.0 | 40111.0 | adjusted (other) |
| EF-C-0002203 | 269610.0 | 150154.0 | -119456.0 | capped at 99th pct |
| EF-C-0002203 | 150154.0 | 269610.0 | 119456.0 | adjusted (other) |
| EF-C-0002204 | 199391.0 | 99173.0 | -100218.0 | capped at 99th pct |
| EF-C-0002204 | 99173.0 | 199391.0 | 100218.0 | adjusted (other) |
| EF-C-0002246 | 123532.0 | 115413.0 | -8119.0 | capped at 99th pct |
| EF-C-0002246 | 115413.0 | 123532.0 | 8119.0 | adjusted (other) |
| EF-C-0002247 | 168401.0 | 48399.0 | -120002.0 | capped at 99th pct |
| EF-C-0002247 | 48399.0 | 168401.0 | 120002.0 | adjusted (other) |
| EF-C-0002293 | 94605.0 | 104793.0 | 10188.0 | adjusted (other) |
| EF-C-0002293 | 94605.0 | 68577.0 | -26028.0 | capped at 99th pct |
| EF-C-0002293 | 104793.0 | 94605.0 | -10188.0 | capped at 99th pct |
| EF-C-0002293 | 104793.0 | 68577.0 | -36216.0 | capped at 99th pct |
| EF-C-0002293 | 68577.0 | 94605.0 | 26028.0 | adjusted (other) |
| EF-C-0002293 | 68577.0 | 104793.0 | 36216.0 | adjusted (other) |
| EF-C-0002294 | 141684.0 | 79320.0 | -62364.0 | capped at 99th pct |
| EF-C-0002294 | 141684.0 | 97701.0 | -43983.0 | capped at 99th pct |
| EF-C-0002294 | 79320.0 | 141684.0 | 62364.0 | adjusted (other) |
| EF-C-0002294 | 79320.0 | 97701.0 | 18381.0 | adjusted (other) |
| EF-C-0002294 | 97701.0 | 141684.0 | 43983.0 | adjusted (other) |
| EF-C-0002294 | 97701.0 | 79320.0 | -18381.0 | capped at 99th pct |
| EF-C-0002295 | 91788.0 | 46585.0 | -45203.0 | capped at 99th pct |
| EF-C-0002295 | 91788.0 | 94333.0 | 2545.0 | adjusted (other) |
| EF-C-0002295 | 46585.0 | 91788.0 | 45203.0 | adjusted (other) |
| EF-C-0002295 | 46585.0 | 94333.0 | 47748.0 | adjusted (other) |
| EF-C-0002295 | 94333.0 | 91788.0 | -2545.0 | capped at 99th pct |
| EF-C-0002295 | 94333.0 | 46585.0 | -47748.0 | capped at 99th pct |
| EF-C-0002315 | 49302.0 | 36674.0 | -12628.0 | capped at 99th pct |
| EF-C-0002315 | 36674.0 | 49302.0 | 12628.0 | adjusted (other) |
| EF-C-0002316 | 34432.0 | 75114.0 | 40682.0 | adjusted (other) |
| EF-C-0002316 | 75114.0 | 34432.0 | -40682.0 | capped at 99th pct |
| EF-C-0002320 | 103810.0 | 78036.0 | -25774.0 | capped at 99th pct |
| EF-C-0002320 | 78036.0 | 103810.0 | 25774.0 | adjusted (other) |
| EF-C-0002321 | 90954.0 | 40934.0 | -50020.0 | capped at 99th pct |
| EF-C-0002321 | 40934.0 | 90954.0 | 50020.0 | adjusted (other) |
| EF-C-0002399 | 73552.0 | 80792.0 | 7240.0 | adjusted (other) |
| EF-C-0002399 | 80792.0 | 73552.0 | -7240.0 | capped at 99th pct |
| EF-C-0002400 | 70232.0 | 49062.0 | -21170.0 | capped at 99th pct |
| EF-C-0002400 | 49062.0 | 70232.0 | 21170.0 | adjusted (other) |
| EF-C-0002424 | 289018.0 | 155731.0 | -133287.0 | capped at 99th pct |
| EF-C-0002424 | 155731.0 | 289018.0 | 133287.0 | adjusted (other) |
| EF-C-0002425 | 156997.0 | 151949.0 | -5048.0 | capped at 99th pct |
| EF-C-0002425 | 151949.0 | 156997.0 | 5048.0 | adjusted (other) |
| EF-C-0002433 | 123876.0 | 100952.0 | -22924.0 | capped at 99th pct |
| EF-C-0002433 | 100952.0 | 123876.0 | 22924.0 | adjusted (other) |
| EF-C-0002434 | 27639.0 | 62876.0 | 35237.0 | adjusted (other) |
| EF-C-0002434 | 62876.0 | 27639.0 | -35237.0 | capped at 99th pct |
| EF-C-0002446 | 211894.0 | 78673.0 | -133221.0 | capped at 99th pct |
| EF-C-0002446 | 78673.0 | 211894.0 | 133221.0 | adjusted (other) |
| EF-C-0002447 | 125416.0 | 69635.0 | -55781.0 | capped at 99th pct |
| EF-C-0002447 | 69635.0 | 125416.0 | 55781.0 | adjusted (other) |
| EF-C-0002464 | 144988.0 | 30216.0 | -114772.0 | capped at 99th pct |
| EF-C-0002464 | 30216.0 | 144988.0 | 114772.0 | adjusted (other) |
| EF-C-0002465 | 77707.0 | 94122.0 | 16415.0 | adjusted (other) |
| EF-C-0002465 | 94122.0 | 77707.0 | -16415.0 | capped at 99th pct |
| EF-C-0002493 | 49306.0 | 52787.0 | 3481.0 | adjusted (other) |
| EF-C-0002493 | 52787.0 | 49306.0 | -3481.0 | capped at 99th pct |
| EF-C-0002494 | 114408.0 | 45966.0 | -68442.0 | capped at 99th pct |
| EF-C-0002494 | 45966.0 | 114408.0 | 68442.0 | adjusted (other) |
| EF-C-0002499 | 74080.0 | 55751.0 | -18329.0 | capped at 99th pct |
| EF-C-0002499 | 55751.0 | 74080.0 | 18329.0 | adjusted (other) |
| EF-C-0002500 | 118610.0 | 134483.0 | 15873.0 | adjusted (other) |
| EF-C-0002500 | 134483.0 | 118610.0 | -15873.0 | capped at 99th pct |
| EF-C-0002513 | 205422.0 | 83296.0 | -122126.0 | capped at 99th pct |
| EF-C-0002513 | 83296.0 | 205422.0 | 122126.0 | adjusted (other) |
| EF-C-0002514 | 64752.0 | 105737.0 | 40985.0 | adjusted (other) |
| EF-C-0002514 | 105737.0 | 64752.0 | -40985.0 | capped at 99th pct |
| EF-C-0002531 | 79950.0 | 158841.0 | 78891.0 | adjusted (other) |
| EF-C-0002531 | 158841.0 | 79950.0 | -78891.0 | capped at 99th pct |
| EF-C-0002532 | 40935.0 | 52022.0 | 11087.0 | adjusted (other) |
| EF-C-0002532 | 52022.0 | 40935.0 | -11087.0 | capped at 99th pct |
| EF-C-0002549 | 112375.0 | 95947.0 | -16428.0 | capped at 99th pct |
| EF-C-0002549 | 95947.0 | 112375.0 | 16428.0 | adjusted (other) |
| EF-C-0002550 | 63720.0 | 80305.0 | 16585.0 | adjusted (other) |
| EF-C-0002550 | 80305.0 | 63720.0 | -16585.0 | capped at 99th pct |
| EF-C-0002552 | 30869.0 | 117731.0 | 86862.0 | adjusted (other) |
| EF-C-0002552 | 117731.0 | 30869.0 | -86862.0 | capped at 99th pct |
| EF-C-0002553 | 83078.0 | 46358.0 | -36720.0 | capped at 99th pct |
| EF-C-0002553 | 46358.0 | 83078.0 | 36720.0 | adjusted (other) |
| EF-C-0002557 | 51540.0 | 55487.0 | 3947.0 | adjusted (other) |
| EF-C-0002557 | 55487.0 | 51540.0 | -3947.0 | capped at 99th pct |
| EF-C-0002558 | 59765.0 | 71131.0 | 11366.0 | adjusted (other) |
| EF-C-0002558 | 71131.0 | 59765.0 | -11366.0 | capped at 99th pct |
| EF-C-0002605 | 42555.0 | 33994.0 | -8561.0 | capped at 99th pct |
| EF-C-0002605 | 33994.0 | 42555.0 | 8561.0 | adjusted (other) |
| EF-C-0002606 | 73733.0 | 25789.0 | -47944.0 | capped at 99th pct |
| EF-C-0002606 | 25789.0 | 73733.0 | 47944.0 | adjusted (other) |
| EF-C-0002608 | 53315.0 | 45847.0 | -7468.0 | capped at 99th pct |
| EF-C-0002608 | 45847.0 | 53315.0 | 7468.0 | adjusted (other) |
| EF-C-0002609 | 38493.0 | 54032.0 | 15539.0 | adjusted (other) |
| EF-C-0002609 | 54032.0 | 38493.0 | -15539.0 | capped at 99th pct |
| EF-C-0002630 | 117214.0 | 107281.0 | -9933.0 | capped at 99th pct |
| EF-C-0002630 | 107281.0 | 117214.0 | 9933.0 | adjusted (other) |
| EF-C-0002631 | 65020.0 | 47897.0 | -17123.0 | capped at 99th pct |
| EF-C-0002631 | 47897.0 | 65020.0 | 17123.0 | adjusted (other) |
| EF-C-0002642 | 86422.0 | 183691.0 | 97269.0 | adjusted (other) |
| EF-C-0002642 | 183691.0 | 86422.0 | -97269.0 | capped at 99th pct |
| EF-C-0002643 | 129916.0 | 85866.0 | -44050.0 | capped at 99th pct |
| EF-C-0002643 | 85866.0 | 129916.0 | 44050.0 | adjusted (other) |
| EF-C-0002655 | 134821.0 | 152203.0 | 17382.0 | adjusted (other) |
| EF-C-0002655 | 152203.0 | 134821.0 | -17382.0 | capped at 99th pct |
| EF-C-0002656 | 118891.0 | 64631.0 | -54260.0 | capped at 99th pct |
| EF-C-0002656 | 64631.0 | 118891.0 | 54260.0 | adjusted (other) |
| EF-C-0002660 | 52212.0 | 12800.0 | -39412.0 | capped at 99th pct |
| EF-C-0002660 | 12800.0 | 52212.0 | 39412.0 | adjusted (other) |
| EF-C-0002661 | 32119.0 | 32423.0 | 304.0 | adjusted (other) |
| EF-C-0002661 | 32423.0 | 32119.0 | -304.0 | capped at 99th pct |
| EF-C-0002739 | 104022.0 | 38478.0 | -65544.0 | capped at 99th pct |
| EF-C-0002739 | 38478.0 | 104022.0 | 65544.0 | adjusted (other) |
| EF-C-0002740 | 41057.0 | 48723.0 | 7666.0 | adjusted (other) |
| EF-C-0002740 | 48723.0 | 41057.0 | -7666.0 | capped at 99th pct |
| EF-C-0002764 | 78874.0 | 68374.0 | -10500.0 | capped at 99th pct |
| EF-C-0002764 | 68374.0 | 78874.0 | 10500.0 | adjusted (other) |
| EF-C-0002765 | 30348.0 | 113182.0 | 82834.0 | adjusted (other) |
| EF-C-0002765 | 113182.0 | 30348.0 | -82834.0 | capped at 99th pct |
| EF-C-0002782 | 168789.0 | 236783.0 | 67994.0 | adjusted (other) |
| EF-C-0002782 | 236783.0 | 168789.0 | -67994.0 | capped at 99th pct |
| EF-C-0002783 | 220727.0 | 210819.0 | -9908.0 | capped at 99th pct |
| EF-C-0002783 | 210819.0 | 220727.0 | 9908.0 | adjusted (other) |
| EF-C-0002784 | 41108.0 | 48685.0 | 7577.0 | adjusted (other) |
| EF-C-0002784 | 48685.0 | 41108.0 | -7577.0 | capped at 99th pct |
| EF-C-0002785 | 53540.0 | 135267.0 | 81727.0 | adjusted (other) |
| EF-C-0002785 | 135267.0 | 53540.0 | -81727.0 | capped at 99th pct |
| EF-C-0002844 | 41661.0 | 51983.0 | 10322.0 | adjusted (other) |
| EF-C-0002844 | 51983.0 | 41661.0 | -10322.0 | capped at 99th pct |
| EF-C-0002845 | 67221.0 | 27895.0 | -39326.0 | capped at 99th pct |
| EF-C-0002845 | 27895.0 | 67221.0 | 39326.0 | adjusted (other) |
| EF-C-0002849 | 142249.0 | 178849.0 | 36600.0 | adjusted (other) |
| EF-C-0002849 | 178849.0 | 142249.0 | -36600.0 | capped at 99th pct |
| EF-C-0002850 | 88161.0 | 59044.0 | -29117.0 | capped at 99th pct |
| EF-C-0002850 | 59044.0 | 88161.0 | 29117.0 | adjusted (other) |
| EF-C-0002939 | 59424.0 | 43853.0 | -15571.0 | capped at 99th pct |
| EF-C-0002939 | 43853.0 | 59424.0 | 15571.0 | adjusted (other) |
| EF-C-0002940 | 129558.0 | 90151.0 | -39407.0 | capped at 99th pct |
| EF-C-0002940 | 90151.0 | 129558.0 | 39407.0 | adjusted (other) |
| EF-C-0002946 | 37989.0 | 91181.0 | 53192.0 | adjusted (other) |
| EF-C-0002946 | 91181.0 | 37989.0 | -53192.0 | capped at 99th pct |
| EF-C-0002947 | 57584.0 | 31302.0 | -26282.0 | capped at 99th pct |
| EF-C-0002947 | 31302.0 | 57584.0 | 26282.0 | adjusted (other) |
| EF-C-0002951 | 185963.0 | 242023.0 | 56060.0 | adjusted (other) |
| EF-C-0002951 | 242023.0 | 185963.0 | -56060.0 | capped at 99th pct |
| EF-C-0002962 | 98284.0 | 84550.0 | -13734.0 | capped at 99th pct |
| EF-C-0002962 | 84550.0 | 98284.0 | 13734.0 | adjusted (other) |
| EF-C-0002963 | 112321.0 | 93435.0 | -18886.0 | capped at 99th pct |
| EF-C-0002963 | 93435.0 | 112321.0 | 18886.0 | adjusted (other) |
| EF-C-0003023 | 40703.0 | 23913.0 | -16790.0 | capped at 99th pct |
| EF-C-0003023 | 23913.0 | 40703.0 | 16790.0 | adjusted (other) |
| EF-C-0003024 | 50788.0 | 47140.0 | -3648.0 | capped at 99th pct |
| EF-C-0003024 | 47140.0 | 50788.0 | 3648.0 | adjusted (other) |
| EF-C-0003048 | 166362.0 | 78155.0 | -88207.0 | capped at 99th pct |
| EF-C-0003048 | 78155.0 | 166362.0 | 88207.0 | adjusted (other) |
| EF-C-0003049 | 73210.0 | 44523.0 | -28687.0 | capped at 99th pct |
| EF-C-0003049 | 44523.0 | 73210.0 | 28687.0 | adjusted (other) |
| EF-C-0003064 | 51872.0 | 32941.0 | -18931.0 | capped at 99th pct |
| EF-C-0003064 | 32941.0 | 51872.0 | 18931.0 | adjusted (other) |
| EF-C-0003065 | 39894.0 | 46604.0 | 6710.0 | adjusted (other) |
| EF-C-0003065 | 46604.0 | 39894.0 | -6710.0 | capped at 99th pct |
| EF-C-0003092 | 95156.0 | 68859.0 | -26297.0 | capped at 99th pct |
| EF-C-0003092 | 95156.0 | 190625.0 | 95469.0 | adjusted (other) |
| EF-C-0003092 | 68859.0 | 95156.0 | 26297.0 | adjusted (other) |
| EF-C-0003092 | 68859.0 | 190625.0 | 121766.0 | adjusted (other) |
| EF-C-0003092 | 190625.0 | 95156.0 | -95469.0 | capped at 99th pct |
| EF-C-0003092 | 190625.0 | 68859.0 | -121766.0 | capped at 99th pct |
| EF-C-0003093 | 89510.0 | 86591.0 | -2919.0 | capped at 99th pct |
| EF-C-0003093 | 89510.0 | 172927.0 | 83417.0 | adjusted (other) |
| EF-C-0003093 | 86591.0 | 89510.0 | 2919.0 | adjusted (other) |
| EF-C-0003093 | 86591.0 | 172927.0 | 86336.0 | adjusted (other) |
| EF-C-0003093 | 172927.0 | 89510.0 | -83417.0 | capped at 99th pct |
| EF-C-0003093 | 172927.0 | 86591.0 | -86336.0 | capped at 99th pct |
| EF-C-0003094 | 74694.0 | 88814.0 | 14120.0 | adjusted (other) |
| EF-C-0003094 | 74694.0 | 148432.0 | 73738.0 | adjusted (other) |
| EF-C-0003094 | 88814.0 | 74694.0 | -14120.0 | capped at 99th pct |
| EF-C-0003094 | 88814.0 | 148432.0 | 59618.0 | adjusted (other) |
| EF-C-0003094 | 148432.0 | 74694.0 | -73738.0 | capped at 99th pct |
| EF-C-0003094 | 148432.0 | 88814.0 | -59618.0 | capped at 99th pct |
| EF-C-0003097 | 258337.0 | 156003.0 | -102334.0 | capped at 99th pct |
| EF-C-0003097 | 156003.0 | 258337.0 | 102334.0 | adjusted (other) |
| EF-C-0003100 | 23915.0 | 148986.0 | 125071.0 | adjusted (other) |
| EF-C-0003100 | 148986.0 | 23915.0 | -125071.0 | capped at 99th pct |
| EF-C-0003101 | 35676.0 | 53365.0 | 17689.0 | adjusted (other) |
| EF-C-0003101 | 53365.0 | 35676.0 | -17689.0 | capped at 99th pct |
| EF-C-0003123 | 94087.0 | 205173.0 | 111086.0 | adjusted (other) |
| EF-C-0003123 | 205173.0 | 94087.0 | -111086.0 | capped at 99th pct |
| EF-C-0003124 | 31685.0 | 12035.0 | -19650.0 | capped at 99th pct |
| EF-C-0003124 | 12035.0 | 31685.0 | 19650.0 | adjusted (other) |
| EF-C-0003133 | 68925.0 | 45295.0 | -23630.0 | capped at 99th pct |
| EF-C-0003133 | 45295.0 | 68925.0 | 23630.0 | adjusted (other) |
| EF-C-0003134 | 87120.0 | 21956.0 | -65164.0 | capped at 99th pct |
| EF-C-0003134 | 21956.0 | 87120.0 | 65164.0 | adjusted (other) |
| EF-C-0003176 | 86503.0 | 67853.0 | -18650.0 | capped at 99th pct |
| EF-C-0003176 | 67853.0 | 86503.0 | 18650.0 | adjusted (other) |
| EF-C-0003177 | 62108.0 | 28179.0 | -33929.0 | capped at 99th pct |
| EF-C-0003177 | 28179.0 | 62108.0 | 33929.0 | adjusted (other) |
| EF-C-0003181 | 72194.0 | 68010.0 | -4184.0 | capped at 99th pct |
| EF-C-0003181 | 68010.0 | 72194.0 | 4184.0 | adjusted (other) |
| EF-C-0003182 | 25054.0 | 22583.0 | -2471.0 | capped at 99th pct |
| EF-C-0003182 | 22583.0 | 25054.0 | 2471.0 | adjusted (other) |
| EF-C-0003202 | 79142.0 | 72673.0 | -6469.0 | capped at 99th pct |
| EF-C-0003202 | 72673.0 | 79142.0 | 6469.0 | adjusted (other) |
| EF-C-0003203 | 75979.0 | 34242.0 | -41737.0 | capped at 99th pct |
| EF-C-0003203 | 34242.0 | 75979.0 | 41737.0 | adjusted (other) |
| EF-C-0003213 | 70523.0 | 72639.0 | 2116.0 | adjusted (other) |
| EF-C-0003213 | 72639.0 | 70523.0 | -2116.0 | capped at 99th pct |
| EF-C-0003214 | 29386.0 | 75510.0 | 46124.0 | adjusted (other) |
| EF-C-0003214 | 75510.0 | 29386.0 | -46124.0 | capped at 99th pct |
| EF-C-0003218 | 21359.0 | 84484.0 | 63125.0 | adjusted (other) |
| EF-C-0003218 | 84484.0 | 21359.0 | -63125.0 | capped at 99th pct |
| EF-C-0003219 | 64963.0 | 60513.0 | -4450.0 | capped at 99th pct |
| EF-C-0003219 | 60513.0 | 64963.0 | 4450.0 | adjusted (other) |
| EF-C-0003247 | 223648.0 | 40071.0 | -183577.0 | capped at 99th pct |
| EF-C-0003247 | 40071.0 | 223648.0 | 183577.0 | adjusted (other) |
| EF-C-0003248 | 52273.0 | 43804.0 | -8469.0 | capped at 99th pct |
| EF-C-0003248 | 43804.0 | 52273.0 | 8469.0 | adjusted (other) |
| EF-C-0003257 | 121261.0 | 81857.0 | -39404.0 | capped at 99th pct |
| EF-C-0003257 | 81857.0 | 121261.0 | 39404.0 | adjusted (other) |
| EF-C-0003258 | 75386.0 | 184425.0 | 109039.0 | adjusted (other) |
| EF-C-0003258 | 184425.0 | 75386.0 | -109039.0 | capped at 99th pct |
| EF-C-0003313 | 55748.0 | 77583.0 | 21835.0 | adjusted (other) |
| EF-C-0003313 | 77583.0 | 55748.0 | -21835.0 | capped at 99th pct |
| EF-C-0003314 | 86542.0 | 84324.0 | -2218.0 | capped at 99th pct |
| EF-C-0003314 | 84324.0 | 86542.0 | 2218.0 | adjusted (other) |
| EF-C-0003343 | 95959.0 | 84527.0 | -11432.0 | capped at 99th pct |
| EF-C-0003343 | 84527.0 | 95959.0 | 11432.0 | adjusted (other) |
| EF-C-0003344 | 81733.0 | 36759.0 | -44974.0 | capped at 99th pct |
| EF-C-0003344 | 36759.0 | 81733.0 | 44974.0 | adjusted (other) |
| EF-C-0003357 | 72274.0 | 150742.0 | 78468.0 | adjusted (other) |
| EF-C-0003357 | 150742.0 | 72274.0 | -78468.0 | capped at 99th pct |
| EF-C-0003358 | 77516.0 | 71634.0 | -5882.0 | capped at 99th pct |
| EF-C-0003358 | 71634.0 | 77516.0 | 5882.0 | adjusted (other) |
| EF-C-0003373 | 137056.0 | 144499.0 | 7443.0 | adjusted (other) |
| EF-C-0003373 | 144499.0 | 137056.0 | -7443.0 | capped at 99th pct |
| EF-C-0003374 | 86859.0 | 143064.0 | 56205.0 | adjusted (other) |
| EF-C-0003374 | 143064.0 | 86859.0 | -56205.0 | capped at 99th pct |
| EF-C-0003391 | 49533.0 | 102338.0 | 52805.0 | adjusted (other) |
| EF-C-0003391 | 102338.0 | 49533.0 | -52805.0 | capped at 99th pct |
| EF-C-0003392 | 178310.0 | 65723.0 | -112587.0 | capped at 99th pct |
| EF-C-0003392 | 65723.0 | 178310.0 | 112587.0 | adjusted (other) |
| EF-C-0003484 | 94495.0 | 88466.0 | -6029.0 | capped at 99th pct |
| EF-C-0003484 | 88466.0 | 94495.0 | 6029.0 | adjusted (other) |
| EF-C-0003485 | 47640.0 | 33018.0 | -14622.0 | capped at 99th pct |
| EF-C-0003485 | 33018.0 | 47640.0 | 14622.0 | adjusted (other) |
| EF-C-0003490 | 68754.0 | 64100.0 | -4654.0 | capped at 99th pct |
| EF-C-0003490 | 64100.0 | 68754.0 | 4654.0 | adjusted (other) |
| EF-C-0003491 | 145926.0 | 48178.0 | -97748.0 | capped at 99th pct |
| EF-C-0003491 | 48178.0 | 145926.0 | 97748.0 | adjusted (other) |
| EF-C-0003507 | 117612.0 | 97659.0 | -19953.0 | capped at 99th pct |
| EF-C-0003507 | 117612.0 | 81699.0 | -35913.0 | capped at 99th pct |
| EF-C-0003507 | 97659.0 | 117612.0 | 19953.0 | adjusted (other) |
| EF-C-0003507 | 97659.0 | 81699.0 | -15960.0 | capped at 99th pct |
| EF-C-0003507 | 81699.0 | 117612.0 | 35913.0 | adjusted (other) |
| EF-C-0003507 | 81699.0 | 97659.0 | 15960.0 | adjusted (other) |
| EF-C-0003508 | 59427.0 | 79047.0 | 19620.0 | adjusted (other) |
| EF-C-0003508 | 59427.0 | 101193.0 | 41766.0 | adjusted (other) |
| EF-C-0003508 | 79047.0 | 59427.0 | -19620.0 | capped at 99th pct |
| EF-C-0003508 | 79047.0 | 101193.0 | 22146.0 | adjusted (other) |
| EF-C-0003508 | 101193.0 | 59427.0 | -41766.0 | capped at 99th pct |
| EF-C-0003508 | 101193.0 | 79047.0 | -22146.0 | capped at 99th pct |
| EF-C-0003509 | 42727.0 | 37233.0 | -5494.0 | capped at 99th pct |
| EF-C-0003509 | 42727.0 | 51554.0 | 8827.0 | adjusted (other) |
| EF-C-0003509 | 37233.0 | 42727.0 | 5494.0 | adjusted (other) |
| EF-C-0003509 | 37233.0 | 51554.0 | 14321.0 | adjusted (other) |
| EF-C-0003509 | 51554.0 | 42727.0 | -8827.0 | capped at 99th pct |
| EF-C-0003509 | 51554.0 | 37233.0 | -14321.0 | capped at 99th pct |
| EF-C-0003517 | 63883.0 | 54259.0 | -9624.0 | capped at 99th pct |
| EF-C-0003517 | 54259.0 | 63883.0 | 9624.0 | adjusted (other) |
| EF-C-0003518 | 102804.0 | 85552.0 | -17252.0 | capped at 99th pct |
| EF-C-0003518 | 85552.0 | 102804.0 | 17252.0 | adjusted (other) |
| EF-C-0003531 | 179362.0 | 250405.0 | 71043.0 | adjusted (other) |
| EF-C-0003531 | 250405.0 | 179362.0 | -71043.0 | capped at 99th pct |
| EF-C-0003532 | 117565.0 | 88740.0 | -28825.0 | capped at 99th pct |
| EF-C-0003532 | 88740.0 | 117565.0 | 28825.0 | adjusted (other) |
| EF-C-0003541 | 446840.0 | 183190.0 | -263650.0 | capped at 99th pct |
| EF-C-0003555 | 44392.0 | 82102.0 | 37710.0 | adjusted (other) |
| EF-C-0003555 | 82102.0 | 44392.0 | -37710.0 | capped at 99th pct |
| EF-C-0003556 | 39811.0 | 67451.0 | 27640.0 | adjusted (other) |
| EF-C-0003556 | 67451.0 | 39811.0 | -27640.0 | capped at 99th pct |
| EF-C-0003558 | 141061.0 | 92429.0 | -48632.0 | capped at 99th pct |
| EF-C-0003558 | 141061.0 | 58605.0 | -82456.0 | capped at 99th pct |
| EF-C-0003558 | 92429.0 | 141061.0 | 48632.0 | adjusted (other) |
| EF-C-0003558 | 92429.0 | 58605.0 | -33824.0 | capped at 99th pct |
| EF-C-0003558 | 58605.0 | 141061.0 | 82456.0 | adjusted (other) |
| EF-C-0003558 | 58605.0 | 92429.0 | 33824.0 | adjusted (other) |
| EF-C-0003559 | 41135.0 | 69484.0 | 28349.0 | adjusted (other) |
| EF-C-0003559 | 41135.0 | 157863.0 | 116728.0 | adjusted (other) |
| EF-C-0003559 | 69484.0 | 41135.0 | -28349.0 | capped at 99th pct |
| EF-C-0003559 | 69484.0 | 157863.0 | 88379.0 | adjusted (other) |
| EF-C-0003559 | 157863.0 | 41135.0 | -116728.0 | capped at 99th pct |
| EF-C-0003559 | 157863.0 | 69484.0 | -88379.0 | capped at 99th pct |
| EF-C-0003560 | 47466.0 | 32856.0 | -14610.0 | capped at 99th pct |
| EF-C-0003560 | 47466.0 | 52678.0 | 5212.0 | adjusted (other) |
| EF-C-0003560 | 32856.0 | 47466.0 | 14610.0 | adjusted (other) |
| EF-C-0003560 | 32856.0 | 52678.0 | 19822.0 | adjusted (other) |
| EF-C-0003560 | 52678.0 | 47466.0 | -5212.0 | capped at 99th pct |
| EF-C-0003560 | 52678.0 | 32856.0 | -19822.0 | capped at 99th pct |
| EF-C-0003578 | 83396.0 | 95641.0 | 12245.0 | adjusted (other) |
| EF-C-0003578 | 95641.0 | 83396.0 | -12245.0 | capped at 99th pct |
| EF-C-0003579 | 64284.0 | 36780.0 | -27504.0 | capped at 99th pct |
| EF-C-0003579 | 36780.0 | 64284.0 | 27504.0 | adjusted (other) |
| EF-C-0003586 | 30696.0 | 45681.0 | 14985.0 | adjusted (other) |
| EF-C-0003586 | 45681.0 | 30696.0 | -14985.0 | capped at 99th pct |
| EF-C-0003587 | 71627.0 | 77455.0 | 5828.0 | adjusted (other) |
| EF-C-0003587 | 77455.0 | 71627.0 | -5828.0 | capped at 99th pct |
| EF-C-0003588 | 123639.0 | 96533.0 | -27106.0 | capped at 99th pct |
| EF-C-0003588 | 96533.0 | 123639.0 | 27106.0 | adjusted (other) |
| EF-C-0003589 | 41104.0 | 145845.0 | 104741.0 | adjusted (other) |
| EF-C-0003589 | 145845.0 | 41104.0 | -104741.0 | capped at 99th pct |
| EF-C-0003630 | 122771.0 | 132811.0 | 10040.0 | adjusted (other) |
| EF-C-0003630 | 132811.0 | 122771.0 | -10040.0 | capped at 99th pct |
| EF-C-0003631 | 137566.0 | 115507.0 | -22059.0 | capped at 99th pct |
| EF-C-0003631 | 115507.0 | 137566.0 | 22059.0 | adjusted (other) |
| EF-C-0003640 | 280563.0 | 51575.0 | -228988.0 | capped at 99th pct |
| EF-C-0003640 | 51575.0 | 280563.0 | 228988.0 | adjusted (other) |
| EF-C-0003641 | 95570.0 | 171260.0 | 75690.0 | adjusted (other) |
| EF-C-0003641 | 171260.0 | 95570.0 | -75690.0 | capped at 99th pct |
| EF-C-0003646 | 82535.0 | 195136.0 | 112601.0 | adjusted (other) |
| EF-C-0003646 | 195136.0 | 82535.0 | -112601.0 | capped at 99th pct |
| EF-C-0003647 | 60158.0 | 187831.0 | 127673.0 | adjusted (other) |
| EF-C-0003647 | 187831.0 | 60158.0 | -127673.0 | capped at 99th pct |
| EF-C-0003676 | 45579.0 | 33364.0 | -12215.0 | capped at 99th pct |
| EF-C-0003676 | 33364.0 | 45579.0 | 12215.0 | adjusted (other) |
| EF-C-0003677 | 76368.0 | 44359.0 | -32009.0 | capped at 99th pct |
| EF-C-0003677 | 44359.0 | 76368.0 | 32009.0 | adjusted (other) |
| EF-C-0003678 | 58124.0 | 17481.0 | -40643.0 | capped at 99th pct |
| EF-C-0003678 | 17481.0 | 58124.0 | 40643.0 | adjusted (other) |
| EF-C-0003679 | 22280.0 | 85827.0 | 63547.0 | adjusted (other) |
| EF-C-0003679 | 85827.0 | 22280.0 | -63547.0 | capped at 99th pct |
| EF-C-0003697 | 149840.0 | 71939.0 | -77901.0 | capped at 99th pct |
| EF-C-0003697 | 71939.0 | 149840.0 | 77901.0 | adjusted (other) |
| EF-C-0003698 | 142410.0 | 114443.0 | -27967.0 | capped at 99th pct |
| EF-C-0003698 | 114443.0 | 142410.0 | 27967.0 | adjusted (other) |
| EF-C-0003722 | 44370.0 | 84248.0 | 39878.0 | adjusted (other) |
| EF-C-0003722 | 84248.0 | 44370.0 | -39878.0 | capped at 99th pct |
| EF-C-0003723 | 60633.0 | 76692.0 | 16059.0 | adjusted (other) |
| EF-C-0003723 | 76692.0 | 60633.0 | -16059.0 | capped at 99th pct |
| EF-C-0003727 | 83915.0 | 108700.0 | 24785.0 | adjusted (other) |
| EF-C-0003727 | 108700.0 | 83915.0 | -24785.0 | capped at 99th pct |
| EF-C-0003728 | 74242.0 | 89682.0 | 15440.0 | adjusted (other) |
| EF-C-0003728 | 89682.0 | 74242.0 | -15440.0 | capped at 99th pct |
| EF-C-0003764 | 60903.0 | 198553.0 | 137650.0 | adjusted (other) |
| EF-C-0003764 | 198553.0 | 60903.0 | -137650.0 | capped at 99th pct |
| EF-C-0003765 | 173717.0 | 85267.0 | -88450.0 | capped at 99th pct |
| EF-C-0003765 | 85267.0 | 173717.0 | 88450.0 | adjusted (other) |
| EF-C-0003780 | 53522.0 | 45177.0 | -8345.0 | capped at 99th pct |
| EF-C-0003780 | 45177.0 | 53522.0 | 8345.0 | adjusted (other) |
| EF-C-0003781 | 38272.0 | 73473.0 | 35201.0 | adjusted (other) |
| EF-C-0003781 | 73473.0 | 38272.0 | -35201.0 | capped at 99th pct |
| EF-C-0003812 | 34065.0 | 80871.0 | 46806.0 | adjusted (other) |
| EF-C-0003812 | 80871.0 | 34065.0 | -46806.0 | capped at 99th pct |
| EF-C-0003813 | -64479.0 | 136042.0 | 200521.0 | adjusted (other) |
| EF-C-0003874 | 53418.0 | 46535.0 | -6883.0 | capped at 99th pct |
| EF-C-0003874 | 46535.0 | 53418.0 | 6883.0 | adjusted (other) |
| EF-C-0003875 | 36146.0 | 18586.0 | -17560.0 | capped at 99th pct |
| EF-C-0003875 | 18586.0 | 36146.0 | 17560.0 | adjusted (other) |
| EF-C-0003890 | 95555.0 | 117924.0 | 22369.0 | adjusted (other) |
| EF-C-0003890 | 117924.0 | 95555.0 | -22369.0 | capped at 99th pct |
| EF-C-0003891 | 65389.0 | 273513.0 | 208124.0 | adjusted (other) |
| EF-C-0003891 | 273513.0 | 65389.0 | -208124.0 | capped at 99th pct |
| EF-C-0003903 | 65692.0 | 131900.0 | 66208.0 | adjusted (other) |
| EF-C-0003903 | 131900.0 | 65692.0 | -66208.0 | capped at 99th pct |
| EF-C-0003904 | 148454.0 | 108482.0 | -39972.0 | capped at 99th pct |
| EF-C-0003904 | 108482.0 | 148454.0 | 39972.0 | adjusted (other) |
| EF-C-0003909 | 90382.0 | 88703.0 | -1679.0 | capped at 99th pct |
| EF-C-0003909 | 88703.0 | 90382.0 | 1679.0 | adjusted (other) |
| EF-C-0003910 | 22706.0 | 36794.0 | 14088.0 | adjusted (other) |
| EF-C-0003910 | 36794.0 | 22706.0 | -14088.0 | capped at 99th pct |
| EF-C-0003915 | 123256.0 | 84515.0 | -38741.0 | capped at 99th pct |
| EF-C-0003915 | 84515.0 | 123256.0 | 38741.0 | adjusted (other) |
| EF-C-0003916 | 48421.0 | 85271.0 | 36850.0 | adjusted (other) |
| EF-C-0003916 | 85271.0 | 48421.0 | -36850.0 | capped at 99th pct |
| EF-C-0003954 | 65406.0 | 108245.0 | 42839.0 | adjusted (other) |
| EF-C-0003954 | 108245.0 | 65406.0 | -42839.0 | capped at 99th pct |
| EF-C-0003955 | 90791.0 | 47135.0 | -43656.0 | capped at 99th pct |
| EF-C-0003955 | 47135.0 | 90791.0 | 43656.0 | adjusted (other) |
| EF-C-0003990 | 68979.0 | 29121.0 | -39858.0 | capped at 99th pct |
| EF-C-0003990 | 29121.0 | 68979.0 | 39858.0 | adjusted (other) |
| EF-C-0003991 | 69556.0 | 28697.0 | -40859.0 | capped at 99th pct |
| EF-C-0003991 | 28697.0 | 69556.0 | 40859.0 | adjusted (other) |
| EF-C-0003994 | 93752.0 | 45996.0 | -47756.0 | capped at 99th pct |
| EF-C-0003994 | 45996.0 | 93752.0 | 47756.0 | adjusted (other) |
| EF-C-0003995 | 52173.0 | 53386.0 | 1213.0 | adjusted (other) |
| EF-C-0003995 | 53386.0 | 52173.0 | -1213.0 | capped at 99th pct |
| EF-C-0004000 | 79395.0 | 85657.0 | 6262.0 | adjusted (other) |
| EF-C-0004000 | 85657.0 | 79395.0 | -6262.0 | capped at 99th pct |
| EF-C-0004001 | 90996.0 | 105875.0 | 14879.0 | adjusted (other) |
| EF-C-0004001 | 105875.0 | 90996.0 | -14879.0 | capped at 99th pct |
| EF-C-0004010 | 16259.0 | 36545.0 | 20286.0 | adjusted (other) |
| EF-C-0004010 | 36545.0 | 16259.0 | -20286.0 | capped at 99th pct |
| EF-C-0004011 | 78032.0 | 94227.0 | 16195.0 | adjusted (other) |
| EF-C-0004011 | 94227.0 | 78032.0 | -16195.0 | capped at 99th pct |
| EF-C-0004072 | 30418.0 | 33331.0 | 2913.0 | adjusted (other) |
| EF-C-0004072 | 33331.0 | 30418.0 | -2913.0 | capped at 99th pct |
| EF-C-0004073 | 132065.0 | 213175.0 | 81110.0 | adjusted (other) |
| EF-C-0004073 | 213175.0 | 132065.0 | -81110.0 | capped at 99th pct |
| EF-C-0004101 | 40050.0 | 168190.0 | 128140.0 | adjusted (other) |
| EF-C-0004101 | 168190.0 | 40050.0 | -128140.0 | capped at 99th pct |
| EF-C-0004102 | 38291.0 | 67635.0 | 29344.0 | adjusted (other) |
| EF-C-0004102 | 67635.0 | 38291.0 | -29344.0 | capped at 99th pct |
| EF-C-0004151 | 52314.0 | 30729.0 | -21585.0 | capped at 99th pct |
| EF-C-0004151 | 30729.0 | 52314.0 | 21585.0 | adjusted (other) |
| EF-C-0004152 | 14513.0 | 142824.0 | 128311.0 | adjusted (other) |
| EF-C-0004152 | 142824.0 | 14513.0 | -128311.0 | capped at 99th pct |
| EF-C-0004162 | 61396.0 | 177565.0 | 116169.0 | adjusted (other) |
| EF-C-0004162 | 177565.0 | 61396.0 | -116169.0 | capped at 99th pct |
| EF-C-0004163 | 39035.0 | 95467.0 | 56432.0 | adjusted (other) |
| EF-C-0004163 | 95467.0 | 39035.0 | -56432.0 | capped at 99th pct |
| EF-C-0004179 | 88923.0 | 104300.0 | 15377.0 | adjusted (other) |
| EF-C-0004179 | 104300.0 | 88923.0 | -15377.0 | capped at 99th pct |
| EF-C-0004180 | 104223.0 | 109860.0 | 5637.0 | adjusted (other) |
| EF-C-0004180 | 109860.0 | 104223.0 | -5637.0 | capped at 99th pct |
| EF-C-0004185 | 115064.0 | 177304.0 | 62240.0 | adjusted (other) |
| EF-C-0004185 | 177304.0 | 115064.0 | -62240.0 | capped at 99th pct |
| EF-C-0004186 | 84743.0 | 144968.0 | 60225.0 | adjusted (other) |
| EF-C-0004186 | 144968.0 | 84743.0 | -60225.0 | capped at 99th pct |
| EF-C-0004197 | 63486.0 | 53550.0 | -9936.0 | capped at 99th pct |
| EF-C-0004197 | 53550.0 | 63486.0 | 9936.0 | adjusted (other) |
| EF-C-0004198 | 65144.0 | 86323.0 | 21179.0 | adjusted (other) |
| EF-C-0004198 | 86323.0 | 65144.0 | -21179.0 | capped at 99th pct |
| EF-C-0004201 | 127191.0 | 73761.0 | -53430.0 | capped at 99th pct |
| EF-C-0004201 | 73761.0 | 127191.0 | 53430.0 | adjusted (other) |
| EF-C-0004202 | 51074.0 | 111302.0 | 60228.0 | adjusted (other) |
| EF-C-0004202 | 111302.0 | 51074.0 | -60228.0 | capped at 99th pct |
| EF-C-0004206 | 22697.0 | 40147.0 | 17450.0 | adjusted (other) |
| EF-C-0004206 | 40147.0 | 22697.0 | -17450.0 | capped at 99th pct |
| EF-C-0004207 | 103531.0 | 86129.0 | -17402.0 | capped at 99th pct |
| EF-C-0004207 | 86129.0 | 103531.0 | 17402.0 | adjusted (other) |
| EF-C-0004219 | 132823.0 | 65270.0 | -67553.0 | capped at 99th pct |
| EF-C-0004219 | 65270.0 | 132823.0 | 67553.0 | adjusted (other) |
| EF-C-0004220 | 50109.0 | 49593.0 | -516.0 | capped at 99th pct |
| EF-C-0004220 | 49593.0 | 50109.0 | 516.0 | adjusted (other) |
| EF-C-0004228 | 86244.0 | 234303.0 | 148059.0 | adjusted (other) |
| EF-C-0004228 | 234303.0 | 86244.0 | -148059.0 | capped at 99th pct |
| EF-C-0004229 | 159564.0 | 250023.0 | 90459.0 | adjusted (other) |
| EF-C-0004229 | 250023.0 | 159564.0 | -90459.0 | capped at 99th pct |
| EF-C-0004235 | 131673.0 | 85946.0 | -45727.0 | capped at 99th pct |
| EF-C-0004235 | 85946.0 | 131673.0 | 45727.0 | adjusted (other) |
| EF-C-0004236 | 120407.0 | 148234.0 | 27827.0 | adjusted (other) |
| EF-C-0004236 | 148234.0 | 120407.0 | -27827.0 | capped at 99th pct |
| EF-C-0004255 | 230254.0 | 117361.0 | -112893.0 | capped at 99th pct |
| EF-C-0004255 | 230254.0 | 96224.0 | -134030.0 | capped at 99th pct |
| EF-C-0004255 | 117361.0 | 230254.0 | 112893.0 | adjusted (other) |
| EF-C-0004255 | 117361.0 | 96224.0 | -21137.0 | capped at 99th pct |
| EF-C-0004255 | 96224.0 | 230254.0 | 134030.0 | adjusted (other) |
| EF-C-0004255 | 96224.0 | 117361.0 | 21137.0 | adjusted (other) |
| EF-C-0004256 | 51169.0 | 68609.0 | 17440.0 | adjusted (other) |
| EF-C-0004256 | 51169.0 | 126805.0 | 75636.0 | adjusted (other) |
| EF-C-0004256 | 68609.0 | 51169.0 | -17440.0 | capped at 99th pct |
| EF-C-0004256 | 68609.0 | 126805.0 | 58196.0 | adjusted (other) |
| EF-C-0004256 | 126805.0 | 51169.0 | -75636.0 | capped at 99th pct |
| EF-C-0004256 | 126805.0 | 68609.0 | -58196.0 | capped at 99th pct |
| EF-C-0004257 | 46137.0 | 112724.0 | 66587.0 | adjusted (other) |
| EF-C-0004257 | 46137.0 | 77588.0 | 31451.0 | adjusted (other) |
| EF-C-0004257 | 112724.0 | 46137.0 | -66587.0 | capped at 99th pct |
| EF-C-0004257 | 112724.0 | 77588.0 | -35136.0 | capped at 99th pct |
| EF-C-0004257 | 77588.0 | 46137.0 | -31451.0 | capped at 99th pct |
| EF-C-0004257 | 77588.0 | 112724.0 | 35136.0 | adjusted (other) |
| EF-C-0004281 | 74616.0 | 184509.0 | 109893.0 | adjusted (other) |
| EF-C-0004281 | 184509.0 | 74616.0 | -109893.0 | capped at 99th pct |
| EF-C-0004282 | 94718.0 | 220895.0 | 126177.0 | adjusted (other) |
| EF-C-0004282 | 220895.0 | 94718.0 | -126177.0 | capped at 99th pct |
| EF-C-0004287 | 196598.0 | 121938.0 | -74660.0 | capped at 99th pct |
| EF-C-0004287 | 121938.0 | 196598.0 | 74660.0 | adjusted (other) |
| EF-C-0004288 | -43909.0 | 69837.0 | 113746.0 | adjusted (other) |
| EF-C-0004297 | 97800.0 | 68677.0 | -29123.0 | capped at 99th pct |
| EF-C-0004297 | 68677.0 | 97800.0 | 29123.0 | adjusted (other) |
| EF-C-0004298 | 85252.0 | 64346.0 | -20906.0 | capped at 99th pct |
| EF-C-0004298 | 64346.0 | 85252.0 | 20906.0 | adjusted (other) |
| EF-C-0004300 | 93311.0 | 167730.0 | 74419.0 | adjusted (other) |
| EF-C-0004300 | 167730.0 | 93311.0 | -74419.0 | capped at 99th pct |
| EF-C-0004301 | 84138.0 | 94180.0 | 10042.0 | adjusted (other) |
| EF-C-0004301 | 94180.0 | 84138.0 | -10042.0 | capped at 99th pct |
| EF-C-0004304 | 211910.0 | 110762.0 | -101148.0 | capped at 99th pct |
| EF-C-0004304 | 110762.0 | 211910.0 | 101148.0 | adjusted (other) |
| EF-C-0004305 | 194893.0 | 210910.0 | 16017.0 | adjusted (other) |
| EF-C-0004305 | 210910.0 | 194893.0 | -16017.0 | capped at 99th pct |
| EF-C-0004309 | 48994.0 | 54601.0 | 5607.0 | adjusted (other) |
| EF-C-0004309 | 54601.0 | 48994.0 | -5607.0 | capped at 99th pct |
| EF-C-0004310 | 90770.0 | 84994.0 | -5776.0 | capped at 99th pct |
| EF-C-0004310 | 84994.0 | 90770.0 | 5776.0 | adjusted (other) |
| EF-C-0004336 | 20687.0 | 29681.0 | 8994.0 | adjusted (other) |
| EF-C-0004336 | 29681.0 | 20687.0 | -8994.0 | capped at 99th pct |
| EF-C-0004337 | 40476.0 | 53458.0 | 12982.0 | adjusted (other) |
| EF-C-0004337 | 53458.0 | 40476.0 | -12982.0 | capped at 99th pct |
| EF-C-0004371 | 95916.0 | 81913.0 | -14003.0 | capped at 99th pct |
| EF-C-0004371 | 81913.0 | 95916.0 | 14003.0 | adjusted (other) |
| EF-C-0004372 | 101839.0 | 103623.0 | 1784.0 | adjusted (other) |
| EF-C-0004372 | 103623.0 | 101839.0 | -1784.0 | capped at 99th pct |
| EF-C-0004440 | 150922.0 | 42791.0 | -108131.0 | capped at 99th pct |
| EF-C-0004440 | 42791.0 | 150922.0 | 108131.0 | adjusted (other) |
| EF-C-0004441 | 55541.0 | 80442.0 | 24901.0 | adjusted (other) |
| EF-C-0004441 | 80442.0 | 55541.0 | -24901.0 | capped at 99th pct |
| EF-C-0004475 | 60559.0 | 92810.0 | 32251.0 | adjusted (other) |
| EF-C-0004475 | 92810.0 | 60559.0 | -32251.0 | capped at 99th pct |
| EF-C-0004476 | 84508.0 | 290586.0 | 206078.0 | adjusted (other) |
| EF-C-0004476 | 290586.0 | 84508.0 | -206078.0 | capped at 99th pct |
| EF-C-0004483 | 76456.0 | 90901.0 | 14445.0 | adjusted (other) |
| EF-C-0004483 | 90901.0 | 76456.0 | -14445.0 | capped at 99th pct |
| EF-C-0004484 | 28797.0 | 49559.0 | 20762.0 | adjusted (other) |
| EF-C-0004484 | 49559.0 | 28797.0 | -20762.0 | capped at 99th pct |
| EF-C-0004523 | 46832.0 | 88855.0 | 42023.0 | adjusted (other) |
| EF-C-0004523 | 88855.0 | 46832.0 | -42023.0 | capped at 99th pct |
| EF-C-0004524 | 114120.0 | 137041.0 | 22921.0 | adjusted (other) |
| EF-C-0004524 | 137041.0 | 114120.0 | -22921.0 | capped at 99th pct |
| EF-C-0004534 | 108985.0 | 99710.0 | -9275.0 | capped at 99th pct |
| EF-C-0004534 | 99710.0 | 108985.0 | 9275.0 | adjusted (other) |
| EF-C-0004535 | 73827.0 | 93830.0 | 20003.0 | adjusted (other) |
| EF-C-0004535 | 93830.0 | 73827.0 | -20003.0 | capped at 99th pct |
| EF-C-0004589 | 23163.0 | 69404.0 | 46241.0 | adjusted (other) |
| EF-C-0004589 | 23163.0 | 57922.0 | 34759.0 | adjusted (other) |
| EF-C-0004589 | 69404.0 | 23163.0 | -46241.0 | capped at 99th pct |
| EF-C-0004589 | 69404.0 | 57922.0 | -11482.0 | capped at 99th pct |
| EF-C-0004589 | 57922.0 | 23163.0 | -34759.0 | capped at 99th pct |
| EF-C-0004589 | 57922.0 | 69404.0 | 11482.0 | adjusted (other) |
| EF-C-0004590 | 53879.0 | 90636.0 | 36757.0 | adjusted (other) |
| EF-C-0004590 | 53879.0 | 80117.0 | 26238.0 | adjusted (other) |
| EF-C-0004590 | 90636.0 | 53879.0 | -36757.0 | capped at 99th pct |
| EF-C-0004590 | 90636.0 | 80117.0 | -10519.0 | capped at 99th pct |
| EF-C-0004590 | 80117.0 | 53879.0 | -26238.0 | capped at 99th pct |
| EF-C-0004590 | 80117.0 | 90636.0 | 10519.0 | adjusted (other) |
| EF-C-0004591 | 91671.0 | 76923.0 | -14748.0 | capped at 99th pct |
| EF-C-0004591 | 91671.0 | 51878.0 | -39793.0 | capped at 99th pct |
| EF-C-0004591 | 76923.0 | 91671.0 | 14748.0 | adjusted (other) |
| EF-C-0004591 | 76923.0 | 51878.0 | -25045.0 | capped at 99th pct |
| EF-C-0004591 | 51878.0 | 91671.0 | 39793.0 | adjusted (other) |
| EF-C-0004591 | 51878.0 | 76923.0 | 25045.0 | adjusted (other) |
| EF-C-0004597 | 32373.0 | 28735.0 | -3638.0 | capped at 99th pct |
| EF-C-0004597 | 28735.0 | 32373.0 | 3638.0 | adjusted (other) |
| EF-C-0004598 | 37273.0 | 149247.0 | 111974.0 | adjusted (other) |
| EF-C-0004598 | 149247.0 | 37273.0 | -111974.0 | capped at 99th pct |
| EF-C-0004611 | 45552.0 | 68656.0 | 23104.0 | adjusted (other) |
| EF-C-0004611 | 68656.0 | 45552.0 | -23104.0 | capped at 99th pct |
| EF-C-0004612 | 22881.0 | 62198.0 | 39317.0 | adjusted (other) |
| EF-C-0004612 | 62198.0 | 22881.0 | -39317.0 | capped at 99th pct |
| EF-C-0004648 | 122902.0 | 31475.0 | -91427.0 | capped at 99th pct |
| EF-C-0004648 | 31475.0 | 122902.0 | 91427.0 | adjusted (other) |
| EF-C-0004649 | 28532.0 | 45923.0 | 17391.0 | adjusted (other) |
| EF-C-0004649 | 45923.0 | 28532.0 | -17391.0 | capped at 99th pct |
| EF-C-0004669 | 121489.0 | 76529.0 | -44960.0 | capped at 99th pct |
| EF-C-0004669 | 76529.0 | 121489.0 | 44960.0 | adjusted (other) |
| EF-C-0004671 | 102230.0 | 73048.0 | -29182.0 | capped at 99th pct |
| EF-C-0004671 | 73048.0 | 102230.0 | 29182.0 | adjusted (other) |
| EF-C-0004672 | 55218.0 | 101107.0 | 45889.0 | adjusted (other) |
| EF-C-0004672 | 101107.0 | 55218.0 | -45889.0 | capped at 99th pct |
| EF-C-0004679 | 241682.0 | 46356.0 | -195326.0 | capped at 99th pct |
| EF-C-0004679 | 46356.0 | 241682.0 | 195326.0 | adjusted (other) |
| EF-C-0004680 | 111430.0 | 81747.0 | -29683.0 | capped at 99th pct |
| EF-C-0004680 | 81747.0 | 111430.0 | 29683.0 | adjusted (other) |
| EF-C-0004710 | 111286.0 | 185312.0 | 74026.0 | adjusted (other) |
| EF-C-0004710 | 185312.0 | 111286.0 | -74026.0 | capped at 99th pct |
| EF-C-0004711 | 146872.0 | 76777.0 | -70095.0 | capped at 99th pct |
| EF-C-0004711 | 76777.0 | 146872.0 | 70095.0 | adjusted (other) |
| EF-C-0004735 | 49718.0 | 39212.0 | -10506.0 | capped at 99th pct |
| EF-C-0004735 | 39212.0 | 49718.0 | 10506.0 | adjusted (other) |
| EF-C-0004736 | 42132.0 | 36976.0 | -5156.0 | capped at 99th pct |
| EF-C-0004736 | 36976.0 | 42132.0 | 5156.0 | adjusted (other) |
| EF-C-0004741 | 26112.0 | 18812.0 | -7300.0 | capped at 99th pct |
| EF-C-0004741 | 18812.0 | 26112.0 | 7300.0 | adjusted (other) |
| EF-C-0004742 | 36400.0 | 81198.0 | 44798.0 | adjusted (other) |
| EF-C-0004742 | 81198.0 | 36400.0 | -44798.0 | capped at 99th pct |
| EF-C-0004762 | 94602.0 | 103731.0 | 9129.0 | adjusted (other) |
| EF-C-0004762 | 103731.0 | 94602.0 | -9129.0 | capped at 99th pct |
| EF-C-0004763 | 79650.0 | 76518.0 | -3132.0 | capped at 99th pct |
| EF-C-0004763 | 76518.0 | 79650.0 | 3132.0 | adjusted (other) |
| EF-C-0004807 | 697254.5332 | 39070.0 | -658184.5332 | capped at 99th pct |
| EF-C-0004808 | 35442.0 | 39127.0 | 3685.0 | adjusted (other) |
| EF-C-0004808 | 39127.0 | 35442.0 | -3685.0 | capped at 99th pct |
| EF-C-0004847 | 42981.0 | 47458.0 | 4477.0 | adjusted (other) |
| EF-C-0004847 | 47458.0 | 42981.0 | -4477.0 | capped at 99th pct |
| EF-C-0004848 | 121496.0 | 84368.0 | -37128.0 | capped at 99th pct |
| EF-C-0004848 | 84368.0 | 121496.0 | 37128.0 | adjusted (other) |
| EF-C-0004882 | 128455.0 | 122956.0 | -5499.0 | capped at 99th pct |
| EF-C-0004882 | 122956.0 | 128455.0 | 5499.0 | adjusted (other) |
| EF-C-0004883 | 139153.0 | 75382.0 | -63771.0 | capped at 99th pct |
| EF-C-0004883 | 75382.0 | 139153.0 | 63771.0 | adjusted (other) |
| EF-C-0004907 | 49466.0 | 23852.0 | -25614.0 | capped at 99th pct |
| EF-C-0004907 | 23852.0 | 49466.0 | 25614.0 | adjusted (other) |
| EF-C-0004908 | 134777.0 | 72953.0 | -61824.0 | capped at 99th pct |
| EF-C-0004908 | 72953.0 | 134777.0 | 61824.0 | adjusted (other) |
| EF-C-0004909 | 122045.0 | 78994.0 | -43051.0 | capped at 99th pct |
| EF-C-0004909 | 78994.0 | 122045.0 | 43051.0 | adjusted (other) |
| EF-C-0004910 | 51795.0 | 81580.0 | 29785.0 | adjusted (other) |
| EF-C-0004910 | 81580.0 | 51795.0 | -29785.0 | capped at 99th pct |
| EF-C-0004934 | 33790.0 | 38037.0 | 4247.0 | adjusted (other) |
| EF-C-0004934 | 38037.0 | 33790.0 | -4247.0 | capped at 99th pct |
| EF-C-0004935 | 87141.0 | 63657.0 | -23484.0 | capped at 99th pct |
| EF-C-0004935 | 63657.0 | 87141.0 | 23484.0 | adjusted (other) |
| EF-C-0004983 | 137833.0 | 57577.0 | -80256.0 | capped at 99th pct |
| EF-C-0004983 | 57577.0 | 137833.0 | 80256.0 | adjusted (other) |
| EF-C-0004984 | 85400.0 | 63023.0 | -22377.0 | capped at 99th pct |
| EF-C-0004984 | 63023.0 | 85400.0 | 22377.0 | adjusted (other) |
| EF-C-0004993 | 76435.0 | 104661.0 | 28226.0 | adjusted (other) |
| EF-C-0004993 | 104661.0 | 76435.0 | -28226.0 | capped at 99th pct |
| EF-C-0004994 | 74570.0 | 63159.0 | -11411.0 | capped at 99th pct |
| EF-C-0004994 | 63159.0 | 74570.0 | 11411.0 | adjusted (other) |
| EF-C-0004996 | 52429.0 | 163062.0 | 110633.0 | adjusted (other) |
| EF-C-0004996 | 163062.0 | 52429.0 | -110633.0 | capped at 99th pct |
| EF-C-0004997 | 90847.0 | 42720.0 | -48127.0 | capped at 99th pct |
| EF-C-0004997 | 42720.0 | 90847.0 | 48127.0 | adjusted (other) |
| EF-C-0005010 | 84474.0 | 60157.0 | -24317.0 | capped at 99th pct |
| EF-C-0005010 | 60157.0 | 84474.0 | 24317.0 | adjusted (other) |
| EF-C-0005015 | 37018.0 | 48745.0 | 11727.0 | adjusted (other) |
| EF-C-0005015 | 48745.0 | 37018.0 | -11727.0 | capped at 99th pct |
| EF-C-0005016 | 49176.0 | 34989.0 | -14187.0 | capped at 99th pct |
| EF-C-0005016 | 34989.0 | 49176.0 | 14187.0 | adjusted (other) |
| EF-C-0005039 | 100526.0 | 97706.0 | -2820.0 | capped at 99th pct |
| EF-C-0005039 | 97706.0 | 100526.0 | 2820.0 | adjusted (other) |
| EF-C-0005040 | 204703.0 | 52708.0 | -151995.0 | capped at 99th pct |
| EF-C-0005040 | 52708.0 | 204703.0 | 151995.0 | adjusted (other) |
| EF-C-0005055 | 63841.0 | 92193.0 | 28352.0 | adjusted (other) |
| EF-C-0005055 | 92193.0 | 63841.0 | -28352.0 | capped at 99th pct |
| EF-C-0005056 | 314197.0 | 87412.0 | -226785.0 | capped at 99th pct |
| EF-C-0005061 | 80533.0 | 21047.0 | -59486.0 | capped at 99th pct |
| EF-C-0005061 | 21047.0 | 80533.0 | 59486.0 | adjusted (other) |
| EF-C-0005062 | 52104.0 | 102111.0 | 50007.0 | adjusted (other) |
| EF-C-0005062 | 102111.0 | 52104.0 | -50007.0 | capped at 99th pct |
| EF-C-0005063 | 90275.0 | 89175.0 | -1100.0 | capped at 99th pct |
| EF-C-0005063 | 89175.0 | 90275.0 | 1100.0 | adjusted (other) |
| EF-C-0005064 | 150587.0 | 79786.0 | -70801.0 | capped at 99th pct |
| EF-C-0005064 | 79786.0 | 150587.0 | 70801.0 | adjusted (other) |
| EF-C-0005069 | 102530.0 | 74241.0 | -28289.0 | capped at 99th pct |
| EF-C-0005069 | 74241.0 | 102530.0 | 28289.0 | adjusted (other) |
| EF-C-0005070 | 75407.0 | 130993.0 | 55586.0 | adjusted (other) |
| EF-C-0005070 | 130993.0 | 75407.0 | -55586.0 | capped at 99th pct |
| EF-C-0005083 | 125272.0 | 130011.0 | 4739.0 | adjusted (other) |
| EF-C-0005083 | 130011.0 | 125272.0 | -4739.0 | capped at 99th pct |
| EF-C-0005084 | 89964.0 | 263794.0 | 173830.0 | adjusted (other) |
| EF-C-0005084 | 263794.0 | 89964.0 | -173830.0 | capped at 99th pct |
| EF-C-0005122 | 45497.0 | 71099.0 | 25602.0 | adjusted (other) |
| EF-C-0005122 | 71099.0 | 45497.0 | -25602.0 | capped at 99th pct |
| EF-C-0005123 | 41259.0 | 41309.0 | 50.0 | adjusted (other) |
| EF-C-0005123 | 41309.0 | 41259.0 | -50.0 | capped at 99th pct |
| EF-C-0005139 | 48603.0 | 43550.0 | -5053.0 | capped at 99th pct |
| EF-C-0005139 | 43550.0 | 48603.0 | 5053.0 | adjusted (other) |
| EF-C-0005140 | 43418.0 | 55167.0 | 11749.0 | adjusted (other) |
| EF-C-0005140 | 55167.0 | 43418.0 | -11749.0 | capped at 99th pct |
| EF-C-0005152 | 276868.0 | 45706.0 | -231162.0 | capped at 99th pct |
| EF-C-0005152 | 45706.0 | 276868.0 | 231162.0 | adjusted (other) |
| EF-C-0005153 | 159042.0 | 91789.0 | -67253.0 | capped at 99th pct |
| EF-C-0005153 | 91789.0 | 159042.0 | 67253.0 | adjusted (other) |
| EF-C-0005183 | 35195.0 | 122293.0 | 87098.0 | adjusted (other) |
| EF-C-0005183 | 122293.0 | 35195.0 | -87098.0 | capped at 99th pct |
| EF-C-0005184 | 83082.0 | 60891.0 | -22191.0 | capped at 99th pct |
| EF-C-0005184 | 60891.0 | 83082.0 | 22191.0 | adjusted (other) |
| EF-C-0005188 | 79627.0 | 256528.0 | 176901.0 | adjusted (other) |
| EF-C-0005188 | 256528.0 | 79627.0 | -176901.0 | capped at 99th pct |
| EF-C-0005189 | 230710.0 | 101967.0 | -128743.0 | capped at 99th pct |
| EF-C-0005189 | 101967.0 | 230710.0 | 128743.0 | adjusted (other) |
| EF-C-0005193 | 238449.0 | 85863.0 | -152586.0 | capped at 99th pct |
| EF-C-0005193 | 238449.0 | 207451.0 | -30998.0 | capped at 99th pct |
| EF-C-0005193 | 85863.0 | 238449.0 | 152586.0 | adjusted (other) |
| EF-C-0005193 | 85863.0 | 207451.0 | 121588.0 | adjusted (other) |
| EF-C-0005193 | 207451.0 | 238449.0 | 30998.0 | adjusted (other) |
| EF-C-0005193 | 207451.0 | 85863.0 | -121588.0 | capped at 99th pct |
| EF-C-0005194 | 62354.0 | 74004.0 | 11650.0 | adjusted (other) |
| EF-C-0005194 | 62354.0 | 112136.0 | 49782.0 | adjusted (other) |
| EF-C-0005194 | 74004.0 | 62354.0 | -11650.0 | capped at 99th pct |
| EF-C-0005194 | 74004.0 | 112136.0 | 38132.0 | adjusted (other) |
| EF-C-0005194 | 112136.0 | 62354.0 | -49782.0 | capped at 99th pct |
| EF-C-0005194 | 112136.0 | 74004.0 | -38132.0 | capped at 99th pct |
| EF-C-0005195 | 55160.0 | 44185.0 | -10975.0 | capped at 99th pct |
| EF-C-0005195 | 55160.0 | 140612.0 | 85452.0 | adjusted (other) |
| EF-C-0005195 | 44185.0 | 55160.0 | 10975.0 | adjusted (other) |
| EF-C-0005195 | 44185.0 | 140612.0 | 96427.0 | adjusted (other) |
| EF-C-0005195 | 140612.0 | 55160.0 | -85452.0 | capped at 99th pct |
| EF-C-0005195 | 140612.0 | 44185.0 | -96427.0 | capped at 99th pct |
| EF-C-0005196 | 120319.0 | 109509.0 | -10810.0 | capped at 99th pct |
| EF-C-0005196 | 109509.0 | 120319.0 | 10810.0 | adjusted (other) |
| EF-C-0005197 | 122033.0 | 170567.0 | 48534.0 | adjusted (other) |
| EF-C-0005197 | 170567.0 | 122033.0 | -48534.0 | capped at 99th pct |
| EF-C-0005215 | 123552.0 | 107868.0 | -15684.0 | capped at 99th pct |
| EF-C-0005215 | 107868.0 | 123552.0 | 15684.0 | adjusted (other) |
| EF-C-0005216 | 123468.0 | 156282.0 | 32814.0 | adjusted (other) |
| EF-C-0005216 | 156282.0 | 123468.0 | -32814.0 | capped at 99th pct |
| EF-C-0005236 | 82518.0 | 72102.0 | -10416.0 | capped at 99th pct |
| EF-C-0005236 | 82518.0 | 71167.0 | -11351.0 | capped at 99th pct |
| EF-C-0005236 | 72102.0 | 82518.0 | 10416.0 | adjusted (other) |
| EF-C-0005236 | 72102.0 | 71167.0 | -935.0 | capped at 99th pct |
| EF-C-0005236 | 71167.0 | 82518.0 | 11351.0 | adjusted (other) |
| EF-C-0005236 | 71167.0 | 72102.0 | 935.0 | adjusted (other) |
| EF-C-0005237 | 59426.0 | 126116.0 | 66690.0 | adjusted (other) |
| EF-C-0005237 | 59426.0 | 78093.0 | 18667.0 | adjusted (other) |
| EF-C-0005237 | 126116.0 | 59426.0 | -66690.0 | capped at 99th pct |
| EF-C-0005237 | 126116.0 | 78093.0 | -48023.0 | capped at 99th pct |
| EF-C-0005237 | 78093.0 | 59426.0 | -18667.0 | capped at 99th pct |
| EF-C-0005237 | 78093.0 | 126116.0 | 48023.0 | adjusted (other) |
| EF-C-0005238 | 35492.0 | 120120.0 | 84628.0 | adjusted (other) |
| EF-C-0005238 | 35492.0 | 53257.0 | 17765.0 | adjusted (other) |
| EF-C-0005238 | 120120.0 | 35492.0 | -84628.0 | capped at 99th pct |
| EF-C-0005238 | 120120.0 | 53257.0 | -66863.0 | capped at 99th pct |
| EF-C-0005238 | 53257.0 | 35492.0 | -17765.0 | capped at 99th pct |
| EF-C-0005238 | 53257.0 | 120120.0 | 66863.0 | adjusted (other) |
| EF-C-0005239 | 81948.0 | 40523.0 | -41425.0 | capped at 99th pct |
| EF-C-0005239 | 40523.0 | 81948.0 | 41425.0 | adjusted (other) |
| EF-C-0005240 | 56611.0 | 24641.0 | -31970.0 | capped at 99th pct |
| EF-C-0005240 | 24641.0 | 56611.0 | 31970.0 | adjusted (other) |
| EF-C-0005252 | 88808.0 | 55566.0 | -33242.0 | capped at 99th pct |
| EF-C-0005252 | 55566.0 | 88808.0 | 33242.0 | adjusted (other) |
| EF-C-0005253 | 54014.0 | 87713.0 | 33699.0 | adjusted (other) |
| EF-C-0005253 | 87713.0 | 54014.0 | -33699.0 | capped at 99th pct |
| EF-C-0005257 | 98270.0 | 211509.0 | 113239.0 | adjusted (other) |
| EF-C-0005257 | 211509.0 | 98270.0 | -113239.0 | capped at 99th pct |
| EF-C-0005258 | 44276.0 | 57665.0 | 13389.0 | adjusted (other) |
| EF-C-0005258 | 57665.0 | 44276.0 | -13389.0 | capped at 99th pct |
| EF-C-0005265 | 31578.0 | 56167.0 | 24589.0 | adjusted (other) |
| EF-C-0005265 | 56167.0 | 31578.0 | -24589.0 | capped at 99th pct |
| EF-C-0005266 | 70208.0 | 52419.0 | -17789.0 | capped at 99th pct |
| EF-C-0005266 | 52419.0 | 70208.0 | 17789.0 | adjusted (other) |
| EF-C-0005267 | 46060.0 | 72075.0 | 26015.0 | adjusted (other) |
| EF-C-0005267 | 72075.0 | 46060.0 | -26015.0 | capped at 99th pct |
| EF-C-0005268 | 80091.0 | 51772.0 | -28319.0 | capped at 99th pct |
| EF-C-0005268 | 51772.0 | 80091.0 | 28319.0 | adjusted (other) |
| EF-C-0005284 | 126851.0 | 128544.0 | 1693.0 | adjusted (other) |
| EF-C-0005284 | 128544.0 | 126851.0 | -1693.0 | capped at 99th pct |
| EF-C-0005285 | 80791.0 | 78416.0 | -2375.0 | capped at 99th pct |
| EF-C-0005285 | 78416.0 | 80791.0 | 2375.0 | adjusted (other) |
| EF-C-0005344 | 190400.0 | 103852.0 | -86548.0 | capped at 99th pct |
| EF-C-0005344 | 103852.0 | 190400.0 | 86548.0 | adjusted (other) |
| EF-C-0005345 | 46640.0 | 127397.0 | 80757.0 | adjusted (other) |
| EF-C-0005345 | 127397.0 | 46640.0 | -80757.0 | capped at 99th pct |
| EF-C-0005366 | 75849.0 | 37216.0 | -38633.0 | capped at 99th pct |
| EF-C-0005366 | 37216.0 | 75849.0 | 38633.0 | adjusted (other) |
| EF-C-0005367 | 76039.0 | 68446.0 | -7593.0 | capped at 99th pct |
| EF-C-0005367 | 68446.0 | 76039.0 | 7593.0 | adjusted (other) |
| EF-C-0005383 | 225002.0 | 101912.0 | -123090.0 | capped at 99th pct |
| EF-C-0005383 | 101912.0 | 225002.0 | 123090.0 | adjusted (other) |
| EF-C-0005384 | 66672.0 | 171747.0 | 105075.0 | adjusted (other) |
| EF-C-0005384 | 171747.0 | 66672.0 | -105075.0 | capped at 99th pct |
| EF-C-0005388 | 143075.0 | 163573.0 | 20498.0 | adjusted (other) |
| EF-C-0005388 | 163573.0 | 143075.0 | -20498.0 | capped at 99th pct |
| EF-C-0005389 | 69767.0 | 38763.0 | -31004.0 | capped at 99th pct |
| EF-C-0005389 | 38763.0 | 69767.0 | 31004.0 | adjusted (other) |
| EF-C-0005391 | 27734.0 | 36726.0 | 8992.0 | adjusted (other) |
| EF-C-0005391 | 36726.0 | 27734.0 | -8992.0 | capped at 99th pct |
| EF-C-0005392 | 47472.0 | 102557.0 | 55085.0 | adjusted (other) |
| EF-C-0005392 | 102557.0 | 47472.0 | -55085.0 | capped at 99th pct |
| EF-C-0005400 | 92129.0 | 49608.0 | -42521.0 | capped at 99th pct |
| EF-C-0005400 | 49608.0 | 92129.0 | 42521.0 | adjusted (other) |
| EF-C-0005401 | 77610.0 | 53357.0 | -24253.0 | capped at 99th pct |
| EF-C-0005401 | 53357.0 | 77610.0 | 24253.0 | adjusted (other) |
| EF-C-0005402 | 66819.0 | 65936.0 | -883.0 | capped at 99th pct |
| EF-C-0005402 | 65936.0 | 66819.0 | 883.0 | adjusted (other) |
| EF-C-0005403 | 61786.0 | 47095.0 | -14691.0 | capped at 99th pct |
| EF-C-0005403 | 47095.0 | 61786.0 | 14691.0 | adjusted (other) |
| EF-C-0005406 | 44664.0 | 66156.0 | 21492.0 | adjusted (other) |
| EF-C-0005406 | 66156.0 | 44664.0 | -21492.0 | capped at 99th pct |
| EF-C-0005407 | 38254.0 | 68018.0 | 29764.0 | adjusted (other) |
| EF-C-0005407 | 68018.0 | 38254.0 | -29764.0 | capped at 99th pct |
| EF-C-0005408 | 82274.0 | 253218.0 | 170944.0 | adjusted (other) |
| EF-C-0005408 | 253218.0 | 82274.0 | -170944.0 | capped at 99th pct |
| EF-C-0005409 | 88251.0 | 247476.0 | 159225.0 | adjusted (other) |
| EF-C-0005409 | 247476.0 | 88251.0 | -159225.0 | capped at 99th pct |
| EF-C-0005419 | 73226.0 | 72446.0 | -780.0 | capped at 99th pct |
| EF-C-0005419 | 72446.0 | 73226.0 | 780.0 | adjusted (other) |
| EF-C-0005420 | 1634400.688 | 102897.0 | -1531503.688 | capped at 99th pct |
| EF-C-0005429 | 148846.0 | 114517.0 | -34329.0 | capped at 99th pct |
| EF-C-0005429 | 114517.0 | 148846.0 | 34329.0 | adjusted (other) |
| EF-C-0005430 | 355677.0 | 265632.0 | -90045.0 | capped at 99th pct |
| EF-C-0005441 | 11725.0 | 45145.0 | 33420.0 | adjusted (other) |
| EF-C-0005441 | 45145.0 | 11725.0 | -33420.0 | capped at 99th pct |
| EF-C-0005442 | 62561.0 | 54650.0 | -7911.0 | capped at 99th pct |
| EF-C-0005442 | 54650.0 | 62561.0 | 7911.0 | adjusted (other) |
| EF-C-0005452 | 61140.0 | 21695.0 | -39445.0 | capped at 99th pct |
| EF-C-0005452 | 21695.0 | 61140.0 | 39445.0 | adjusted (other) |
| EF-C-0005453 | 52826.0 | 84509.0 | 31683.0 | adjusted (other) |
| EF-C-0005453 | 84509.0 | 52826.0 | -31683.0 | capped at 99th pct |
| EF-C-0005458 | 29230.0 | 42580.0 | 13350.0 | adjusted (other) |
| EF-C-0005458 | 42580.0 | 29230.0 | -13350.0 | capped at 99th pct |
| EF-C-0005459 | 66576.0 | 42720.0 | -23856.0 | capped at 99th pct |
| EF-C-0005459 | 42720.0 | 66576.0 | 23856.0 | adjusted (other) |
| EF-C-0005472 | 37270.0 | 57069.0 | 19799.0 | adjusted (other) |
| EF-C-0005472 | 57069.0 | 37270.0 | -19799.0 | capped at 99th pct |
| EF-C-0005473 | 164578.0 | 63001.0 | -101577.0 | capped at 99th pct |
| EF-C-0005473 | 63001.0 | 164578.0 | 101577.0 | adjusted (other) |
| EF-C-0005479 | 35788.0 | 122381.0 | 86593.0 | adjusted (other) |
| EF-C-0005479 | 122381.0 | 35788.0 | -86593.0 | capped at 99th pct |
| EF-C-0005480 | 162724.0 | 80064.0 | -82660.0 | capped at 99th pct |
| EF-C-0005480 | 80064.0 | 162724.0 | 82660.0 | adjusted (other) |
| EF-C-0005489 | 25174.0 | 49566.0 | 24392.0 | adjusted (other) |
| EF-C-0005489 | 49566.0 | 25174.0 | -24392.0 | capped at 99th pct |
| EF-C-0005490 | 48417.0 | 96535.0 | 48118.0 | adjusted (other) |
| EF-C-0005490 | 96535.0 | 48417.0 | -48118.0 | capped at 99th pct |
| EF-C-0005529 | 95288.0 | 97657.0 | 2369.0 | adjusted (other) |
| EF-C-0005529 | 97657.0 | 95288.0 | -2369.0 | capped at 99th pct |
| EF-C-0005530 | 41111.0 | 90834.0 | 49723.0 | adjusted (other) |
| EF-C-0005530 | 90834.0 | 41111.0 | -49723.0 | capped at 99th pct |
| EF-C-0005536 | 30442.0 | 53456.0 | 23014.0 | adjusted (other) |
| EF-C-0005536 | 53456.0 | 30442.0 | -23014.0 | capped at 99th pct |
| EF-C-0005537 | 87104.0 | 31948.0 | -55156.0 | capped at 99th pct |
| EF-C-0005537 | 31948.0 | 87104.0 | 55156.0 | adjusted (other) |
| EF-C-0005541 | 41094.0 | 100650.0 | 59556.0 | adjusted (other) |
| EF-C-0005541 | 100650.0 | 41094.0 | -59556.0 | capped at 99th pct |
| EF-C-0005545 | 88748.0 | 40825.0 | -47923.0 | capped at 99th pct |
| EF-C-0005545 | 40825.0 | 88748.0 | 47923.0 | adjusted (other) |
| EF-C-0005546 | 51391.0 | 28302.0 | -23089.0 | capped at 99th pct |
| EF-C-0005546 | 28302.0 | 51391.0 | 23089.0 | adjusted (other) |
| EF-C-0005581 | 181920.0 | 157873.0 | -24047.0 | capped at 99th pct |
| EF-C-0005581 | 157873.0 | 181920.0 | 24047.0 | adjusted (other) |
| EF-C-0005582 | 94917.0 | 90208.0 | -4709.0 | capped at 99th pct |
| EF-C-0005582 | 90208.0 | 94917.0 | 4709.0 | adjusted (other) |
| EF-C-0005592 | 134821.0 | 95841.0 | -38980.0 | capped at 99th pct |
| EF-C-0005592 | 95841.0 | 134821.0 | 38980.0 | adjusted (other) |
| EF-C-0005593 | 188354.0 | 105573.0 | -82781.0 | capped at 99th pct |
| EF-C-0005593 | 105573.0 | 188354.0 | 82781.0 | adjusted (other) |
| EF-C-0005604 | 85770.0 | 87014.0 | 1244.0 | adjusted (other) |
| EF-C-0005604 | 87014.0 | 85770.0 | -1244.0 | capped at 99th pct |
| EF-C-0005605 | 62313.0 | 33641.0 | -28672.0 | capped at 99th pct |
| EF-C-0005605 | 33641.0 | 62313.0 | 28672.0 | adjusted (other) |
| EF-C-0005636 | 26701.0 | 96770.0 | 70069.0 | adjusted (other) |
| EF-C-0005636 | 96770.0 | 26701.0 | -70069.0 | capped at 99th pct |
| EF-C-0005637 | 344693.0 | 169120.0 | -175573.0 | capped at 99th pct |
| EF-C-0005659 | 42291.0 | 44635.0 | 2344.0 | adjusted (other) |
| EF-C-0005659 | 44635.0 | 42291.0 | -2344.0 | capped at 99th pct |
| EF-C-0005660 | 102193.0 | 71916.0 | -30277.0 | capped at 99th pct |
| EF-C-0005660 | 71916.0 | 102193.0 | 30277.0 | adjusted (other) |
| EF-C-0005689 | 54194.0 | 40264.0 | -13930.0 | capped at 99th pct |
| EF-C-0005689 | 40264.0 | 54194.0 | 13930.0 | adjusted (other) |
| EF-C-0005690 | 27988.0 | 35757.0 | 7769.0 | adjusted (other) |
| EF-C-0005690 | 35757.0 | 27988.0 | -7769.0 | capped at 99th pct |
| EF-C-0005794 | 107538.0 | 37010.0 | -70528.0 | capped at 99th pct |
| EF-C-0005794 | 37010.0 | 107538.0 | 70528.0 | adjusted (other) |
| EF-C-0005795 | 25382.0 | 34185.0 | 8803.0 | adjusted (other) |
| EF-C-0005795 | 34185.0 | 25382.0 | -8803.0 | capped at 99th pct |
| EF-C-0005800 | 213451.0 | 171177.0 | -42274.0 | capped at 99th pct |
| EF-C-0005800 | 171177.0 | 213451.0 | 42274.0 | adjusted (other) |
| EF-C-0005801 | 153311.0 | 65908.0 | -87403.0 | capped at 99th pct |
| EF-C-0005801 | 65908.0 | 153311.0 | 87403.0 | adjusted (other) |
| EF-C-0005863 | 42788.0 | 53314.0 | 10526.0 | adjusted (other) |
| EF-C-0005863 | 53314.0 | 42788.0 | -10526.0 | capped at 99th pct |
| EF-C-0005864 | 37955.0 | 49005.0 | 11050.0 | adjusted (other) |
| EF-C-0005864 | 49005.0 | 37955.0 | -11050.0 | capped at 99th pct |
| EF-C-0005895 | 146068.0 | 89544.0 | -56524.0 | capped at 99th pct |
| EF-C-0005895 | 89544.0 | 146068.0 | 56524.0 | adjusted (other) |
| EF-C-0005896 | 120634.0 | 77686.0 | -42948.0 | capped at 99th pct |
| EF-C-0005896 | 77686.0 | 120634.0 | 42948.0 | adjusted (other) |
| EF-C-0005935 | 165612.0 | 41236.0 | -124376.0 | capped at 99th pct |
| EF-C-0005935 | 41236.0 | 165612.0 | 124376.0 | adjusted (other) |
| EF-C-0005936 | 69919.0 | 76481.0 | 6562.0 | adjusted (other) |
| EF-C-0005936 | 76481.0 | 69919.0 | -6562.0 | capped at 99th pct |
| EF-C-0005951 | 86412.0 | 53993.0 | -32419.0 | capped at 99th pct |
| EF-C-0005951 | 53993.0 | 86412.0 | 32419.0 | adjusted (other) |
| EF-C-0005952 | 71298.0 | 51742.0 | -19556.0 | capped at 99th pct |
| EF-C-0005952 | 51742.0 | 71298.0 | 19556.0 | adjusted (other) |
| EF-C-0005966 | 51817.0 | 98907.0 | 47090.0 | adjusted (other) |
| EF-C-0005966 | 98907.0 | 51817.0 | -47090.0 | capped at 99th pct |
| EF-C-0005967 | 100035.0 | 41879.0 | -58156.0 | capped at 99th pct |
| EF-C-0005967 | 41879.0 | 100035.0 | 58156.0 | adjusted (other) |
| EF-C-0005975 | 67776.0 | 49061.0 | -18715.0 | capped at 99th pct |
| EF-C-0005975 | 49061.0 | 67776.0 | 18715.0 | adjusted (other) |
| EF-C-0005976 | 67606.0 | 37514.0 | -30092.0 | capped at 99th pct |
| EF-C-0005976 | 37514.0 | 67606.0 | 30092.0 | adjusted (other) |
| EF-C-0005979 | 90510.0 | 70122.0 | -20388.0 | capped at 99th pct |
| EF-C-0005979 | 70122.0 | 90510.0 | 20388.0 | adjusted (other) |
| EF-C-0005980 | 31606.0 | 50746.0 | 19140.0 | adjusted (other) |
| EF-C-0005980 | 50746.0 | 31606.0 | -19140.0 | capped at 99th pct |
| EF-C-0005999 | 105729.0 | 79426.0 | -26303.0 | capped at 99th pct |
| EF-C-0005999 | 79426.0 | 105729.0 | 26303.0 | adjusted (other) |
| EF-C-0006000 | 43234.0 | 52706.0 | 9472.0 | adjusted (other) |
| EF-C-0006000 | 52706.0 | 43234.0 | -9472.0 | capped at 99th pct |
| EF-C-0006026 | 96176.0 | 48579.0 | -47597.0 | capped at 99th pct |
| EF-C-0006026 | 48579.0 | 96176.0 | 47597.0 | adjusted (other) |
| EF-C-0006027 | 71610.0 | 131010.0 | 59400.0 | adjusted (other) |
| EF-C-0006027 | 131010.0 | 71610.0 | -59400.0 | capped at 99th pct |
| EF-C-0006036 | 52154.0 | 105534.0 | 53380.0 | adjusted (other) |
| EF-C-0006036 | 105534.0 | 52154.0 | -53380.0 | capped at 99th pct |
| EF-C-0006037 | 65856.0 | 122416.0 | 56560.0 | adjusted (other) |
| EF-C-0006037 | 122416.0 | 65856.0 | -56560.0 | capped at 99th pct |
| EF-C-0006055 | 77920.0 | 40377.0 | -37543.0 | capped at 99th pct |
| EF-C-0006055 | 40377.0 | 77920.0 | 37543.0 | adjusted (other) |
| EF-C-0006056 | 20658.0 | 57618.0 | 36960.0 | adjusted (other) |
| EF-C-0006056 | 57618.0 | 20658.0 | -36960.0 | capped at 99th pct |
| EF-C-0006061 | 24477.0 | 91360.0 | 66883.0 | adjusted (other) |
| EF-C-0006061 | 91360.0 | 24477.0 | -66883.0 | capped at 99th pct |
| EF-C-0006062 | 383999.904 | 69775.0 | -314224.904 | capped at 99th pct |
| EF-C-0006065 | 78011.0 | 69326.0 | -8685.0 | capped at 99th pct |
| EF-C-0006065 | 69326.0 | 78011.0 | 8685.0 | adjusted (other) |
| EF-C-0006066 | 78069.0 | 55745.0 | -22324.0 | capped at 99th pct |
| EF-C-0006066 | 55745.0 | 78069.0 | 22324.0 | adjusted (other) |
| EF-C-0006075 | 110899.0 | 44598.0 | -66301.0 | capped at 99th pct |
| EF-C-0006075 | 44598.0 | 110899.0 | 66301.0 | adjusted (other) |
| EF-C-0006076 | 62704.0 | 68356.0 | 5652.0 | adjusted (other) |
| EF-C-0006076 | 68356.0 | 62704.0 | -5652.0 | capped at 99th pct |
| EF-C-0006083 | 105024.0 | 120043.0 | 15019.0 | adjusted (other) |
| EF-C-0006083 | 120043.0 | 105024.0 | -15019.0 | capped at 99th pct |
| EF-C-0006084 | 189056.0 | 123291.0 | -65765.0 | capped at 99th pct |
| EF-C-0006084 | 123291.0 | 189056.0 | 65765.0 | adjusted (other) |
| EF-C-0006136 | 42007.0 | 44559.0 | 2552.0 | adjusted (other) |
| EF-C-0006136 | 44559.0 | 42007.0 | -2552.0 | capped at 99th pct |
| EF-C-0006137 | 104484.0 | 17961.0 | -86523.0 | capped at 99th pct |
| EF-C-0006137 | 17961.0 | 104484.0 | 86523.0 | adjusted (other) |
| EF-C-0006138 | 80935.0 | 116654.0 | 35719.0 | adjusted (other) |
| EF-C-0006138 | 116654.0 | 80935.0 | -35719.0 | capped at 99th pct |
| EF-C-0006139 | 87204.0 | 75170.0 | -12034.0 | capped at 99th pct |
| EF-C-0006139 | 75170.0 | 87204.0 | 12034.0 | adjusted (other) |
| EF-C-0006163 | 45592.0 | 78230.0 | 32638.0 | adjusted (other) |
| EF-C-0006163 | 78230.0 | 45592.0 | -32638.0 | capped at 99th pct |
| EF-C-0006164 | 92470.0 | 143319.0 | 50849.0 | adjusted (other) |
| EF-C-0006164 | 143319.0 | 92470.0 | -50849.0 | capped at 99th pct |
| EF-C-0006201 | 43957.0 | 48385.0 | 4428.0 | adjusted (other) |
| EF-C-0006201 | 48385.0 | 43957.0 | -4428.0 | capped at 99th pct |
| EF-C-0006202 | 91140.0 | 125795.0 | 34655.0 | adjusted (other) |
| EF-C-0006202 | 125795.0 | 91140.0 | -34655.0 | capped at 99th pct |
| EF-C-0006249 | 124226.0 | 93356.0 | -30870.0 | capped at 99th pct |
| EF-C-0006249 | 93356.0 | 124226.0 | 30870.0 | adjusted (other) |
| EF-C-0006250 | 155126.0 | 56360.0 | -98766.0 | capped at 99th pct |
| EF-C-0006250 | 56360.0 | 155126.0 | 98766.0 | adjusted (other) |
| EF-C-0006255 | 85803.0 | 199503.0 | 113700.0 | adjusted (other) |
| EF-C-0006255 | 199503.0 | 85803.0 | -113700.0 | capped at 99th pct |
| EF-C-0006256 | 61920.0 | 60739.0 | -1181.0 | capped at 99th pct |
| EF-C-0006256 | 60739.0 | 61920.0 | 1181.0 | adjusted (other) |
| EF-C-0006268 | 46193.0 | 33000.0 | -13193.0 | capped at 99th pct |
| EF-C-0006268 | 33000.0 | 46193.0 | 13193.0 | adjusted (other) |
| EF-C-0006269 | 55786.0 | 38564.0 | -17222.0 | capped at 99th pct |
| EF-C-0006269 | 38564.0 | 55786.0 | 17222.0 | adjusted (other) |
| EF-C-0006273 | 78855.0 | 27096.0 | -51759.0 | capped at 99th pct |
| EF-C-0006273 | 27096.0 | 78855.0 | 51759.0 | adjusted (other) |
| EF-C-0006274 | 41268.0 | 69217.0 | 27949.0 | adjusted (other) |
| EF-C-0006274 | 69217.0 | 41268.0 | -27949.0 | capped at 99th pct |
| EF-C-0006275 | 93938.0 | 53575.0 | -40363.0 | capped at 99th pct |
| EF-C-0006275 | 53575.0 | 93938.0 | 40363.0 | adjusted (other) |
| EF-C-0006276 | 165544.0 | 128644.0 | -36900.0 | capped at 99th pct |
| EF-C-0006276 | 128644.0 | 165544.0 | 36900.0 | adjusted (other) |
| EF-C-0006286 | 62641.0 | 58017.0 | -4624.0 | capped at 99th pct |
| EF-C-0006286 | 58017.0 | 62641.0 | 4624.0 | adjusted (other) |
| EF-C-0006287 | 160580.0 | 69884.0 | -90696.0 | capped at 99th pct |
| EF-C-0006287 | 69884.0 | 160580.0 | 90696.0 | adjusted (other) |
| EF-C-0006302 | 78402.0 | 106147.0 | 27745.0 | adjusted (other) |
| EF-C-0006302 | 106147.0 | 78402.0 | -27745.0 | capped at 99th pct |
| EF-C-0006303 | 321808.0 | 113027.0 | -208781.0 | capped at 99th pct |
| EF-C-0006339 | 64954.0 | 32159.0 | -32795.0 | capped at 99th pct |
| EF-C-0006339 | 32159.0 | 64954.0 | 32795.0 | adjusted (other) |
| EF-C-0006340 | 56295.0 | 56622.0 | 327.0 | adjusted (other) |
| EF-C-0006340 | 56622.0 | 56295.0 | -327.0 | capped at 99th pct |
| EF-C-0006348 | 24895.0 | 35948.0 | 11053.0 | adjusted (other) |
| EF-C-0006348 | 35948.0 | 24895.0 | -11053.0 | capped at 99th pct |
| EF-C-0006349 | 55899.0 | 30584.0 | -25315.0 | capped at 99th pct |
| EF-C-0006349 | 30584.0 | 55899.0 | 25315.0 | adjusted (other) |
| EF-C-0006400 | 106001.0 | 94968.0 | -11033.0 | capped at 99th pct |
| EF-C-0006400 | 94968.0 | 106001.0 | 11033.0 | adjusted (other) |
| EF-C-0006401 | 77430.0 | 101470.0 | 24040.0 | adjusted (other) |
| EF-C-0006401 | 101470.0 | 77430.0 | -24040.0 | capped at 99th pct |
| EF-C-0006414 | 37058.0 | 59409.0 | 22351.0 | adjusted (other) |
| EF-C-0006414 | 59409.0 | 37058.0 | -22351.0 | capped at 99th pct |
| EF-C-0006415 | 95759.0 | 104319.0 | 8560.0 | adjusted (other) |
| EF-C-0006415 | 104319.0 | 95759.0 | -8560.0 | capped at 99th pct |
| EF-C-0006445 | 46389.0 | 55229.0 | 8840.0 | adjusted (other) |
| EF-C-0006445 | 55229.0 | 46389.0 | -8840.0 | capped at 99th pct |
| EF-C-0006446 | 98959.0 | 81087.0 | -17872.0 | capped at 99th pct |
| EF-C-0006446 | 81087.0 | 98959.0 | 17872.0 | adjusted (other) |
| EF-C-0006452 | 150582.0 | 97855.0 | -52727.0 | capped at 99th pct |
| EF-C-0006452 | 97855.0 | 150582.0 | 52727.0 | adjusted (other) |
| EF-C-0006453 | 114870.0 | 118913.0 | 4043.0 | adjusted (other) |
| EF-C-0006453 | 118913.0 | 114870.0 | -4043.0 | capped at 99th pct |
| EF-C-0006466 | 80582.0 | 212178.0 | 131596.0 | adjusted (other) |
| EF-C-0006466 | 212178.0 | 80582.0 | -131596.0 | capped at 99th pct |
| EF-C-0006475 | 59641.0 | 91431.0 | 31790.0 | adjusted (other) |
| EF-C-0006475 | 91431.0 | 59641.0 | -31790.0 | capped at 99th pct |
| EF-C-0006476 | 78129.0 | 74303.0 | -3826.0 | capped at 99th pct |
| EF-C-0006476 | 74303.0 | 78129.0 | 3826.0 | adjusted (other) |
| EF-C-0006481 | 106456.0 | 76435.0 | -30021.0 | capped at 99th pct |
| EF-C-0006481 | 76435.0 | 106456.0 | 30021.0 | adjusted (other) |
| EF-C-0006482 | 176927.0 | 295337.0 | 118410.0 | adjusted (other) |
| EF-C-0006482 | 295337.0 | 176927.0 | -118410.0 | capped at 99th pct |
| EF-C-0006500 | 74330.0 | 97368.0 | 23038.0 | adjusted (other) |
| EF-C-0006500 | 97368.0 | 74330.0 | -23038.0 | capped at 99th pct |
| EF-C-0006501 | 152909.0 | 159730.0 | 6821.0 | adjusted (other) |
| EF-C-0006501 | 159730.0 | 152909.0 | -6821.0 | capped at 99th pct |
| EF-C-0006508 | 294625.0 | 71508.0 | -223117.0 | capped at 99th pct |
| EF-C-0006508 | 71508.0 | 294625.0 | 223117.0 | adjusted (other) |
| EF-C-0006509 | 133663.0 | 152987.0 | 19324.0 | adjusted (other) |
| EF-C-0006509 | 152987.0 | 133663.0 | -19324.0 | capped at 99th pct |
| EF-C-0006515 | 48896.0 | 66306.0 | 17410.0 | adjusted (other) |
| EF-C-0006515 | 66306.0 | 48896.0 | -17410.0 | capped at 99th pct |
| EF-C-0006516 | 83673.0 | 133887.0 | 50214.0 | adjusted (other) |
| EF-C-0006516 | 133887.0 | 83673.0 | -50214.0 | capped at 99th pct |
| EF-C-0006528 | 233041.0 | 198157.0 | -34884.0 | capped at 99th pct |
| EF-C-0006528 | 198157.0 | 233041.0 | 34884.0 | adjusted (other) |
| EF-C-0006529 | 128804.0 | 166842.0 | 38038.0 | adjusted (other) |
| EF-C-0006529 | 166842.0 | 128804.0 | -38038.0 | capped at 99th pct |
| EF-C-0006549 | 86467.0 | 138792.0 | 52325.0 | adjusted (other) |
| EF-C-0006549 | 138792.0 | 86467.0 | -52325.0 | capped at 99th pct |
| EF-C-0006550 | 39947.0 | 52497.0 | 12550.0 | adjusted (other) |
| EF-C-0006550 | 52497.0 | 39947.0 | -12550.0 | capped at 99th pct |
| EF-C-0006596 | 196730.0 | 105571.0 | -91159.0 | capped at 99th pct |
| EF-C-0006596 | 105571.0 | 196730.0 | 91159.0 | adjusted (other) |
| EF-C-0006597 | 239977.0 | 290893.0 | 50916.0 | adjusted (other) |
| EF-C-0006597 | 290893.0 | 239977.0 | -50916.0 | capped at 99th pct |
| EF-C-0006602 | 294681.0 | 152765.0 | -141916.0 | capped at 99th pct |
| EF-C-0006602 | 294681.0 | 221837.0 | -72844.0 | capped at 99th pct |
| EF-C-0006602 | 152765.0 | 294681.0 | 141916.0 | adjusted (other) |
| EF-C-0006602 | 152765.0 | 221837.0 | 69072.0 | adjusted (other) |
| EF-C-0006602 | 221837.0 | 294681.0 | 72844.0 | adjusted (other) |
| EF-C-0006602 | 221837.0 | 152765.0 | -69072.0 | capped at 99th pct |
| EF-C-0006603 | 3237609.214 | 208431.0 | -3029178.214 | capped at 99th pct |
| EF-C-0006603 | 3237609.214 | 90120.0 | -3147489.214 | capped at 99th pct |
| EF-C-0006603 | 208431.0 | 90120.0 | -118311.0 | capped at 99th pct |
| EF-C-0006603 | 90120.0 | 208431.0 | 118311.0 | adjusted (other) |
| EF-C-0006604 | 146076.0 | 184420.0 | 38344.0 | adjusted (other) |
| EF-C-0006604 | 146076.0 | 161051.0 | 14975.0 | adjusted (other) |
| EF-C-0006604 | 184420.0 | 146076.0 | -38344.0 | capped at 99th pct |
| EF-C-0006604 | 184420.0 | 161051.0 | -23369.0 | capped at 99th pct |
| EF-C-0006604 | 161051.0 | 146076.0 | -14975.0 | capped at 99th pct |
| EF-C-0006604 | 161051.0 | 184420.0 | 23369.0 | adjusted (other) |
| EF-C-0006607 | 260001.0 | 101265.0 | -158736.0 | capped at 99th pct |
| EF-C-0006607 | 101265.0 | 260001.0 | 158736.0 | adjusted (other) |
| EF-C-0006608 | 88819.0 | 48571.0 | -40248.0 | capped at 99th pct |
| EF-C-0006608 | 48571.0 | 88819.0 | 40248.0 | adjusted (other) |
| EF-C-0006644 | 78294.0 | 46482.0 | -31812.0 | capped at 99th pct |
| EF-C-0006644 | 46482.0 | 78294.0 | 31812.0 | adjusted (other) |
| EF-C-0006645 | 88900.0 | 60158.0 | -28742.0 | capped at 99th pct |
| EF-C-0006645 | 60158.0 | 88900.0 | 28742.0 | adjusted (other) |
| EF-C-0006668 | 84430.0 | 125092.0 | 40662.0 | adjusted (other) |
| EF-C-0006668 | 125092.0 | 84430.0 | -40662.0 | capped at 99th pct |
| EF-C-0006669 | 178622.0 | 111862.0 | -66760.0 | capped at 99th pct |
| EF-C-0006669 | 111862.0 | 178622.0 | 66760.0 | adjusted (other) |
| EF-C-0006678 | 25690.0 | 125600.0 | 99910.0 | adjusted (other) |
| EF-C-0006678 | 125600.0 | 25690.0 | -99910.0 | capped at 99th pct |
| EF-C-0006679 | 58902.0 | 43497.0 | -15405.0 | capped at 99th pct |
| EF-C-0006679 | 43497.0 | 58902.0 | 15405.0 | adjusted (other) |
| EF-C-0006682 | 16816.0 | 67882.0 | 51066.0 | adjusted (other) |
| EF-C-0006682 | 67882.0 | 16816.0 | -51066.0 | capped at 99th pct |
| EF-C-0006683 | 56333.0 | 38207.0 | -18126.0 | capped at 99th pct |
| EF-C-0006683 | 38207.0 | 56333.0 | 18126.0 | adjusted (other) |
| EF-C-0006708 | 84934.0 | 232582.0 | 147648.0 | adjusted (other) |
| EF-C-0006708 | 232582.0 | 84934.0 | -147648.0 | capped at 99th pct |
| EF-C-0006753 | 65326.0 | 30681.0 | -34645.0 | capped at 99th pct |
| EF-C-0006753 | 30681.0 | 65326.0 | 34645.0 | adjusted (other) |
| EF-C-0006754 | 81064.0 | 51534.0 | -29530.0 | capped at 99th pct |
| EF-C-0006754 | 51534.0 | 81064.0 | 29530.0 | adjusted (other) |
| EF-C-0006762 | 40567.0 | 63399.0 | 22832.0 | adjusted (other) |
| EF-C-0006762 | 63399.0 | 40567.0 | -22832.0 | capped at 99th pct |
| EF-C-0006763 | 97286.0 | 45675.0 | -51611.0 | capped at 99th pct |
| EF-C-0006763 | 45675.0 | 97286.0 | 51611.0 | adjusted (other) |
| EF-C-0006785 | 62603.0 | 109166.0 | 46563.0 | adjusted (other) |
| EF-C-0006785 | 109166.0 | 62603.0 | -46563.0 | capped at 99th pct |
| EF-C-0006786 | 34148.0 | 110221.0 | 76073.0 | adjusted (other) |
| EF-C-0006786 | 110221.0 | 34148.0 | -76073.0 | capped at 99th pct |
| EF-C-0006794 | 129555.0 | 69300.0 | -60255.0 | capped at 99th pct |
| EF-C-0006794 | 69300.0 | 129555.0 | 60255.0 | adjusted (other) |
| EF-C-0006795 | 70375.0 | 108179.0 | 37804.0 | adjusted (other) |
| EF-C-0006795 | 108179.0 | 70375.0 | -37804.0 | capped at 99th pct |
| EF-C-0006823 | 185640.0 | 59886.0 | -125754.0 | capped at 99th pct |
| EF-C-0006823 | 185640.0 | 148879.0 | -36761.0 | capped at 99th pct |
| EF-C-0006823 | 59886.0 | 185640.0 | 125754.0 | adjusted (other) |
| EF-C-0006823 | 59886.0 | 148879.0 | 88993.0 | adjusted (other) |
| EF-C-0006823 | 148879.0 | 185640.0 | 36761.0 | adjusted (other) |
| EF-C-0006823 | 148879.0 | 59886.0 | -88993.0 | capped at 99th pct |
| EF-C-0006824 | 194542.0 | 70197.0 | -124345.0 | capped at 99th pct |
| EF-C-0006824 | 194542.0 | 119690.0 | -74852.0 | capped at 99th pct |
| EF-C-0006824 | 70197.0 | 194542.0 | 124345.0 | adjusted (other) |
| EF-C-0006824 | 70197.0 | 119690.0 | 49493.0 | adjusted (other) |
| EF-C-0006824 | 119690.0 | 194542.0 | 74852.0 | adjusted (other) |
| EF-C-0006824 | 119690.0 | 70197.0 | -49493.0 | capped at 99th pct |
| EF-C-0006825 | 81527.0 | 75742.0 | -5785.0 | capped at 99th pct |
| EF-C-0006825 | 81527.0 | 103995.0 | 22468.0 | adjusted (other) |
| EF-C-0006825 | 75742.0 | 81527.0 | 5785.0 | adjusted (other) |
| EF-C-0006825 | 75742.0 | 103995.0 | 28253.0 | adjusted (other) |
| EF-C-0006825 | 103995.0 | 81527.0 | -22468.0 | capped at 99th pct |
| EF-C-0006825 | 103995.0 | 75742.0 | -28253.0 | capped at 99th pct |
| EF-C-0006829 | 65578.0 | 92716.0 | 27138.0 | adjusted (other) |
| EF-C-0006829 | 92716.0 | 65578.0 | -27138.0 | capped at 99th pct |
| EF-C-0006830 | 41179.0 | 55512.0 | 14333.0 | adjusted (other) |
| EF-C-0006830 | 55512.0 | 41179.0 | -14333.0 | capped at 99th pct |
| EF-C-0006901 | 75725.0 | 26755.0 | -48970.0 | capped at 99th pct |
| EF-C-0006901 | 26755.0 | 75725.0 | 48970.0 | adjusted (other) |
| EF-C-0006902 | 78217.0 | 25560.0 | -52657.0 | capped at 99th pct |
| EF-C-0006902 | 25560.0 | 78217.0 | 52657.0 | adjusted (other) |
| EF-C-0006917 | 21570.0 | 48323.0 | 26753.0 | adjusted (other) |
| EF-C-0006917 | 48323.0 | 21570.0 | -26753.0 | capped at 99th pct |
| EF-C-0006918 | 73404.0 | 38081.0 | -35323.0 | capped at 99th pct |
| EF-C-0006918 | 38081.0 | 73404.0 | 35323.0 | adjusted (other) |
| EF-C-0006961 | 84547.0 | 116700.0 | 32153.0 | adjusted (other) |
| EF-C-0006961 | 116700.0 | 84547.0 | -32153.0 | capped at 99th pct |
| EF-C-0006968 | 40457.0 | 44089.0 | 3632.0 | adjusted (other) |
| EF-C-0006968 | 44089.0 | 40457.0 | -3632.0 | capped at 99th pct |
| EF-C-0006969 | 74366.0 | 41700.0 | -32666.0 | capped at 99th pct |
| EF-C-0006969 | 41700.0 | 74366.0 | 32666.0 | adjusted (other) |
| EF-C-0006975 | 116485.0 | 29418.0 | -87067.0 | capped at 99th pct |
| EF-C-0006975 | 29418.0 | 116485.0 | 87067.0 | adjusted (other) |
| EF-C-0006976 | 40912.0 | 101512.0 | 60600.0 | adjusted (other) |
| EF-C-0006976 | 101512.0 | 40912.0 | -60600.0 | capped at 99th pct |
| EF-C-0007001 | 31046.0 | 63607.0 | 32561.0 | adjusted (other) |
| EF-C-0007001 | 63607.0 | 31046.0 | -32561.0 | capped at 99th pct |
| EF-C-0007002 | 23400.0 | 14346.0 | -9054.0 | capped at 99th pct |
| EF-C-0007002 | 14346.0 | 23400.0 | 9054.0 | adjusted (other) |
| EF-C-0007005 | 58994.0 | 76545.0 | 17551.0 | adjusted (other) |
| EF-C-0007005 | 76545.0 | 58994.0 | -17551.0 | capped at 99th pct |
| EF-C-0007006 | 38345.0 | 79469.0 | 41124.0 | adjusted (other) |
| EF-C-0007006 | 79469.0 | 38345.0 | -41124.0 | capped at 99th pct |
| EF-C-0007058 | 59279.0 | 89268.0 | 29989.0 | adjusted (other) |
| EF-C-0007058 | 89268.0 | 59279.0 | -29989.0 | capped at 99th pct |
| EF-C-0007059 | 139917.0 | 116718.0 | -23199.0 | capped at 99th pct |
| EF-C-0007059 | 116718.0 | 139917.0 | 23199.0 | adjusted (other) |
| EF-C-0007062 | 66047.0 | 69170.0 | 3123.0 | adjusted (other) |
| EF-C-0007062 | 69170.0 | 66047.0 | -3123.0 | capped at 99th pct |
| EF-C-0007063 | 89572.0 | 60976.0 | -28596.0 | capped at 99th pct |
| EF-C-0007063 | 60976.0 | 89572.0 | 28596.0 | adjusted (other) |
| EF-C-0007071 | 118317.0 | 163938.0 | 45621.0 | adjusted (other) |
| EF-C-0007071 | 163938.0 | 118317.0 | -45621.0 | capped at 99th pct |
| EF-C-0007072 | 122986.0 | 99580.0 | -23406.0 | capped at 99th pct |
| EF-C-0007072 | 99580.0 | 122986.0 | 23406.0 | adjusted (other) |
| EF-C-0007078 | 111312.0 | 93640.0 | -17672.0 | capped at 99th pct |
| EF-C-0007078 | 111312.0 | 211182.0 | 99870.0 | adjusted (other) |
| EF-C-0007078 | 93640.0 | 111312.0 | 17672.0 | adjusted (other) |
| EF-C-0007078 | 93640.0 | 211182.0 | 117542.0 | adjusted (other) |
| EF-C-0007078 | 211182.0 | 111312.0 | -99870.0 | capped at 99th pct |
| EF-C-0007078 | 211182.0 | 93640.0 | -117542.0 | capped at 99th pct |
| EF-C-0007079 | 100828.0 | 90784.0 | -10044.0 | capped at 99th pct |
| EF-C-0007079 | 100828.0 | 139371.0 | 38543.0 | adjusted (other) |
| EF-C-0007079 | 90784.0 | 100828.0 | 10044.0 | adjusted (other) |
| EF-C-0007079 | 90784.0 | 139371.0 | 48587.0 | adjusted (other) |
| EF-C-0007079 | 139371.0 | 100828.0 | -38543.0 | capped at 99th pct |
| EF-C-0007079 | 139371.0 | 90784.0 | -48587.0 | capped at 99th pct |
| EF-C-0007080 | 241048.0 | 115900.0 | -125148.0 | capped at 99th pct |
| EF-C-0007080 | 241048.0 | 81180.0 | -159868.0 | capped at 99th pct |
| EF-C-0007080 | 115900.0 | 241048.0 | 125148.0 | adjusted (other) |
| EF-C-0007080 | 115900.0 | 81180.0 | -34720.0 | capped at 99th pct |
| EF-C-0007080 | 81180.0 | 241048.0 | 159868.0 | adjusted (other) |
| EF-C-0007080 | 81180.0 | 115900.0 | 34720.0 | adjusted (other) |
| EF-C-0007083 | 75138.0 | 103816.0 | 28678.0 | adjusted (other) |
| EF-C-0007083 | 103816.0 | 75138.0 | -28678.0 | capped at 99th pct |
| EF-C-0007084 | 92414.0 | 94705.0 | 2291.0 | adjusted (other) |
| EF-C-0007084 | 94705.0 | 92414.0 | -2291.0 | capped at 99th pct |
| EF-C-0007108 | 261110.0 | 68629.0 | -192481.0 | capped at 99th pct |
| EF-C-0007108 | 68629.0 | 261110.0 | 192481.0 | adjusted (other) |
| EF-C-0007109 | 37316.0 | 70193.0 | 32877.0 | adjusted (other) |
| EF-C-0007109 | 70193.0 | 37316.0 | -32877.0 | capped at 99th pct |
| EF-C-0007110 | 69765.0 | 230318.0 | 160553.0 | adjusted (other) |
| EF-C-0007110 | 230318.0 | 69765.0 | -160553.0 | capped at 99th pct |
| EF-C-0007111 | 33931.0 | 47166.0 | 13235.0 | adjusted (other) |
| EF-C-0007111 | 47166.0 | 33931.0 | -13235.0 | capped at 99th pct |
| EF-C-0007112 | 43569.0 | 112099.0 | 68530.0 | adjusted (other) |
| EF-C-0007112 | 43569.0 | 113139.0 | 69570.0 | adjusted (other) |
| EF-C-0007112 | 112099.0 | 43569.0 | -68530.0 | capped at 99th pct |
| EF-C-0007112 | 112099.0 | 113139.0 | 1040.0 | adjusted (other) |
| EF-C-0007112 | 113139.0 | 43569.0 | -69570.0 | capped at 99th pct |
| EF-C-0007112 | 113139.0 | 112099.0 | -1040.0 | capped at 99th pct |
| EF-C-0007113 | 52539.0 | 102780.0 | 50241.0 | adjusted (other) |
| EF-C-0007113 | 52539.0 | 83295.0 | 30756.0 | adjusted (other) |
| EF-C-0007113 | 102780.0 | 52539.0 | -50241.0 | capped at 99th pct |
| EF-C-0007113 | 102780.0 | 83295.0 | -19485.0 | capped at 99th pct |
| EF-C-0007113 | 83295.0 | 52539.0 | -30756.0 | capped at 99th pct |
| EF-C-0007113 | 83295.0 | 102780.0 | 19485.0 | adjusted (other) |
| EF-C-0007114 | 72947.0 | 117557.0 | 44610.0 | adjusted (other) |
| EF-C-0007114 | 72947.0 | 56362.0 | -16585.0 | capped at 99th pct |
| EF-C-0007114 | 117557.0 | 72947.0 | -44610.0 | capped at 99th pct |
| EF-C-0007114 | 117557.0 | 56362.0 | -61195.0 | capped at 99th pct |
| EF-C-0007114 | 56362.0 | 72947.0 | 16585.0 | adjusted (other) |
| EF-C-0007114 | 56362.0 | 117557.0 | 61195.0 | adjusted (other) |
| EF-C-0007142 | 34250.0 | 99206.0 | 64956.0 | adjusted (other) |
| EF-C-0007142 | 99206.0 | 34250.0 | -64956.0 | capped at 99th pct |
| EF-C-0007143 | 97902.0 | 152021.0 | 54119.0 | adjusted (other) |
| EF-C-0007143 | 152021.0 | 97902.0 | -54119.0 | capped at 99th pct |
| EF-C-0007144 | 167388.0 | 206825.0 | 39437.0 | adjusted (other) |
| EF-C-0007144 | 206825.0 | 167388.0 | -39437.0 | capped at 99th pct |
| EF-C-0007145 | 50411.0 | 28042.0 | -22369.0 | capped at 99th pct |
| EF-C-0007145 | 28042.0 | 50411.0 | 22369.0 | adjusted (other) |
| EF-C-0007157 | 106317.0 | 57998.0 | -48319.0 | capped at 99th pct |
| EF-C-0007157 | 57998.0 | 106317.0 | 48319.0 | adjusted (other) |
| EF-C-0007158 | 62474.0 | 49167.0 | -13307.0 | capped at 99th pct |
| EF-C-0007158 | 49167.0 | 62474.0 | 13307.0 | adjusted (other) |
| EF-C-0007246 | 59190.0 | 156726.0 | 97536.0 | adjusted (other) |
| EF-C-0007246 | 59190.0 | 74410.0 | 15220.0 | adjusted (other) |
| EF-C-0007246 | 156726.0 | 59190.0 | -97536.0 | capped at 99th pct |
| EF-C-0007246 | 156726.0 | 74410.0 | -82316.0 | capped at 99th pct |
| EF-C-0007246 | 74410.0 | 59190.0 | -15220.0 | capped at 99th pct |
| EF-C-0007246 | 74410.0 | 156726.0 | 82316.0 | adjusted (other) |
| EF-C-0007247 | 61061.0 | 164569.0 | 103508.0 | adjusted (other) |
| EF-C-0007247 | 164569.0 | 61061.0 | -103508.0 | capped at 99th pct |
| EF-C-0007248 | 79236.0 | 99109.0 | 19873.0 | adjusted (other) |
| EF-C-0007248 | 79236.0 | 120157.0 | 40921.0 | adjusted (other) |
| EF-C-0007248 | 99109.0 | 79236.0 | -19873.0 | capped at 99th pct |
| EF-C-0007248 | 99109.0 | 120157.0 | 21048.0 | adjusted (other) |
| EF-C-0007248 | 120157.0 | 79236.0 | -40921.0 | capped at 99th pct |
| EF-C-0007248 | 120157.0 | 99109.0 | -21048.0 | capped at 99th pct |
| EF-C-0007262 | 70808.0 | 57844.0 | -12964.0 | capped at 99th pct |
| EF-C-0007262 | 57844.0 | 70808.0 | 12964.0 | adjusted (other) |
| EF-C-0007263 | 94267.0 | 68005.0 | -26262.0 | capped at 99th pct |
| EF-C-0007263 | 68005.0 | 94267.0 | 26262.0 | adjusted (other) |
| EF-C-0007264 | 116153.0 | 40913.0 | -75240.0 | capped at 99th pct |
| EF-C-0007264 | 40913.0 | 116153.0 | 75240.0 | adjusted (other) |
| EF-C-0007265 | 56687.0 | 49336.0 | -7351.0 | capped at 99th pct |
| EF-C-0007265 | 49336.0 | 56687.0 | 7351.0 | adjusted (other) |
| EF-C-0007277 | 62455.0 | 119229.0 | 56774.0 | adjusted (other) |
| EF-C-0007277 | 119229.0 | 62455.0 | -56774.0 | capped at 99th pct |
| EF-C-0007278 | 51197.0 | 95268.0 | 44071.0 | adjusted (other) |
| EF-C-0007278 | 95268.0 | 51197.0 | -44071.0 | capped at 99th pct |
| EF-C-0007288 | 43034.0 | 93722.0 | 50688.0 | adjusted (other) |
| EF-C-0007288 | 93722.0 | 43034.0 | -50688.0 | capped at 99th pct |
| EF-C-0007289 | 52465.0 | 17592.0 | -34873.0 | capped at 99th pct |
| EF-C-0007289 | 17592.0 | 52465.0 | 34873.0 | adjusted (other) |
| EF-C-0007324 | 25187.0 | 64322.0 | 39135.0 | adjusted (other) |
| EF-C-0007324 | 64322.0 | 25187.0 | -39135.0 | capped at 99th pct |
| EF-C-0007325 | 66351.0 | 23875.0 | -42476.0 | capped at 99th pct |
| EF-C-0007325 | 23875.0 | 66351.0 | 42476.0 | adjusted (other) |
| EF-C-0007338 | 90986.0 | 69353.0 | -21633.0 | capped at 99th pct |
| EF-C-0007338 | 90986.0 | 63609.0 | -27377.0 | capped at 99th pct |
| EF-C-0007338 | 69353.0 | 90986.0 | 21633.0 | adjusted (other) |
| EF-C-0007338 | 69353.0 | 63609.0 | -5744.0 | capped at 99th pct |
| EF-C-0007338 | 63609.0 | 90986.0 | 27377.0 | adjusted (other) |
| EF-C-0007338 | 63609.0 | 69353.0 | 5744.0 | adjusted (other) |
| EF-C-0007339 | 50985.0 | 62892.0 | 11907.0 | adjusted (other) |
| EF-C-0007339 | 50985.0 | 166455.0 | 115470.0 | adjusted (other) |
| EF-C-0007339 | 62892.0 | 50985.0 | -11907.0 | capped at 99th pct |
| EF-C-0007339 | 62892.0 | 166455.0 | 103563.0 | adjusted (other) |
| EF-C-0007339 | 166455.0 | 50985.0 | -115470.0 | capped at 99th pct |
| EF-C-0007339 | 166455.0 | 62892.0 | -103563.0 | capped at 99th pct |
| EF-C-0007340 | 47108.0 | 78050.0 | 30942.0 | adjusted (other) |
| EF-C-0007340 | 47108.0 | 38685.0 | -8423.0 | capped at 99th pct |
| EF-C-0007340 | 78050.0 | 47108.0 | -30942.0 | capped at 99th pct |
| EF-C-0007340 | 78050.0 | 38685.0 | -39365.0 | capped at 99th pct |
| EF-C-0007340 | 38685.0 | 47108.0 | 8423.0 | adjusted (other) |
| EF-C-0007340 | 38685.0 | 78050.0 | 39365.0 | adjusted (other) |
| EF-C-0007357 | 146368.0 | 93151.0 | -53217.0 | capped at 99th pct |
| EF-C-0007357 | 93151.0 | 146368.0 | 53217.0 | adjusted (other) |
| EF-C-0007358 | 86119.0 | 34178.0 | -51941.0 | capped at 99th pct |
| EF-C-0007358 | 34178.0 | 86119.0 | 51941.0 | adjusted (other) |
| EF-C-0007363 | 124957.0 | 70385.0 | -54572.0 | capped at 99th pct |
| EF-C-0007363 | 70385.0 | 124957.0 | 54572.0 | adjusted (other) |
| EF-C-0007364 | 227174.0 | 244677.0 | 17503.0 | adjusted (other) |
| EF-C-0007364 | 244677.0 | 227174.0 | -17503.0 | capped at 99th pct |
| EF-C-0007389 | 249972.0 | 122899.0 | -127073.0 | capped at 99th pct |
| EF-C-0007389 | 122899.0 | 249972.0 | 127073.0 | adjusted (other) |
| EF-C-0007390 | 87310.0 | 64557.0 | -22753.0 | capped at 99th pct |
| EF-C-0007390 | 64557.0 | 87310.0 | 22753.0 | adjusted (other) |
| EF-C-0007404 | 89177.0 | 59653.0 | -29524.0 | capped at 99th pct |
| EF-C-0007404 | 59653.0 | 89177.0 | 29524.0 | adjusted (other) |
| EF-C-0007405 | 94159.0 | 71393.0 | -22766.0 | capped at 99th pct |
| EF-C-0007405 | 71393.0 | 94159.0 | 22766.0 | adjusted (other) |
| EF-C-0007412 | 32040.0 | 41136.0 | 9096.0 | adjusted (other) |
| EF-C-0007412 | 41136.0 | 32040.0 | -9096.0 | capped at 99th pct |
| EF-C-0007413 | 88295.0 | 129975.0 | 41680.0 | adjusted (other) |
| EF-C-0007413 | 129975.0 | 88295.0 | -41680.0 | capped at 99th pct |
| EF-C-0007414 | 93241.0 | 81677.0 | -11564.0 | capped at 99th pct |
| EF-C-0007414 | 81677.0 | 93241.0 | 11564.0 | adjusted (other) |
| EF-C-0007415 | 196066.0 | 92127.0 | -103939.0 | capped at 99th pct |
| EF-C-0007415 | 92127.0 | 196066.0 | 103939.0 | adjusted (other) |
| EF-C-0003813 | -64479.0 | NaN | — | negative -> NaN |
| EF-C-0004288 | -43909.0 | NaN | — | negative -> NaN |

---

## C. Policy ID Coverage

Checks for `policy_id` values that appear in the severity file but have
no matching record in the frequency file. These are **orphaned claims** —
they cannot be linked back to a policy exposure row.

### C.1 Coverage summary

| Version | Unique freq IDs | Unique sev IDs | Covered (both) | Orphaned (sev only) | Orphaned % |
| --- | --- | --- | --- | --- | --- |
| RAW | 90,558 | 6,993 | 6,939 | 54 | 0.8% |
| CLEANED | 90,781 | 6,918 | 6,879 | 39 | 0.6% |

### C.2 Orphaned policies in cleaned files (with claim counts)

| policy_id | Claims in sev |
| --- | --- |
| EF-025700 | 1 |
| EF-028268_???3303 | 1 |
| EF-064334 | 1 |
| EF-085793_???6763 | 1 |
| EF-169926_???4703 | 1 |
| EF-194033_???2401 | 1 |
| EF-204938 | 1 |
| EF-216768_???2099 | 1 |
| EF-216970 | 1 |
| EF-224008_???8332 | 1 |
| EF-282604_???1573 | 1 |
| EF-336186_???5882 | 1 |
| EF-339813_???4655 | 1 |
| EF-347049 | 1 |
| EF-358094_???9014 | 1 |
| EF-362534_???4446 | 1 |
| EF-504143_???5610 | 1 |
| EF-540637_???7786 | 1 |
| EF-606771 | 1 |
| EF-634071_???4370 | 1 |
| EF-636967_???9285 | 1 |
| EF-674511_???9072 | 1 |
| EF-682717_???4254 | 1 |
| EF-715958 | 1 |
| EF-734935 | 1 |
| EF-781289_???8807 | 1 |
| EF-810415 | 1 |
| EF-846547_???1916 | 1 |
| EF-849088_???6377 | 1 |
| EF-867726_???5407 | 1 |
| EF-881996_???5567 | 1 |
| EF-885673_???7397 | 1 |
| EF-941560 | 1 |
| EF-973323 | 1 |
| EF-977640_???6171 | 1 |
| EF-985633_???2118 | 1 |
| EF-988067_???7302 | 1 |
| EF-996273_???1617 | 1 |
| MP-0208 | 1 |

> Orphaned policies with prefix `MP-` were assigned placeholder IDs during
> cleaning (originally `NaN`). These are expected and not data errors.

---

## D. Full Audit Trail

```
[15:39:23]  
[15:39:23]  ====================================================================
[15:39:23]  Loading files
[15:39:23]  ====================================================================
[15:39:23]    raw  freq :   95,062 rows x  9 cols
[15:39:23]    raw  sev  :    8,272 rows  x 11 cols
[15:39:23]    clean freq:   95,062 rows x  9 cols
[15:39:23]    clean sev :    8,162 rows  x 11 cols
[15:39:23]  
[15:39:23]  ====================================================================
[15:39:23]  CHECK A — NaN Audit (cleaned files)
[15:39:23]  ====================================================================
[15:39:23]  
  cleaned_freq
[15:39:23]  
  cleaned_sev
[15:39:23]  
[15:39:23]  ====================================================================
[15:39:23]  CHECK B — Claim Amount Reconciliation (raw sev vs cleaned sev)
[15:39:23]  ====================================================================
[15:39:23]    B1: Comparing total claim_amount (raw vs cleaned)
[15:39:23]      Raw total  (excl. negatives) :       738,762,470.79
[15:39:23]      Raw total  (incl. negatives) :       737,830,531.79
[15:39:23]      Cleaned total                :       688,799,002.02
[15:39:23]      Difference vs raw (no-neg)   :       -49,963,468.77  (-6.763%)
[15:39:23]    B2: Checking for NaN in cleaned claim_amount
[15:39:23]    B3: Row-level breakdown of changed claim_amount values
[15:39:23]  
[15:39:23]  ====================================================================
[15:39:23]  CHECK C — Policy ID Coverage (policy_id in sev but not in freq)
[15:39:23]  ====================================================================
[15:39:23]  
  RAW files
[15:39:23]      Unique policy_id in freq : 90,558
[15:39:23]      Unique policy_id in sev  : 6,993
[15:39:23]      Covered (in both)        : 6,939
[15:39:23]      Orphaned (sev only)      : 54  (0.8% of sev policies)
[15:39:23]  
  CLEANED files
[15:39:24]      Unique policy_id in freq : 90,781
[15:39:24]      Unique policy_id in sev  : 6,918
[15:39:24]      Covered (in both)        : 6,879
[15:39:24]      Orphaned (sev only)      : 39  (0.6% of sev policies)
[15:39:24]  
[15:39:24]  ====================================================================
[15:39:24]  Writing audit report
[15:39:24]  ====================================================================
```

---

*Report generated by `audit_equipment_claims.py`*
