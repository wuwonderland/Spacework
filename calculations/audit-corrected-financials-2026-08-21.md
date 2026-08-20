# Corrected Calculation Engine — Five-Market Audit (Revision 2)

**Source script:** `calculations/audit_corrected_calculations.py`  
**Formula verification:** Manual formula check PASSED (Tokyo: YEN 2,091,006 matches script output)  
**Protocol compliance:** All calculations use Python `decimal.Decimal` with documented formula.  
**Independent recalculation:** Each result verified by manual formula expansion.

## Formula

```
Monthly Payment = P × [r(1+r)^n] / [(1+r)^n - 1]
Where: P = Loan principal, r = annual_rate/12 (monthly rate), n = years × 12 (total payments)
Annual Debt Service = Monthly Payment × 12
```

## Standard Assumptions

| Parameter | Value | Source Status |
|-----------|-------|---------------|
| Down payment | 30% | Foreign national LTV ceiling |
| Interest rate | 2.15% fixed | PENDING — industry survey estimate, no central bank publication |
| Loan term | 30 years | Standard |
| Management fee | 15% of gross rent | Industry standard |
| Maintenance reserve | 8% of gross rent | Industry standard |
| Property tax | 0.40% (Tokyo/Koto), 0.35% (others) | Tokyo/Osaka standard |
| Insurance | 0.15% (Tokyo/Koto), 0.12% (others) | Industry standard |

## Input Verification Status

| Market | Purchase Price | Monthly Rent | Vacancy Rate | Status |
|--------|---------------|-------------|-------------|--------|
| Tokyo 23 Wards | YEN 66,000,000 (PENDING — estimated from YEN 1,100,000/sqm, no source) | YEN 220,000 (PENDING — derived from Savills 403, math error in derivation) | 2.2% (DISPUTED — VERIFIED claim says 2.15%) | 3 of 3 inputs UNVERIFIED |
| Koto Ward | YEN 51,000,000 (PENDING — est. 23% below Tokyo) | YEN 190,000 (PENDING — Tokyo data × 0.86) | 2.5% (PENDING — interpolated from Tokyo) | 3 of 3 inputs UNVERIFIED |
| Osaka City | YEN 37,200,000 (PENDING — Kinki region avg) | YEN 105,000 (PENDING — est. 1,750/sqm) | 3.2% (PENDING — no direct data) | 3 of 3 inputs UNVERIFIED |
| Fukuoka City | YEN 28,500,000 (PENDING — JRAE estimate) | YEN 95,000 (PENDING — est. from yield) | 3.8% (PENDING — no direct data) | 3 of 3 inputs UNVERIFIED |
| Sapporo City | YEN 24,300,000 (PENDING — JRAE estimate) | YEN 80,000 (PENDING — est. from yield) | 4.5% (PENDING — estimated) | 3 of 3 inputs UNVERIFIED |

**All 15 calculation inputs are PENDING or DISPUTED.** Per Protocol Rule 14, no investment ranking can be decision-ready using these inputs.

## Corrected Results

| Market | Purchase Price | Loan (70%) | Down (30%) | Gross Rent/yr | NOI | Cap Rate | ADS (correct) | Monthly Pmt | CoC | DSCR |
|--------|---------------|-----------|-----------|--------------|-----|----------|-------------|------------|-----|-----|
| Tokyo 23 Wards | YEN 66,000,000 | YEN 46,200,000 | YEN 19,800,000 | YEN 2,640,000 | YEN 1,611,720 | 2.44% | YEN 2,091,006 | YEN 174,250 | -2.42% | 0.77 |
| Koto Ward | YEN 51,000,000 | YEN 35,700,000 | YEN 15,300,000 | YEN 2,280,000 | YEN 1,418,100 | 2.78% | YEN 1,615,777 | YEN 134,648 | -1.29% | 0.88 |
| Osaka City | YEN 37,200,000 | YEN 26,040,000 | YEN 11,160,000 | YEN 1,260,000 | YEN 755,040 | 2.03% | YEN 1,178,567 | YEN 98,214 | -3.80% | 0.64 |
| Fukuoka City | YEN 28,500,000 | YEN 19,950,000 | YEN 8,550,000 | YEN 1,140,000 | YEN 700,530 | 2.46% | YEN 902,934 | YEN 75,245 | -2.37% | 0.78 |
| Sapporo City | YEN 24,300,000 | YEN 17,010,000 | YEN 7,290,000 | YEN 960,000 | YEN 581,790 | 2.39% | YEN 769,870 | YEN 64,156 | -2.58% | 0.76 |

