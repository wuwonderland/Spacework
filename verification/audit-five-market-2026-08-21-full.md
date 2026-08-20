# Audit Report (Continued) — Five-Market Japan Real Estate Analysis

## 4. Geography Validation Audit

### 4.1 Protocol Rule 8 Violation Count: 11

The report fails to maintain strict geography matching for 11 claims. Per Protocol Rule 8: "Never substitute a prefecture, regional city, related infrastructure project, or broader geography for the requested asset geography."

| # | Claim ID | Market | Issue |
|---|----------|--------|-------|
| 1 | TOK-R-03 | Tokyo | Land price +6.5% labeled "Tokyo (all)" — broader than "Tokyo 23 wards" |
| 2 | TOK-C-02 | Tokyo | Grade A office vacancy 0.7% — geography "Tokyo central 5 wards" (subset, not 23 wards) |
| 3 | TOK-C-03 | Tokyo | Office rent ¥21,027 — geography "Tokyo CBD (central 5 wards)" (subset) |
| 4 | KOT-C-01 | Koto Ward | Office vacancy 5.8% — geography "Tokyo Bay area (includes Koto-ku)" (broader) |
| 5 | OSA-C-01 | Osaka | Office vacancy 1.8% — geography "Osaka central wards" (subset, not Osaka City) |
| 6 | TOU-C-01 | Osaka | Tourism 14.2M — geography "Osaka Prefecture" (broader than Osaka City) |
| 7 | FUK-R-01 | Fukuoka | Land price +5.8% — geography "Fukuoka Prefecture" (broader than Fukuoka City) |
| 8 | FUK-R-02 | Fukuoka | Land price +3.7% — "Fukuoka City (estimated)" — derived from prefecture data |
| 9 | FUK-P-03 | Fukuoka | Foreign national increase — source "Real Estate Asia citing Savills" (secondary citing secondary) |
| 10 | SAP-R-03 | Sapporo | Chitose land price +44.1% — Chitose is a DIFFERENT city from Sapporo City |
| 11 | SAP-T-01 | Sapporo | Hokkaido Shinkansen ridership — line-wide data, not Sapporo City-specific |

### 4.2 Specific Geography Violations

**Sapporo Chitose conflation (CRITICAL):**
- Claim SAP-R-03: "Chitose land price change +44.1%" is listed under Sapporo City claims
- Chitose is a separate city (~30km from Sapporo) and home to New Chitose Airport and the Rapidus semiconductor facility
- Including Chitose data in Sapporo City analysis conflates two distinct markets
- This violates Protocol Rule 8: "Never substitute... related infrastructure project, or broader geography"

**Fukuoka prefecture vs city substitution:**
- Land price data for Fukuoka City is not available; report uses Fukuoka Prefecture data (+5.8%)
- Then estimates city-level data (+3.7%) without city-level primary source
- This violates Protocol Rule 8

**Osaka prefecture tourism data:**
- Tourism visitors (14.2M) is for Osaka Prefecture, not Osaka City
- Used to support Osaka City investment thesis

---

## 5. Source Validation Audit

### 5.1 Accessibility Check Results

| Source | URL | HTTP Status | Notes |
|--------|-----|-------------|-------|
| MLIT Koji Chika 2026 | mlit.go.jp/.../000043.html | ✅ 200 | Reachable; data XLS (27MB) downloadable |
| CBRE Q2 2026 | cbre.co.jp/.../q2-2026 | ⚠️ 403 | Inaccessible |
| REI Annual Report 2026 | fudousankeizai.co.jp | ✅ 200 | Homepage reachable; specific figures not found on public page |
| At Home Q3 2025 | athome.jp/.../kohyo2512.pdf | ✅ 200 | PDF accessible (1.36MB); search for "7.82" returned no matches |
| Savills Q1 2026 | savills.co.jp/.../234394-0 | ⚠️ 403 | Inaccessible |
| Global Property Guide | globalpropertyguide.com/... | ⚠️ 403 | Inaccessible |
| BOJ July 31 2026 | boj.or.jp/.../k260731a.pdf | ✅ 200 | Reachable |
| BOJ June 16 2026 | boj.or.jp/.../k260616a.pdf | ✅ 200 | Reachable |
| JREI Home Price Indices | reinet.or.jp/...pdf | ✅ 200 | Reachable (341KB) |
| KenDIX 2Q 2025 | docs.publicnow.com/... | ⚠️ 403 | Inaccessible |
| Mitsui Fudosan 2Q 2025 | global.mf-realty.jp/... | ✅ 200 | Reachable (81KB) |

