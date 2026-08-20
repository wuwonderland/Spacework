# Automatic External Review

Primary model: `gpt-5.6-luna`

Final model used: `gpt-5.6-luna → gpt-5.6-sol`

# Independent Adversarial Review

**Overall status: FAIL**  
**Material error count: 12** — 3 BLOCKER, 9 MAJOR  
**Eligible for APPROVED: NO**

## BLOCKER findings

1. **Decision report contains obsolete, materially incorrect financing results.**  
   The report uses the superseded calculations rather than `calculations/five-market-calculations.md`.

   | Market | Report CoC | Recalculated CoC* | Report DSCR | Recalculated DSCR* |
   |---|---:|---:|---:|---:|
   | Tokyo 23 wards | -6.83% | -2.42% | 0.53 | 0.77 |
   | Koto | -6.30% | -1.29% | 0.57 | 0.88 |
   | Osaka | -10.65% | -3.80% | 0.38 | 0.64 |
   | Fukuoka | -8.01% | -2.37% | 0.49 | 0.78 |
   | Sapporo | -7.87% | -2.58% | 0.48 | 0.76 |

   \*These match the corrected file within rounding when its stated, mostly PENDING inputs are accepted. Thus the report’s ranking, sensitivity table, net cap rates, and negative-carry magnitudes are stale.

2. **The ranking is driven by PENDING/DISPUTED inputs despite claiming “VERIFIED data only.”**  
   Purchase prices, rents outside Tokyo, residential vacancy assumptions, mortgage rate, operating expenses, and several population/yield inputs are PENDING or unsupported. The calculation file expressly says no ranking may be drawn from them, while the report presents a definitive ranking and scores.

3. **Material VERIFIED claims lack repository-grade exact evidence locations.**  
   The source table contains homepages and “Various reports/Various PDF links,” while many claim locations are only “report,” “summary,” or “same source.” No supplied evidence artifacts establish all 47 VERIFIED claims at exact page/table/row locations. The claim file’s assertion that all are accessible is therefore not reproducible from the supplied repository.

## MAJOR findings

1. **Tokyo rent derivation is arithmetically wrong and may reverse the headline conclusion.**  
   `¥4,698/sqm/month × 60 sqm = ¥281,880/month`, not ¥220,000.

   Using the stated assumptions:

   - Gross annual rent: **¥3,382,560**
   - Vacancy loss at 2.15%: **¥72,725**
   - Operating expenses: **¥1,140,989**
   - NOI: **¥2,168,846**
   - Net cap rate: **3.29%**
   - ADS: approximately **¥2.091M**
   - DSCR: approximately **1.04**
   - CoC: approximately **+0.39%**

   Although vacancy and other inputs remain unverified, this falsifies the report’s categorical “all five markets negative” conclusion under its claimed source-derived Tokyo rent.

2. **The mortgage audit contains an inconsistent manual expansion.**  
   At `r = 0.0215/12` and `n = 360`, `(1+r)^n` is approximately **1.905**, not **1.93044**. The reported payment outputs are close to the correct annuity results, but the displayed verification cannot generate those outputs.

3. **Osaka City population is geographically implausible.**  
   The report/claims use **8.76 million** for Osaka City; that is approximately prefecture-scale, not city-scale. This invalidates the claimed city population and related growth/risk conclusions unless exact city evidence is produced.

4. **Broader geographies continue to influence city/ward conclusions.**
   - Tokyo Bay vacancy is not Koto-ku vacancy.
   - Osaka Prefecture tourism is not Osaka City tourism.
   - Fukuoka Prefecture land growth is not Fukuoka City growth.
   - Chitose land growth and Rapidus investment are not Sapporo City metrics.
   - Tokyo CBD/central five wards are not interchangeable with Tokyo 23 wards.
   
   Several are marked DISPUTED in claims but still appear in the report’s “Verified Market Data,” strengths, catalysts, or risk narrative.

5. **Gross-yield metrics do not reconcile with representative-property inputs.**
   - Tokyo model: 4.00% from ¥220,000 rent, or 5.12% using the actual `¥4,698 × 60`; cited market yield: 3.27%.
   - Osaka model: 3.39%; cited yield: 4.78%.
   - Fukuoka model: 4.00%; cited yield: 4.77%.
   - Sapporo model: 3.95%; cited yield: 5.03%.
   - Koto model: 4.47%; narrative says about 3.5%.

   Market-average gross yields and modeled 60 sqm property economics are being mixed without matching unit size, bedroom count, property age, asking/transaction basis, or observation sample.

