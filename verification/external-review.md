# External Review Queue — Five-Market Audit (2026-08-21)

**Reviewed branch:** `audit/2026-08-21-five-market-calculations`  
**Reviewed commit:** `b0223a5`  
**Reviewer:** ChatGPT (pending)  
**Status:** AWAITING REVIEW  

---

## Review Summary

### Overall Status
AWAITING REVIEW — Not yet reviewed by ChatGPT.

### Material Errors Found (Audit-level)

| # | Type | Severity | Issue |
|---|------|----------|-------|
| 1 | Calculation | BLOCKER | All 25 financial calculations incorrect (ADS 36-51% too high) |
| 2 | Geography | MAJOR | 11 geography violations (Rule 8) |
| 3 | Source | MAJOR | 11 VERIFIED claims from 403 sources (GPG, KenDIX, Savills, CBRE) |
| 4 | Contradiction | MAJOR | 10 internal contradictions between report files |
| 5 | Process | MAJOR | 5 PENDING claims used as calc inputs (Rule 14 violation) |
| 6 | Self-assessment | MINOR | Report claims all quality gates passed — inaccurate |

### Reviewer Questions (Pre-loaded)

1. **Calculations:** Does the report's ADS formula `P × [r(1+r)^n] / [(1+r)^n - 1]` with P=¥46.2M, r=2.15%/12, n=360 produce ¥2,846,352? (Correct: ¥2,091,006. Report is 36% too high.)
2. **Geography:** Is Chitose land price data (+44.1%) valid for Sapporo City analysis? (Chitose is a separate city.)
3. **Sources:** Can the 4 VERIFIED yield/vacancy claims be confirmed from GPG and KenDIX, which return HTTP 403?
4. **Contradictions:** Why does the evidence archive say Sapporo land price is +2.4% while the claims table says +1.8%?
5. **Ranking:** Does the ranking change materially if correct calculations are used? (Koto Ward would rank highest by DSCR 0.88, not lowest.)

### Required Fixes (Pending Reviewer Confirmation)

1. Recalculate all financial metrics with correct mortgage formula
2. Remove/reclassify geography-mismatched claims (Chitose data, Fukuoka prefecture, Osaka prefecture tourism)
3. Re-classify 11 VERIFIED claims as PENDING/DISPUTED if sources inaccessible
4. Resolve internal contradictions between evidence archive and claims table
5. Re-run ranking with VERIFIED data only

### Unresolved Questions

- What formula did the original report use for ADS that produced values 36-51% too high?
- Is the Sapporo land price +2.4% or +1.8%? (Requires MLIT XLS verification)
- Is the At Home +7.82% rent growth figure real or a misread? (Requires Japanese OCR of PDF)
