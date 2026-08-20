"""
Corrected financial calculation engine for the five-market Japan real estate audit.

Builds on the original report's calculations/five-market-calculations.md but:
1. Uses the correct standard mortgage annuity formula
2. Marks PENDING inputs clearly
3. All outputs are machine-checkable

Protocol: RESEARCH -> SOURCE VALIDATION -> GEOGRAPHY VALIDATION ->
NUMERICAL VALIDATION -> CONTRADICTION CHECK -> CALCULATIONS -> AUDIT REPORT
"""

from decimal import Decimal, ROUND_HALF_UP

def mortgage_monthly(principal, annual_rate, years):
    """
    Standard mortgage annuity formula:
    Monthly = P * [r(1+r)^n] / [(1+r)^n - 1]
    where r = monthly interest rate = annual_rate/12, n = total payments = years*12
    """
    r = Decimal(annual_rate) / Decimal(12)
    n = Decimal(years * 12)
    if r == 0:
        return Decimal(principal) / n
    one_plus_r = Decimal(1) + r
    return Decimal(principal) * (r * one_plus_r**n) / (one_plus_r**n - Decimal(1))

def annual_debt_service(principal, annual_rate, years):
    """ADS = monthly_payment * 12"""
    return mortgage_monthly(principal, annual_rate, years) * Decimal(12)

