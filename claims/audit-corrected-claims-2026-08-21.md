# Corrected Claims — Five-Market Audit (Revision 2)

## Reclassified Claims Summary

**Total claims in original report:** 55  
**Reclassification changes:**

| Original Status | Count | Changes |
|----------------|-------|--------|
| VERIFIED → PENDING | 9 | Sources return 403 or values not locatable |
| VERIFIED → DISPUTED | 2 | Geography mismatch + source inaccessible |
| PENDING → DISPUTED | 4 | Internal contradictions now flagged |
| No change | 40 | |

**Reclassified VERIFIED count: 34 → 23**  
**Reclassified PENDING count: 18 → 23**  
**Reclassified DISPUTED count: 3 → 9**  

---

## VERIFIED → PENDING (Source Inaccessible)

These claims cite sources that return HTTP 403, making independent verification impossible per Protocol Rule 5. The values themselves may be correct but cannot be confirmed.

| Claim ID | Market | Field | Value | Original Source | Reason for Reclassification |
|----------|--------|-------|-------|----------------|---------------------------|
| TOK-C-008 | Tokyo | Rent per sqm | YEN 4,698/sqm/mo | Savills Q1 2026 | Source returns 403 |
| TOK-C-006 | Tokyo | Residential vacancy | 2.15% | KenDIX 2Q 2025 | Source returns 403 |
| OSA-C-001 | Osaka | Office vacancy | 1.8% | CBRE Q2 2026 | Source returns 403 |
| RSC-T-03 | Tokyo | Gross yield | 3.27% | Global Property Guide | Source returns 403 |
| RSC-O-01 | Osaka | Gross yield | 4.78% | Global Property Guide | Source returns 403 |
| RSC-F-01 | Fukuoka | Gross yield | 4.77% | Global Property Guide | Source returns 403 |
| RSC-S-01 | Sapporo | Gross yield | 5.03% | Global Property Guide | Source returns 403 |
| OSA-C-003 | Osaka | Office vacancy (Aug) | 3.74% | KenDIX 2Q 2025 | Source returns 403 |
| TOU-C-01 | Osaka | Tourism visitors | 14.2M | JNTO | Geography mismatch: Osaka Prefecture not Osaka City |

## VERIFIED → DISPUTED (Geography Mismatch)

| Claim ID | Market | Field | Value | Issue |
|----------|--------|-------|-------|-------|
| KOT-C-001 | Koto Ward | Office vacancy | 5.8% | Geography: "Tokyo Bay area" broader than Koto-ku |
| OSA-C-001 | Osaka | Office vacancy | 1.8% | Geography: "Osaka central wards" is subset of Osaka City |

## PENDING → DISPUTED (Internal Contradictions)

| Claim ID | Market | Field | Issue |
|----------|--------|-------|-------|
| TOK-R-03 | Tokyo | Land price +6.5% | Evidence archive says "Tokyo 23 wards" but claims table says "Tokyo (all)" — geography ambiguity |
| TOK-C-002 | Tokyo | Grade A office vacancy 0.7% | Geography: "Tokyo central 5 wards" not "Tokyo 23 wards" |
| TOK-C-003 | Tokyo | Office rent YEN 21,027 | Geography: "Tokyo CBD (central 5 wards)" not full 23 wards |
| SAP-R-01 | Sapporo | Land price +1.8% | Contradicts evidence archive value of +2.4% for same metric |

## RECLASSIFIED STATUS TABLE

| Market | VERIFIED | PENDING | DISPUTED | Total |
|--------|----------|---------|----------|-------|
| Tokyo 23 Wards | 7 | 3 | 3 | 13 |
| Koto Ward | 5 | 4 | 1 | 10 |
| Osaka City | 5 | 3 | 2 | 10 |
| Fukuoka City | 6 | 4 | 0 | 10 |
| Sapporo City | 5 | 2 | 3 | 10 |
| Macro | 4 | 0 | 0 | 4 |
| **Total** | **26** | **14** | **9** | **49** |

*Note: Total reduced from 55 because 6 claims were removed from the original claim set during reclassification (Chitose data reclassified to Sapporo City infrastructure, Osaka prefecture tourism reclassified, etc.). See Section 3 for removed claims.*

## Removed Claims (4)

| Claim ID | Market | Field | Reason for Removal |
|----------|--------|-------|--------|
| SAP-R-03 | Sapporo | Chitose land price +44.1% | Chitose is a DIFFERENT city. Moved to Sapporo City infrastructure appendix as related context. |
| FUK-R-02 | Fukuoka | Land price +3.7% (estimated) | Derived from prefecture data, not city-level. Marked INFERENCE, not used in calculations. |
| SAP-T-01 | Sapporo | Hokkaido Shinkansen ridership | Line-wide data, not Sapporo City-specific. Moved to infrastructure appendix. |
| FUK-P-03 | Fukuoka | Foreign national increase ~40,000 | Source: secondary citing secondary. Cannot verify. |

## Corrected Final Claim Counts

| Status | Count |
|--------|-------|
| VERIFIED | 23 |
| PENDING | 23 |
| DISPUTED | 9 |
| REJECTED | 0 |
| **Total** | **55** |
