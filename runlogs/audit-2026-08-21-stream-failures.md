# Run Log — Audit of Five-Market Report (2026-08-21)

**Run ID:** audit/2026-08-21-five-market-calculations  
**Commit:** b0223a56934225c522244cdf7490169a8fcc0b69  
**Date:** August 21, 2026  
**Protocol commit:** 4421902312d82177fadf76ed9c870c316d614e9c  

---

## Stream/Tool-Call Failures

### Failure 1: execute_code — Large calculation script
- **Tool:** `execute_code`
- **Stage:** Calculation audit (DSCR sensitivity analysis)
- **Description:** execute_code call with full calculation audit script (including DSCR sensitivity table) exceeded stream timeout. The response contained a `NameError` for `tokyo_noi_correct` variable and stream was truncated.
- **Side effects verified:** No — the calculation script did not execute successfully. The `audit_calc_helper.py` file was written separately via `write_file` and executed via `terminal`, producing verified results.
- **Recovery action:** Split the calculation into a standalone Python script (`audit_calc_helper.py`), committed alongside the audit report. Re-ran via `terminal()` which completed successfully. All 25 calculation checks verified via the script output.

### Failure 2: execute_code — Numerical validation script
- **Tool:** `execute_code`
- **Stage:** Numerical validation (source accessibility checks + claim validation)
- **Description:** execute_code call with numerical validation script stalled mid-stream. Response contained a `ValueError: Invalid format specifier` in the Tokyo rent derivation check script.
- **Side effects verified:** No — the script did not complete. The numerical validation results were produced by a simplified version of the same analysis, run successfully.
- **Recovery action:** Rewrote the numerical validation as a simpler script without complex f-string formatting. Results verified via terminal execution and documented in the audit report.

---

## Artifact Verification

| Artifact | Path | Exists | Verified |
|----------|------|--------|----------|
| Audit report (full) | verification/audit-five-market-2026-08-21-full.md | ✅ Yes | ✅ 310 lines, 7,733 bytes |
| Audit report (part 1) | verification/audit-five-market-2026-08-21.md | ✅ Yes | ✅ Contains Sections 1-3 |
| Audit report (part 2) | verification/audit-five-market-2026-08-21-part2.md | ✅ Yes | ✅ Contains Sections 4-12 |
| Calculation helper | audit_calc_helper.py | ✅ Yes | ✅ Run via terminal, all 25 checks |
| Commit | b0223a5 | ✅ Yes | ✅ Reachable on remote branch |
| Push | origin audit/2026-08-21-five-market-calculations | ✅ Yes | ✅ Pushed successfully |

## Git State

```
Branch: audit/2026-08-21-five-market-calculations
Commit: b0223a56934225c522244cdf7490169a8fcc0b69
Parent: 439c97c (Research: Five-market Japan real estate analysis)
Remote: origin/audit/2026-08-21-five-market-calculations (up to date)
```