## Error Comparison: Report vs Corrected

| Market | Metric | Report | Corrected | Error |
|--------|--------|--------|-----------|-------|
| Tokyo | ADS | YEN 2,846,352 | YEN 2,091,006 | +36.1% |
| Tokyo | NOI | YEN 1,494,960 | YEN 1,611,720 | -7.2% |
| Tokyo | CoC | -6.83% | -2.42% | -182.2% |
| Tokyo | DSCR | 0.53 | 0.77 | -31.2% |
| Koto | ADS | YEN 2,265,624 | YEN 1,615,777 | +40.2% |
| Koto | NOI | YEN 1,301,280 | YEN 1,418,100 | -8.2% |
| Koto | CoC | -6.30% | -1.29% | -387.6% |
| Koto | DSCR | 0.57 | 0.88 | -35.1% |
| Osaka | ADS | YEN 1,776,516 | YEN 1,178,567 | +50.7% |
| Osaka | NOI | YEN 673,440 | YEN 755,040 | -10.8% |
| Osaka | CoC | -10.65% | -3.80% | -180.6% |
| Osaka | DSCR | 0.38 | 0.64 | -40.7% |
| Fukuoka | ADS | YEN 1,321,188 | YEN 902,934 | +46.3% |
| Fukuoka | NOI | YEN 642,960 | YEN 700,530 | -8.2% |
| Fukuoka | CoC | -8.01% | -2.37% | -238.4% |
| Fukuoka | DSCR | 0.49 | 0.78 | -36.8% |
| Sapporo | ADS | YEN 1,124,316 | YEN 769,870 | +46.0% |
| Sapporo | NOI | YEN 534,960 | YEN 581,790 | -8.0% |
| Sapporo | CoC | -7.87% | -2.58% | -205.0% |
| Sapporo | DSCR | 0.48 | 0.76 | -36.5% |

## DSCR Sensitivity Analysis (Corrected)

| Market | DSCR @ 2.15% | DSCR @ 2.65% | DSCR @ 3.15% | (Report values in parens) |
|--------|-------------|-------------|-------------|--------------------------|
| Tokyo 23 Wards | 0.77 | 0.72 | 0.68 | (0.53, 0.49, 0.46) |
| Koto Ward | 0.88 | 0.82 | 0.77 | (0.57, 0.52, 0.48) |
| Osaka City | 0.64 | 0.60 | 0.56 | (0.38, 0.34, 0.31) |
| Fukuoka City | 0.78 | 0.73 | 0.68 | (0.49, 0.44, 0.40) |
| Sapporo City | 0.76 | 0.71 | 0.66 | (0.48, 0.43, 0.39) |

## Ranking Implication (Non-Decisive)

The corrected calculations show different relative rankings than the report's:

| Market | Corrected CoC vs Report CoC | Direction of Error |
|--------|---------------------------|-------------------|
| Tokyo 23 Wards | -2.42% vs -6.83% | Report overstated deficit by 2.8x |
| Koto Ward | -1.29% vs -6.30% | Report overstated deficit by 4.9x |
| Osaka City | -3.80% vs -10.65% | Report overstated deficit by 2.8x |
| Fukuoka City | -2.37% vs -8.01% | Report overstated deficit by 3.4x |
| Sapporo City | -2.58% vs -7.87% | Report overstated deficit by 3.0x |

**Note:** No new investment ranking is created. All 15 calculation inputs are PENDING/DISPUTED. The corrected figures are provided for diagnostic purposes only. No market is decision-ready for investment.
