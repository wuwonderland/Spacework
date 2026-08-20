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