def round_yen(amount):
    """Round to nearest yen."""
    return int(Decimal(str(amount)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def round_pct(amount, decimals=4):
    """Round to specified decimal places."""
    return float(Decimal(str(amount)).quantize(Decimal('0.' + '0'*(decimals-1) + '1'), rounding=ROUND_HALF_UP))

# ================================================================
# INPUTS — with verification status
# ================================================================
# Source: calculations/five-market-calculations.md (original report)
# Note: Several inputs are PENDING — they cannot be independently verified
# from accessible sources. These are clearly flagged.

INPUTS = {
    "Tokyo 23 Wards": {
        "property_size_sqm": 60,
        "purchase_price": 66_000_000,  # PENDING: est. from YEN 1,100,000/sqm, no source
        "monthly_rent": 220_000,      # PENDING: derived from Savills (403), math error in derivation
        "vacancy_rate": 0.022,        # DISPUTED: VERIFIED claim says 2.15%, report uses 2.2%
        "mgmt_fee_pct": 0.15,         # INDUSTRY STANDARD (not market-specific)
        "maint_pct": 0.08,            # INDUSTRY STANDARD (not market-specific)
        "prop_tax_rate": 0.0040,      # OK (Tokyo standard)
        "insurance_rate": 0.0015,     # OK (industry standard)
        "down_payment_pct": 0.30,     # OK (foreign national LTV ceiling)
        "interest_rate": 0.0215,      # PENDING: foreign national rates, no central bank pub
        "loan_term_years": 30,        # OK (standard)
    },
    "Koto Ward": {
        "property_size_sqm": 60,
        "purchase_price": 51_000_000,  # PENDING: est. 23% below Tokyo avg, no source
        "monthly_rent": 190_000,      # PENDING: Tokyo data x 0.86, no source
        "vacancy_rate": 0.025,        # PENDING: interpolated from Tokyo data
        "mgmt_fee_pct": 0.15,
        "maint_pct": 0.08,
        "prop_tax_rate": 0.0040,
        "insurance_rate": 0.0015,
        "down_payment_pct": 0.30,
        "interest_rate": 0.0215,
        "loan_term_years": 30,
    },
    "Osaka City": {
        "property_size_sqm": 60,
        "purchase_price": 37_200_000,  # PENDING: from Kinki region avg, no city-level
        "monthly_rent": 105_000,      # PENDING: est. YEN 1,750/sqm, no source
        "vacancy_rate": 0.032,        # PENDING: no direct data
        "mgmt_fee_pct": 0.15,
        "maint_pct": 0.08,
        "prop_tax_rate": 0.0035,
        "insurance_rate": 0.0012,
        "down_payment_pct": 0.30,
        "interest_rate": 0.0215,
        "loan_term_years": 30,
    },
    "Fukuoka City": {
        "property_size_sqm": 60,
        "purchase_price": 28_500_000,  # PENDING: JRAE estimate
        "monthly_rent": 95_000,       # PENDING: estimated from yield data
        "vacancy_rate": 0.038,        # PENDING: no direct data
        "mgmt_fee_pct": 0.15,
        "maint_pct": 0.08,
        "prop_tax_rate": 0.0035,
        "insurance_rate": 0.0012,
        "down_payment_pct": 0.30,
        "interest_rate": 0.0215,
        "loan_term_years": 30,
    },
    "Sapporo City": {
        "property_size_sqm": 60,
        "purchase_price": 24_300_000,  # PENDING: JRAE estimate
        "monthly_rent": 80_000,       # PENDING: estimated from yield data
        "vacancy_rate": 0.045,        # PENDING: estimated (no direct data)
        "mgmt_fee_pct": 0.15,
        "maint_pct": 0.08,
        "prop_tax_rate": 0.0035,
        "insurance_rate": 0.0012,
        "down_payment_pct": 0.30,
        "interest_rate": 0.0215,
        "loan_term_years": 30,
    },
}

def calculate_market(name, inputs):
    """Calculate all financial metrics for a market."""
    price = Decimal(inputs["purchase_price"])
    rent = Decimal(inputs["monthly_rent"])
    vacancy = Decimal(inputs["vacancy_rate"])
    prop_tax_rate = Decimal(inputs["prop_tax_rate"])
    ins_rate = Decimal(inputs["insurance_rate"])
    down_pct = Decimal(inputs["down_payment_pct"])
    rate = Decimal(inputs["interest_rate"])
    term = inputs["loan_term_years"]
    mgmt_pct = Decimal(inputs["mgmt_fee_pct"])
    maint_pct = Decimal(inputs["maint_pct"])

    loan = price * (Decimal(1) - down_pct)
    down = price * down_pct
    egi = rent * 12
    vac_loss = egi * vacancy
    agi = egi - vac_loss
    mgmt_fee = egi * mgmt_pct
    maint = egi * maint_pct
    prop_tax = price * prop_tax_rate
    insurance = price * ins_rate
    total_expenses = mgmt_fee + maint + prop_tax + insurance
    noi = agi - total_expenses
    cap_rate = noi / price
    ads = annual_debt_service(loan, rate, term)
    monthly_payment = ads / 12
    cf = noi - ads
    coc = cf / down
    dscr = noi / ads

    return {
        "name": name,
        "loan": loan,
        "down": down,
        "egi": egi,
        "vac_loss": vac_loss,
        "agi": agi,
        "mgmt_fee": mgmt_fee,
        "maint": maint,
        "prop_tax": prop_tax,
        "insurance": insurance,
        "total_expenses": total_expenses,
        "noi": noi,
        "cap_rate": cap_rate,
        "ads": ads,
        "monthly_payment": monthly_payment,
        "cash_flow": cf,
        "coc": coc,
        "dscr": dscr,
        "input_status": inputs.get("input_status", "PENDING (multiple unverified inputs)"),
    }

def calc_dscr_sensitivity(name, inputs, rates):
    """Calculate DSCR at multiple interest rates."""
    price = Decimal(inputs["purchase_price"])
    rent = Decimal(inputs["monthly_rent"])
    vacancy = Decimal(inputs["vacancy_rate"])
    prop_tax_rate = Decimal(inputs["prop_tax_rate"])
    ins_rate = Decimal(inputs["insurance_rate"])
    down_pct = Decimal(inputs["down_payment_pct"])
    term = inputs["loan_term_years"]

    loan = price * (Decimal(1) - down_pct)
    egi = rent * 12
    agi = egi * (Decimal(1) - vacancy)
    expenses = egi * Decimal("0.23") + price * (prop_tax_rate + ins_rate)
    # 0.23 = mgmt(15%) + maint(8%)
    noi = agi - expenses

    results = {}
    for rate in rates:
        ads = annual_debt_service(loan, rate, term)
        results[f"dscr_{rate:.4f}"] = noi / ads
    return results

if __name__ == '__main__':
    print("=" * 90)
    print("CORRECTED CALCULATION ENGINE — Five-Market Audit")
    print("Formula: P * [r(1+r)^n] / [(1+r)^n - 1], r=annual_rate/12, n=years*12")
    print("=" * 90)

    all_errors = []
    correct_results = {}

    for name, inputs in INPUTS.items():
        calc = calculate_market(name, inputs)
        correct_results[name] = calc

        print(f"\n--- {name} ---")
        print(f"  Purchase price:  YEN {round_yen(calc['loan'] / Decimal('0.70')):,}")
        print(f"  Loan principal:  YEN {round_yen(calc['loan']):,} (70% LTV)")
        print(f"  Down payment:    YEN {round_yen(calc['down']):,} (30%)")
        print(f"  Gross annual rent: YEN {round_yen(calc['egi']):,}")
        print(f"  Vacancy loss:    YEN {round_yen(calc['vac_loss']):,} ({inputs['vacancy_rate']*100:.1f}%)")
        print(f"  Effective gross:  YEN {round_yen(calc['agi']):,}")
        print(f"  Mgmt fee (15%):  YEN {round_yen(calc['mgmt_fee']):,}")
        print(f"  Maint (8%):      YEN {round_yen(calc['maint']):,}")
        print(f"  Property tax:    YEN {round_yen(calc['prop_tax']):,}")
        print(f"  Insurance:       YEN {round_yen(calc['insurance']):,}")
        print(f"  Total expenses:  YEN {round_yen(calc['total_expenses']):,}")
        print(f"  NOI:             YEN {round_yen(calc['noi']):,}  ({calc['cap_rate']*100:.2f}% cap rate)")
        print(f"  Monthly payment: YEN {round_yen(calc['monthly_payment']):,}")
        print(f"  Annual debt service: YEN {round_yen(calc['ads']):,}")
        print(f"  Cash flow:       YEN {round_yen(calc['cash_flow']):,}")
        print(f"  Cash-on-Cash:    {calc['coc']*100:.2f}%")
        print(f"  DSCR:            {calc['dscr']:.4f}")

        # Verify formula correctness
        expected_ads_tokyo = round_yen(correct_results["Tokyo 23 Wards"]["ads"]) if name == "Tokyo 23 Wards" else None
        if name == "Tokyo 23 Wards":
            print(f"\n  Formula verification: YEN {round_yen(calc['ads']):,}")
            print(f"  Manual check: 46,200,000 * (0.0215/12) * (1+0.0215/12)^360 / ((1+0.0215/12)^360 - 1) * 12")
            r = Decimal("0.0215") / Decimal(12)
            n = Decimal(360)
            monthly = Decimal(46_200_000) * (r * (1+r)**n) / ((1+r)**n - 1)
            manual_ads = monthly * 12
            print(f"  Manual result: YEN {round_yen(manual_ads):,}")
            assert abs(round_yen(manual_ads) - round_yen(calc['ads'])) < 100, "Formula mismatch!"
            print(f"  Formula check: PASSED")

    # DSCR sensitivity analysis
    print(f"\n{'='*90}")
    print("DSCR SENSITIVITY ANALYSIS (Corrected)")
    print(f"{'='*90}")
    print(f"{'Market':<20} {'DSCR@2.15%':>10} {'DSCR@2.65%':>10} {'DSCR@3.15%':>10}")
    print("-" * 55)
    for name, inputs in INPUTS.items():
        sens = calc_dscr_sensitivity(name, inputs, [0.0215, 0.0265, 0.0315])
        # Keys are formatted as dscr_0.02150, dscr_0.02650, dscr_0.03150
        keys = list(sens.keys())
        print(f"{name:<20} {float(sens[keys[0]]):>10.4f} {float(sens[keys[1]]):>10.4f} {float(sens[keys[2]]):>10.4f}")

    # Write corrected calculation output
    print(f"\n{'='*90}")
    print("CORRECTED SUMMARY TABLE")
    print(f"{'='*90}")
    print(f"{'Market':<20} {'Price':>12} {'NOI':>14} {'CapRate':>8} {'ADS':>14} {'CoC':>8} {'DSCR':>6}")
    print("-" * 85)
    for name, calc in correct_results.items():
        print(f"{name:<20} {round_yen(Decimal(INPUTS[name]['purchase_price'])):>12,} "
              f"{round_yen(calc['noi']):>14,} {float(calc['cap_rate'])*100:>7.2f}% "
              f"{round_yen(calc['ads']):>14,} {float(calc['coc'])*100:>7.2f}% {float(calc['dscr']):>6.2f}")