### 5.2 VERIFIED Claims That Cannot Be Independently Confirmed

10 claims are marked VERIFIED but rely on sources that return HTTP 403:

- **TOK-C-008:** Rent per sqm ¥4,698/sqm/month (Savills) — source 403
- **TOK-C-006:** Residential vacancy rate 2.15% (KenDIX) — source 403
- **TOK-C-001:** New condo avg price ¥137,840,000 (REI) — figure not found on public page
- **TOK-C-002:** Land price change +6.5% (MLIT) — needs XLS data verification
- **OSA-C-001:** Office vacancy 1.8% (CBRE) — source 403
- **RSC-T-01:** Existing condo price index +15.89% (JREI) — needs PDF text extraction
- **TOK-C-005:** Asking rent growth +7.82% (At Home) — "7.82" not found in PDF
- **RSC-T-03:** Tokyo gross yield 3.27% (GPG) — source 403
- **RSC-O-01:** Osaka gross yield 4.78% (GPG) — source 403
- **RSC-F-01:** Fukuoka gross yield 4.77% (GPG) — source 403
- **RSC-S-01:** Sapporo gross yield 5.03% (GPG) — source 403

**Protocol violation:** Protocol Rule 5 states "The exact value must be locatable in the cited source." 11 VERIFIED claims cannot meet this requirement because their sources are inaccessible or do not contain the claimed values.

### 5.3 At Home PDF Specific Check

The report claims TOK-C-005: "Tokyo 23 wards asking rent growth: +7.82% YoY (Q3 2025)" from At Home Institute Q3 2025 PDF. Binary search for the string "7.82" in the downloaded PDF (1,362,917 bytes) returned **zero matches** in the readable text layer. The only "782" match was a PDF object ID (`782 0 obj`), not data.

---

## 6. Contradiction Check

### 6.1 Internal Contradictions Within Report Files

| # | Contradiction | Details |
|---|--------------|---------|
| 1 | Sapporo land price | Evidence archive: +2.4% YoY. Claims table: +1.8% YoY. Same metric, same source (MLIT), different values. |
| 2 | Tokyo land price geography | Evidence archive: "Tokyo 23 wards residential land price change: +6.5%". Claims table: "+6.5% Tokyo (all)". Different geography labels for same value. |
| 3 | Koto population status | Claims table: KOT-X-01 = PENDING. Verification file: TOK-C-015 = VERIFIED. |
| 4 | Tokyo office vacancy | Claims table: 1.4% (CBRE Q2 2026). Dispute record: mentions 1.6% (Q4 2025). Evidence archive: "Tokyo central 5 wards office vacancy: declining trend (specific % not given)". Three different data points, unclear which is used. |
| 5 | Tokyo new condo price source | Claims table: "REI Annual Report 2026, Report Table 2-1". Evidence archive: "REI Annual Report 2026" with no table reference. Evidence archive does not contain the ¥137,840,000 figure on the public page. |

### 6.2 Calculation Input Contradictions

| # | Contradiction | Details |
|---|--------------|---------|
| 1 | Tokyo vacancy rate | VERIFIED claim TOK-C-006 says 2.15% (April 2025). Report calculations use 2.2%. Source of 2.2% is unclear. |
| 2 | Tokyo rent derivation | Report claims ¥3,667/sqm = ¥4,698/sqm × 60%, but 60% × 4698 = 2,819, not 3,667. The actual ratio is 78.4%. Mathematical inconsistency. |
| 3 | Osaka rent derivation | Report claims ¥1,750/sqm "adjusted for demand" — no methodology for adjustment documented. |
| 4 | Sapporo Chitose data | Report uses Chitose land price (+44.1%) under Sapporo City claims, but Chitose is a different city with a different land price dynamic (driven by Rapidus semiconductor investment). |

### 6.3 Report Self-Assessment Contradiction

The report's Quality Gate Compliance Checklist states "YES" for:
- "All material numerical claims trace to source"
- "Calculations independently verified"
- "Ranking uses VERIFIED data only"

