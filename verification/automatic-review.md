# Automatic External Review

Primary model: `gpt-5.6-luna`

Final model used: `gpt-5.6-luna → gpt-5.6-sol`

# Independent Adversarial Review

**Overall status: FAIL**  
**Material error count: 10** *(3 BLOCKER, 7 MAJOR)*

## BLOCKER findings

1. **The ranking is driven by PENDING/DISPUTED inputs.**
   - Purchase prices, residential rents, residential vacancies, mortgage rate, and operating expenses are unverified for most markets.
   - These inputs directly determine NOI, cap rate, CoC, and DSCR.
   - Disputed geographic proxies—Tokyo Bay for Koto, Osaka Prefecture for Osaka City, Fukuoka Prefecture for Fukuoka City, and Chitose for Sapporo—also influence the narrative.
   - The report nevertheless publishes a numbered ranking and scores. No reproducible 25-point scoring formula is provided.
   - This directly contradicts both “ranking uses only VERIFIED data points” and the quality gate’s admission that the ranking fails.

2. **Decision-driving calculations and conclusions contradict across files.**
   - The report’s interest-rate table contains obsolete DSCR values: Tokyo is shown as **0.53** at 2.15%, while the calculation file gives **1.04**.
   - Ranking sections retain obsolete CoC figures: Koto **-6.30%**, Osaka **-10.65%**, Fukuoka **-8.01%**, and Sapporo **-7.87%**, versus corrected values of approximately **-1.29%, -3.80%, -2.37%, and -2.58%**.
   - The executive summary says Tokyo is positive, while the ranking calls it “negative cash flow”; the caveat says all markets are cash-flow negative.
   - The report cannot support a coherent material conclusion in its current state.

3. **Material VERIFIED claims lack exact, auditable evidence locations.**
   - Many entries cite only a homepage, “Various reports,” “press release summary,” “same source,” or generic report/table descriptions.
   - Examples include REI’s homepage rather than the exact report, MOJ “Various reports,” municipal “October 2025 report,” and databases without record URLs.
   - The supplied artifacts do not substantiate the external review’s assertion that all 47 VERIFIED claims have accessible exact evidence.
   - HTTP 403 is correctly treated as inaccessible for TOK-X-03, but the same exact-location standard has not demonstrably been met for all other material claims.

## MAJOR findings

1. **Tokyo NOI arithmetic is wrong.**

   From the stated inputs:

   - Gross rent: `¥281,880 × 12 = ¥3,382,560`
   - Vacancy loss: `¥3,382,560 × 2.15% = ¥72,725`
   - Effective gross income: `¥3,309,835`
   - Expenses: `¥507,384 + ¥270,605 + ¥264,000 + ¥99,000 = ¥1,140,989`
   - **Correct NOI: approximately ¥2,168,846**, not ¥2,167,155.
   - Using stated ADS of ¥2,091,006:
     - Cash flow: approximately **¥77,840**
     - CoC: approximately **0.39%**
     - DSCR: approximately **1.037**

   Other base-case outputs reproduce approximately:

   | Market | Recalculated CoC | Recalculated DSCR |
   |---|---:|---:|
   | Koto | -1.29% | 0.88 |
   | Osaka | -3.80% | 0.64 |
   | Fukuoka | -2.37% | 0.78 |
   | Sapporo | -2.58% | 0.76 |

2. **Tokyo sensitivity CoC figures are materially wrong.**
   - At 2.65%, stated inputs imply ADS of roughly ¥2.23M and CoC around **-0.33%**, not **+0.10%**.
   - At 3.15%, CoC is roughly **-1.1%**, not **-0.18%**.
   - The manual amortization check also states `(1+r)^360 = 1.93044`; it is approximately **1.905**, although the reported base payment is close to the correct annuity result.

3. **Published gross yields do not match the representative properties.**

   Gross yields implied by modeled rent and price are:

   | Market | Modeled gross yield | Published market yield |
   |---|---:|---:|
   | Tokyo | 5.13% | 3.27% |
   | Koto | 4.47% | ~3.5% |
   | Osaka | 3.39% | 4.78% |
   | Fukuoka | 4.00% | 4.77% |
   | Sapporo | 3.95% | 5.03% |

   These appear to use different samples, unit sizes, property types, or asking-price/rent methodologies. They cannot be treated as metrics for the same standardized 60 sqm pre-owned condominium without reconciliation. Osaka’s report also states a **1.81% net cap rate**, while the calculation file gives **2.03%**.