6. **Property and metric definitions are not comparable.**  
   New-condominium transaction prices, pre-owned representative properties, residential rents, office vacancies/rents, land-price changes, and broad apartment gross yields are combined into one score without a documented normalization. Grade-A and all-grade office metrics are mostly labeled, but central-five-ward, CBD, citywide, and all-grade series are not consistently comparable.

7. **The scoring model is not reproducible.**  
   Scores such as 18/25 and 16/25 have no factor weights, formulas, normalization, or calculation trail. Claims including “highest liquidity,” “capital preservation,” “youngest demographics,” “proven long-term appreciation,” and disaster-risk levels lack exact evidence.

8. **Operating and CoC assumptions are insufficiently supported.**
   - Tax is described as a percentage of “assessed value,” but calculations apply it to purchase price.
   - Management and reserve percentages are generic assumptions, not market/property evidence.
   - CoC excludes acquisition taxes, brokerage, registration, financing fees, and other initial cash, overstating economic CoC.
   - The 2.15% foreign-national fixed rate and 70% LTV are PENDING but are presented as “standard terms.”

9. **Observation periods and source labels are inconsistent.**  
   The August 2026 ranking mixes April/August 2025, FY2025, Q1/Q2 2026, and static data without staleness adjustments. Some report attributions conflict with claims—for example, Fukuoka/Sapporo vacancy is attributed to KenDIX in places but to accessible Mitsui Fudosan evidence elsewhere.

## MINOR findings

- Fukuoka’s 4.77% yield is described as highest among positive-growth major cities, but Osaka is listed at **4.78%** with positive population growth.
- “20–30% down payments with lower LTV” is internally inconsistent with the baseline 30% down/70% LTV; lower LTV generally requires more than 30% down.
- HTTP 403 is handled correctly only for TOK-X-03 in the revised claims file, but the report still presents the 2.15% residential vacancy in its verified-data section.

## Required fixes

1. Regenerate the report from one authoritative calculation version; remove every superseded CoC, DSCR, ADS, NOI, and cap-rate figure.
2. Correct the Tokyo rent multiplication and rerun the headline conclusion.
3. Remove the ranking and 25-point scores until all decision-driving inputs are VERIFIED, or clearly label the entire output as non-decision-ready scenario analysis.
4. Correct Osaka City population using city-specific evidence.
5. Remove or segregate Tokyo Bay, prefecture-level, central-five-ward, Chitose, and other broader-geography observations from city/ward conclusions.
6. Provide direct accessible URLs plus exact page/table/row or quoted passage for every material VERIFIED claim. Downgrade claims lacking such evidence.
7. Match yield evidence to property type, existing/new status, unit size/bedroom count, geography, observation date, and asking-versus-transaction basis.
8. Document the score formula and evidence for every qualitative factor, or delete the scores.
9. Recalculate CoC using total cash invested and clarify whether taxes use assessed value or purchase price.
10. Correct the displayed amortization exponent and preserve machine-reproducible calculation output.

## Questions requiring evidence

- What exact Osaka City table supports population of 8.76 million and +0.9% growth?
- What exact Savills sample does ¥4,698/sqm cover: all 23 wards, central wards, asking leases, or a specific residential portfolio/grade?
- What are the unit-size and bedroom assumptions behind each Global Property Guide gross yield?
- What accessible source proves Tokyo residential vacancy of exactly 2.15%? If none, use an accessible Statistics Bureau/Tokyo housing survey replacement or retain PENDING.
- What transaction evidence supports each representative pre-owned 60 sqm purchase price and monthly rent?
- What lender evidence supports 70% LTV, 2.15% fixed, and 30-year amortization for foreign nationals?
- Where are the exact evidence files for municipal populations, REI supply/prices, land-price tables, Tenjin projects, Rapidus investment, and hazard elevation?
- How were the 25-point scores calculated and weighted?

**APPROVED eligibility: NO — unresolved BLOCKER findings require FAIL.**
