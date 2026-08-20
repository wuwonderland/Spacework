# External Review — Five-Market Audit (2026-08-21)

**Reviewed branch:** `audit/2026-08-21-five-market-calculations`
**Reviewed commit:** `6869cd8` (audit + runlog/review queue update)
**Reviewer:** ChatGPT
**Status:** FAIL — REVISION REQUIRED

## Review scope
This is an external adversarial review of Hermes' audit of the previous five-market Japan real-estate report. This review does **not** approve the underlying investment report and does not create a new investment ranking.

## Confirmed blockers

| # | Type | Severity | Finding | Required action |
|---|---|---|---|---|
| 1 | Calculation | BLOCKER | The audit reports that all 25 financial calculations were wrong. Its core amortization check is mathematically credible: for P=¥46.2M, annual rate=2.15%, monthly rate=0.0215/12, n=360, annual debt service is approximately ¥2,091,006, not ¥2,846,352. | Rebuild all affected financing calculations from verified inputs using one documented annuity implementation; independently recalculate. |
| 2 | Input integrity | BLOCKER | The audit itself identifies PENDING values used as calculation/risk inputs. | Remove unverified inputs from decision-driving calculations; downgrade outputs to PENDING when inputs are unresolved. |
| 3 | Geography | MAJOR | Chitose is not Sapporo; Fukuoka Prefecture is not Fukuoka City; Osaka Prefecture tourism is not Osaka City; broader Tokyo Bay/central-ward figures are not interchangeable with the requested target geographies. | Re-source at the exact requested geography or mark the claim unavailable. |
| 4 | Evidence traceability | MAJOR | Claims marked VERIFIED cannot be accepted merely because the source page is reachable. Exact values must be locatable in the source. HTTP 403 alone is not proof that the underlying claim is false, but it is sufficient to prevent independent verification unless an archived/downloaded primary document proves the value. | Preserve an accessible evidence artifact or reclassify the claim PENDING/DISPUTED. |
| 5 | Contradictions | MAJOR | The audit reports conflicting Sapporo land-price figures (+2.4% vs +1.8%) and conflicting Tokyo vacancy/geography labels. | Resolve against the exact primary table/observation point or mark DISPUTED. |
| 6 | Self-assessment | MAJOR | The prior report's self-check allegedly marked quality gates as passed despite material errors. | Quality status must be generated from machine-checkable conditions, not the model's narrative assertion. |

## Additional reviewer findings

### A. Review-count inconsistency
The audit summary alternates between **10** and **11** unverifiable VERIFIED claims. This must be reconciled to one claim-level count derived from the actual claims table.

### B. HTTP 403 is an evidence-access problem, not automatically a factual error
A blocked page does not prove that a value is false. The correct status is **UNVERIFIABLE from the currently preserved evidence** unless the exact value is reproduced in an accessible primary document, archived copy, or locally stored evidence artifact whose provenance is documented.

### C. Ranking impact language must remain non-decisive
The audit includes corrected CoC/DSCR figures and comments about ranking implications. Those figures are useful for diagnostic purposes, but the underlying input set still contains unresolved/PENDING claims. Therefore no market ranking should be considered decision-ready until the inputs are fully verified and the corrected calculations are reproducible.

### D. Stream-stall handling is now acceptable only if side effects are checked
The run reported two `execute_code` stream stalls. Hermes subsequently verified the Git commit/artifacts and recorded the failures. This is the correct recovery pattern. Future runs must treat a stalled tool call as **unknown side effect** until the filesystem/Git state proves whether the operation happened.

## Required revision protocol

1. Do **not** rerun the entire research from scratch.
2. Start from the existing audit branch and latest verified Git state.
3. Resolve all BLOCKER findings first.
4. Rebuild the financial calculation layer from source-backed inputs.
5. Reconcile all geography and source-status mismatches.
6. Reconcile conflicting claim records.
7. Re-run deterministic validation checks.
8. Push a new commit.
9. Perform another external review against the new commit.
10. Only move to `APPROVED` when zero BLOCKER findings remain and all decision-driving inputs are VERIFIED.

## PASS criteria for the next review

- Every material calculation reproduces from documented inputs.
- No PENDING/DISPUTED input drives an investment conclusion.
- Every claim's geography exactly matches its label.
- Every VERIFIED claim has preserved evidence sufficient for independent re-location.
- All contradictions are resolved or explicitly marked DISPUTED.
- The final report's quality state is derived from the checks above.