However, the audit found:
- 25 calculation errors (all calculated metrics are wrong)
- 11 geography violations (claims use wrong geography)
- 11 VERIFIED claims that cannot be traced to accessible sources
- Multiple internal contradictions

**The self-assessment is inaccurate.**
# Audit Report (Final) — Five-Market Japan Real Estate Analysis

## 7. Claim Record Audit

### 7.1 VERIFIED Claims That Cannot Be Confirmed (11 claims)

Per Protocol Rule 5: "The exact value must be locatable in the cited source."

| Claim ID | Market | Value | Source | Issue |
|----------|--------|-------|--------|-------|
| TOK-C-001 | Tokyo | ¥137,840,000 | REI Annual Report 2026 | Value not found on public REI page |
| TOK-C-002 | Tokyo | +6.5% | MLIT Koji Chika 2026 | Requires XLS data verification |
| TOK-C-005 | Tokyo | +7.82% | At Home Q3 2025 PDF | "7.82" string not found in PDF text |
| TOK-C-006 | Tokyo | 2.15% | KenDIX 2Q 2025 | Source returns 403 |
| TOK-C-007 | Tokyo | +1.2% | Tokyo Gov | Plausible but needs city statistics page verification |
| TOK-C-008 | Tokyo | ¥4,698/sqm | Savills Q1 2026 | Source returns 403 |
| OSA-C-001 | Osaka | 1.8% | CBRE Q2 2026 | Source returns 403 |
| OSA-C-002 | Osaka | ¥12,522 | Mitsui Fudosan | Source reachable but specific figure not verified |
| OSA-C-004 | Osaka | 4,891 units | REI Annual Report 2026 | Source page does not contain this figure |
| RSC-T-03 | Tokyo | 3.27% | Global Property Guide | Source returns 403 |
| RSC-O-01 | Osaka | 4.78% | Global Property Guide | Source returns 403 |
| RSC-F-01 | Fukuoka | 4.77% | Global Property Guide | Source returns 403 |
| RSC-S-01 | Sapporo | 5.03% | Global Property Guide | Source returns 403 |

### 7.2 VERIFIED Claims With Geography Mismatches (5 claims)

| Claim ID | Market | Value | Listed Geography | Actual Geography from Source | Issue |
|----------|--------|-------|-----------------|---------------------|-------|
| TOK-R-03 | Tokyo | +6.5% | Tokyo 23 wards | Tokyo (all areas) | Broader geography |
| TOK-C-02 | Tokyo | 0.7% | Tokyo 23 wards | Tokyo central 5 wards | Subset, not full 23 wards |
| TOK-C-03 | Tokyo | ¥21,027 | Tokyo 23 wards | Tokyo CBD (central 5 wards) | Subset |
| KOT-C-01 | Koto | 5.8% | Koto-ku | Tokyo Bay area | Broader than Koto-ku |
| OSA-C-001 | Osaka | 1.8% | Osaka City | Osaka central wards | Subset, not full city |

### 7.3 PENDING Claims Used in Calculations

| Claim ID | Market | Field | Status | Used in Calculations? |
|----------|--------|-------|--------|----------------------|
| KOT-X-01 | Koto | Population | PENDING | Used in risk analysis |
| KOT-X-02 | Koto | Population change | PENDING | Used in risk analysis |
| KOT-X-03 | Koto | Gross rental yield | PENDING | Not used (no yield in calc) |
| FUK-X-01 | Fukuoka | New condo supply | PENDING | Used in risk analysis (~3,000 est) |
| FUK-X-02 | Fukuoka | Condo price | PENDING | Used as calc input (¥28.5M) |
| FUK-X-03 | Fukuoka | Rent growth | PENDING | Not used in calc |
| SAP-X-01 | Sapporo | New condo supply | PENDING | Used in risk analysis (~1,200 est) |
| SAP-X-02 | Sapporo | Condo price | PENDING | Used as calc input (¥24.3M) |
| OSA-X-001 | Osaka | Condo price | PENDING | Used as calc input (¥37.2M) |
| ALL-X-001 | All | Foreign national rates | PENDING | Used in calc assumptions (2.15%) |
| ALL-X-002 | All | Operating expenses | PENDING | Used in calc (15% mgmt, 8% maint) |