4. **Geographic substitutions remain in the report despite claim reclassification.**
   - Koto-ku is still presented with Tokyo Bay office vacancy.
   - Osaka City narrative uses Osaka Prefecture tourism.
   - Fukuoka City table uses Fukuoka Prefecture land growth.
   - Sapporo’s strengths use Rapidus investment in Chitose; Chitose is a separate city.
   - Tokyo CBD/central five wards metrics are shown alongside Tokyo 23-ward metrics without consistently preserving the boundary.
   - These contextual figures may be reported only with explicit separation and cannot serve as city-specific ranking evidence.

5. **Osaka population evidence is contradictory and likely geographically wrong.**
   - The claims file marks **8.76M for Osaka City as VERIFIED**.
   - The report correctly changes this to approximately **2.79M** and says 8.76M was prefecture-scale.
   - OSA-P-01 must therefore be rejected or corrected, not remain VERIFIED.
   - Koto’s pending population of **1.234M** also requires direct ward-level evidence before use.

6. **Residential investment conclusions rely heavily on non-comparable office metrics.**
   - Office vacancy/rent observations are used as strengths for a pre-owned residential condominium analysis without a demonstrated relationship to residential NOI or demand.
   - Provider universes and definitions are not reconciled: all-grade versus Grade A, CBD versus 23 wards, and different provider/date series.
   - Osaka’s 1.8% versus 3.74% vacancy difference is attributed only to time, but provider coverage and grade definitions may also differ.

7. **Several material qualitative claims lack structured evidence.**
   - Liquidity ordering, “safest market,” “youngest demographics,” tenant quality, single-industry concentration, regulatory scrutiny, disaster-risk levels, supply-risk labels, and “lowest supply since 2003” do not have exact supporting claim records.
   - The 18/25 and 16/25 scores have no disclosed category weights or calculations and are not reproducible.

## MINOR findings

- The report calls 15% of rent a “management fee,” which may be confused with condominium building management fees; the definition should be explicit.
- Property tax is modeled as a percentage of purchase value while the justification refers to assessed value.
- CoC uses down payment only and excludes acquisition tax, brokerage, registration, financing fees, and initial reserves. This is permissible only if prominently labeled as a restricted diagnostic definition.
- Source attribution is inconsistent: some Fukuoka/Sapporo vacancy figures are attributed to KenDIX in the report but to Mitsui Fudosan in the calculation/reclassification notes.
- The report combines asking rents, market averages, estimated rents, new-condo prices, and a pre-owned representative property without adequate adjustment for age, location, floor, or unit size.
- No appreciation forecast is made. Rate-sensitivity scenarios have explicit rate assumptions, but their calculations and report presentation require correction.

## Required fixes

1. Remove the numbered ranking and scores until all decision-driving inputs are VERIFIED, or label the entire section as a non-ranking illustrative scenario with no investment conclusion.
2. Replace every stale CoC/DSCR value in the report with one consistent recalculated table.
3. Correct Tokyo NOI and the 2.65%/3.15% sensitivity calculations.
4. Reconcile each external gross-yield statistic with property type, unit size, geography, observation date, and asking-versus-transaction methodology; otherwise do not compare it to the representative model.
5. Correct OSA-P-01 and audit all city population claims against official city/ward datasets.
6. Remove or segregate Tokyo Bay, prefecture-level, central-five-ward, and Chitose evidence from city-specific conclusions.
7. Add exact URLs, document titles, publication dates, page/table/cell locations, and archived copies for every material VERIFIED claim.
8. Use an accessible replacement for TOK-X-03—such as an official or provider-hosted report containing the exact residential series—or keep it PENDING and exclude it from decision-driving calculations.
9. Provide a reproducible scoring methodology, including categories, weights, and claim-to-score mapping.
10. Separate residential transaction evidence from office-market context and clearly define gross versus net yield.

## Questions requiring evidence

- What exact sample underlies GPG’s yields—unit size, property age, asking or transaction price, and asking or achieved rent?
- What accessible document and table support the Tokyo 2.15% residential vacancy rate?
- What official Osaka City dataset supports 2.79M and +0.9%, and why is 8.76M still VERIFIED in claims?
- What official Koto-ku dataset supports 1.234M and +1.5%?
- What city-specific transaction evidence supports the ¥51.0M, ¥37.2M, ¥28.5M, and ¥24.3M representative prices?
- What lender quotations support 70% LTV and 2.15% fixed financing for foreign nationals?
- What evidence supports the modeled residential rents and vacancy rates outside Tokyo?
- What evidence and methodology support the liquidity, demographic, disaster, supply-risk, and regulatory labels?
- How are the 25-point scores calculated?

## Eligible for APPROVED

**No.** Unresolved blockers remain, so the report is not eligible for **APPROVED**.
