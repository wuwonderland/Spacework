# Automatic External Review

Primary model: `gpt-5.6-luna`

Final model used: `gpt-5.6-luna → gpt-5.6-sol`

# Independent Adversarial Review

## Overall status: **FAIL**

**Material error count: 11** — 3 BLOCKER, 8 MAJOR.  
The report is not synchronized with the corrected calculation file and its ranking materially depends on PENDING/DISPUTED inputs.

## BLOCKER findings

1. **The published financing results are materially wrong and contradict the repository’s corrected calculations.**
   - Report CoC: **-6.30% to -10.65%**; corrected file: **-1.29% to -3.80%**.
   - Report DSCR at 2.15%: **0.38–0.57**; corrected file: **0.64–0.88**.
   - Osaka report net cap rate: **1.81%**; reproducible corrected value: **2.03%**.
   - The report’s sensitivity table, rankings, weaknesses and investment implications still use the superseded numbers.

2. **PENDING inputs directly drive the ranking and principal conclusion.**
   - Purchase prices, market rents, residential vacancy rates, mortgage rate and operating-expense assumptions are mostly PENDING or unsupported.
   - Koto’s price, rent and vacancy are entirely interpolated/estimated.
   - Nevertheless, the report says the ranking uses “only VERIFIED data” and presents decisive CoC, DSCR and entry-price comparisons.
   - This directly contradicts `calculations/five-market-calculations.md`, which says the results are “DIAGNOSTIC ONLY” and that no ranking may be drawn.

3. **Tokyo rent is arithmetically misderived, potentially reversing the “all markets negative” conclusion.**
   - The calculation file says `¥4,698/sqm × 60 sqm = ¥220,000/month`; the actual result is **¥281,880/month**.
   - Using the stated assumptions:
     - Gross annual rent: **¥3,382,560**
     - NOI: approximately **¥2,168,846**
     - ADS: approximately **¥2,091,006**
     - DSCR: approximately **1.04**
     - CoC: approximately **+0.39%**
   - Thus, if ¥4,698/sqm/month is genuinely applicable to a 60 sqm 2LDK, the report’s central statement that all five markets are negative is false.

## MAJOR findings

1. **Koto-ku is improperly represented by Tokyo Bay data.**  
   The 5.8% vacancy rate covers the broader Tokyo Bay area, not Koto-ku. Claims classify it DISPUTED, but the report includes it in “Verified Market Data.”

2. **Osaka City and Osaka Prefecture are mixed.**
   - Tourism of 14.2 million is prefecture-level, not Osaka City.
   - The stated Osaka City population of **8.76 million** appears to be prefecture-scale; Osaka City is roughly one-third of that. Exact municipal evidence is required.
   - These data support Osaka’s risk and catalyst narrative despite the mismatch.

3. **Fukuoka City and Fukuoka Prefecture are mixed.**  
   The +5.8% land-price change is prefecture-level and classified DISPUTED, but appears in the city comparison.

4. **Sapporo and Chitose are mixed.**
   - Chitose’s +44.1% land-price change and Rapidus investment are not Sapporo City observations.
   - Rapidus is nevertheless presented as a Sapporo ranking strength and used to characterize Sapporo’s industry concentration.

5. **Gross-yield claims do not reconcile to the representative properties.**

   | Market | Rent and price implied gross yield | Reported market yield |
   |---|---:|---:|
   | Tokyo | 4.00% using ¥220k and ¥66m | 3.27% |
   | Koto | 4.47% | ~3.5% |
   | Osaka | 3.39% | 4.78% |
   | Fukuoka | 4.00% | 4.77% |
   | Sapporo | 3.95% | 5.03% |

   City-average GPG yields cannot be substituted for a standardized 60 sqm pre-owned 2LDK without matching property type, unit size, price basis and observation period.