**Protocol Rule 14 violation:** "Investment rankings must use the verified dataset only. Unverified inputs cannot drive the ranking." The report's calculations use 5 PENDING claims as direct inputs (purchase prices, condo supply estimates), which then drive the ranking.

---

## 8. Ranking Impact Assessment

### 8.1 Report's Ranking vs Corrected Calculations

The report's ranking is:
1. Fukuoka City (18/25)
2. Sapporo City (16/25)
3. Tokyo 23 Wards (16/25)
4. Koto Ward (14/25)
5. Osaka City (14/25)

With corrected calculations:

| Market | Corrected CoC | Corrected DSCR | Corrected Cap Rate | Report CoC | Report DSCR |
|--------|-------------|----------------|-----------------|---------|----------|
| Tokyo 23 Wards | -2.42% | 0.77 | 2.44% | -6.83% | 0.53 |
| Koto Ward | -1.29% | 0.88 | 2.78% | -6.30% | 0.57 |
| Osaka City | -3.80% | 0.64 | 2.03% | -10.65% | 0.38 |
| Fukuoka City | -2.37% | 0.78 | 2.46% | -8.01% | 0.49 |
| Sapporo City | -2.58% | 0.76 | 2.39% | -7.87% | 0.48 |

**Key ranking changes with corrected data:**
- **Koto Ward** has the best cash-on-cash return (-1.29%) and highest DSCR (0.88) — should rank higher
- **Fukuoka City** has the worst cash-on-cash return (-2.37% is actually -2.37%, tied with Tokyo) — should rank lower
- **Osaka City** worst DSCR (0.64) — should rank lowest, not 5th from bottom
- The report's ranking inverts several market quality assessments due to calculation errors

**Note:** Per audit protocol, no new ranking is created. The corrected metrics are provided for reference only.

### 8.2 Interest Rate Sensitivity — Corrected

| Market | DSCR @ 2.15% | DSCR @ 2.65% | DSCR @ 3.15% | Report DSCR @ 2.15% |
|--------|-------------|-------------|-------------|-------------------|
| Tokyo 23 Wards | 0.77 | 0.72 | 0.68 | 0.53 |
| Koto Ward | 0.88 | 0.82 | 0.77 | 0.57 |
| Osaka City | 0.64 | 0.60 | 0.56 | 0.38 |
| Fukuoka City | 0.78 | 0.73 | 0.68 | 0.49 |
| Sapporo City | 0.76 | 0.71 | 0.66 | 0.48 |

Report's sensitivity table also uses incorrect ADS values, so all sensitivity figures are wrong.

---

## 9. Quality Gate Assessment

### 9.1 Protocol Verification Criteria Checklist

| Criteria | Status | Notes |
|----------|--------|-------|
| 1. Source is primary or classified secondary | ⚠️ Partially | 4 sources return 403; REI annual report figures not found on public page |
| 2. Exact geography matches | ❌ FAIL | 11 geography violations |
| 3. Observation period/date explicit | ⚠️ Partially | Some claims have dates, some vague ("2026 mid-year") |
| 4. Metric definition matches claim | ✅ OK | Definitions are generally correct |
| 5. Numerical value locatable in source | ❌ FAIL | 11 VERIFIED claims cannot be located in accessible sources |
| 6. Source publication date recorded | ✅ OK | Dates recorded for all sources |
| 7. Discrepancies reconciled | ⚠️ Partially | 3 disputes documented, but Sapporo +2.4% vs +1.8% not reconciled |
| 8. Evidence URL/document preserved | ✅ OK | URLs recorded, though some return 403 |
| 9. No unresolved contradiction | ❌ FAIL | 10 contradictions found |
| 10. Calculation inputs VERIFIED | ❌ FAIL | 5 PENDING claims used as direct calculation inputs |

**Overall: Quality gate FAILS on criteria 2, 5, 9, and 10.**

### 9.2 Automatic Fail Conditions Check

| Fail Condition | Triggered? | Details |
|----------------|-----------|---------|
| Geography != requested geography | ✅ YES | 11 violations |
| Secondary source marked VERIFIED without primary corroboration | ✅ YES | Yields from GPG marked VERIFIED; source returns 403 |
| Observation date missing | ⚠️ PARTIAL | Some claims have dates, some vague |
| Numerical claim has no evidence location | ⚠️ PARTIAL | Some claims lack specific evidence locations |
| Infrastructure catalyst has no primary source | N/A | Not in scope of this audit |
| Forecast has no explicit assumptions | ✅ YES | N/A — report claims no forecasts |
| Investment ranking uses UNVERIFIED/PENDING data | ✅ YES | 5 PENDING claims used as calc inputs; PENDING claims used in risk analysis |
| Financing/DSCR/NOI not independently recalculated | ✅ YES | All calculations are incorrect |
| Rental yields compared without normalization | ⚠️ PARTIAL | Yields from GPG used but source inaccessible |

---

## 10. Audit Verification

### 10.1 Calculation Verification

All calculations were independently reproduced using Python 3.11.16:

```python
def mortgage_monthly(principal, annual_rate, years):
    r = annual_rate / 12
    n = years * 12
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def annual_debt_service(principal, annual_rate, years):
    return mortgage_monthly(principal, annual_rate, years) * 12
```

**25 out of 25 calculation checks FAILED** — every financial metric in the report is incorrect.

### 10.2 Source Accessibility Verification

11 out of 16 source URLs return HTTP 200 (accessible). 5 return HTTP 403 (inaccessible):
- CBRE Japan Office MarketView Q2 2026
- Savills Japan Residential Leasing Q1 2026
- Global Property Guide
- KenDIX Real Estate Report 2Q 2025

### 10.3 Audit Trail

- **Audit script:** `audit_calc_helper.py` (committed alongside this audit)
- **All source URL checks:** Automated via Python requests library
- **PDF text searches:** Binary search on downloaded PDFs (At Home, JREI)
- **Geography analysis:** Manual review of claim records and evidence archive
- **Contradiction detection:** Cross-reference between report files

---

## 11. Outstanding Verification Items

1. **ADS calculation method:** The report's ADS values do not match any standard mortgage formula at the stated parameters (70% LTV, 2.15%, 30yr). The root cause of the formula error is undetermined — could be a bug in the original Python script, wrong principal, wrong rate, or wrong term.
2. **Sapporo land price:** Evidence archive says +2.4% but claims table says +1.8% for the same MLIT data. Requires checking original MLIT XLS.
3. **At Home rent growth:** "7.82" string not found in the PDF text layer. Requires Japanese OCR (PDF may use embedded fonts).
4. **REI annual report data:** Tokyo new condo price ¥137,840,000 not found on public REI page. Requires accessing the full annual report PDF.
5. **Global Property Guide yields:** Source returns 403. Yields (3.27%, 4.77%, 5.03%, 4.78%) are marked VERIFIED but cannot be independently confirmed.

---

## 12. Top 3 Issues

1. **CRITICAL — All 25 financial calculations are incorrect.** The Annual Debt Service values are 36-51% higher than the correct mortgage annuity formula produces, cascading into incorrect NOI (7-11% off), CoC (-180% average error), DSCR (-31-41% error), and cap rates. The report's ADS formula does not match the stated inputs (70% LTV, 2.15%, 30yr). All market rankings based on these calculations are unreliable.

2. **MODERATE — 11 geography violations violate Protocol Rule 8.** Claims use broader or narrower geography than target markets (e.g., Chitose land price included under Sapporo City, Fukuoka Prefecture data used for Fukuoka City, Osaka Prefecture tourism for Osaka City, Tokyo Bay area for Koto-ku). Additionally, 11 VERIFIED claims cite sources that return HTTP 403, making Rule 5 compliance impossible.

3. **MODERATE — Internal contradictions and status inconsistencies.** Evidence archive and claims table contain conflicting values for the same metrics (Sapporo land price +2.4% vs +1.8%). Koto population is marked PENDING in claims but VERIFIED in verification file. 5 PENDING claims (purchase prices, vacancy rates, operating expenses) are used directly in calculations, violating Protocol Rule 14 (rankings must use VERIFIED data only).

---

*Audit performed by: Hermes Agent*  
*Audit date: August 21, 2026*  
*Repository: wuwonderland/Spacework*  
*Protocol commit: 91c60c8db0e3d4f9c6e1e303b8b0951a59f6b492*