6. **Property and metric definitions are not comparable.**
   - Office vacancy is used to support residential-condominium investment conclusions.
   - New-condo prices and supply are used alongside estimated pre-owned-condo economics.
   - Asking rents, average rents and estimated rents are mixed.
   - There is no demonstrated match for building age, unit size, grade or transaction-versus-asking basis.
   - Tokyo CBD/central-five-ward office rent is not a Tokyo-23-ward residential metric.

7. **VERIFIED evidence traceability is insufficient.**
   - Several locations are generic—“Various reports,” “October 2025 report,” “same source,” “press release summary,” or a publisher homepage—rather than an exact accessible URL, page/table and quoted passage.
   - The repository statement that all 47 VERIFIED claims have accessible evidence is not demonstrated by the supplied artifacts.
   - HTTP 403 is handled correctly for TOK-X-03 in the claims/calculation files, but the main report still places the 2.15% value in its “Verified Market Data” section.

8. **The scoring and material risk conclusions are not reproducible.**
   - No formula or criterion weights explain scores such as 18/25 and 16/25.
   - Liquidity ordering, “safest market,” “highest valuation risk,” “single-industry risk,” demographic labels and disaster-risk gradings lack exact evidence or calculation.
   - The report therefore cannot establish that its ordering follows only verified evidence.

## MINOR findings

- The mortgage derivation prints `(1+r)^360 = 1.93044`; at 2.15% nominal with monthly compounding it is approximately **1.905**. The resulting payment is nevertheless close to correct.
- Property tax is described as based on assessed value but calculated as a percentage of purchase price.
- “20–30% down payments with lower LTV” is internally wrong: 20% down implies higher LTV than the modeled 30% down.
- Fukuoka is called the “best yield profile” at 4.77% even though Sapporo is reported at 5.03%; the intended demographic qualification should be explicit.
- No quantitative appreciation forecast is made, but qualitative catalyst effects are asserted without explicit transmission assumptions.

## Required fixes

1. Replace every stale CoC, DSCR, ADS, NOI and cap-rate figure in the report with one consistently recalculated version.
2. Resolve the Tokyo ¥4,698/sqm rent definition and correct the multiplication; rerun the central conclusion afterward.
3. Remove the ranking or clearly mark it non-decision-ready until all decision-driving prices, rents, vacancy rates, financing terms and expense assumptions are verified.
4. Remove or relabel all Tokyo Bay/Koto, prefecture/city and Chitose/Sapporo substitutions.
5. Correct Osaka City population using an exact municipal table.
6. Match yield observations to property type, unit size, building age, geography, date and asking/transaction basis.
7. Distinguish gross yield, effective gross income, NOI cap rate and cash-on-cash return consistently.
8. Add an exact accessible URL, page/table and quotation for every material VERIFIED claim. For TOK-X-03, use an accessible municipal/MLIT housing survey or leave it PENDING and exclude it from decision-driving analysis.
9. Publish the 25-point scoring formula and evidence for every risk score, or remove the scores.
10. Reconcile `reports/`, `calculations/`, `claims/` and `verification/`; the external review’s “blockers resolved” assertion is currently contradicted by the main report.

## Questions requiring evidence

- Does Savills’ ¥4,698/sqm figure apply to a 60 sqm 2LDK, and is it asking, achieved, gross or effective rent?
- What exact transaction evidence supports each representative purchase price?
- What accessible lender evidence supports 70% LTV and 2.15% fixed for foreign nationals?
- What exact source supports Osaka City population of 8.76 million?
- What residential vacancy evidence supports Osaka, Fukuoka, Sapporo and Koto?
- What unit sizes and property types underlie each Global Property Guide yield?
- What evidence supports the liquidity ranking and the “single-industry,” valuation and disaster-risk assessments?
- Are management, reserve, tax and insurance assumptions based on purchase price, assessed value, fixed condominium charges or gross rent?

## Eligible for APPROVED

**No.** Unresolved blockers affect the central cash-flow conclusion and the published ranking.
