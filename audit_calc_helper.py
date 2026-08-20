"""
Independent financial calculation audit of five-market Japan real estate report.
All calculations use the standard mortgage annuity formula.
"""

def mortgage_monthly(principal, annual_rate, years):
    """Standard mortgage: P * [r(1+r)^n] / [((1+r)^n - 1]
    r = monthly interest rate, n = total number of payments"""
    r = annual_rate / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * (r * (1 + r)**n) / ((1 + r)**n - 1)

def annual_debt_service(principal, annual_rate, years):
    return mortgage_monthly(principal, annual_rate, years) * 12

def calc_market(name, price, rent, vacancy, prop_tax_rate, ins_rate,
                mgmt_pct=0.15, maint_pct=0.08,
                down_pct=0.30, rate=0.0215, term=30):
    """Calculate all financial metrics for a market."""
    loan = price * (1 - down_pct)
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
    monthly = ads / 12
    cf = noi - ads
    coc = cf / down
    dscr = noi / ads
    return {
        'name': name,
        'loan': loan,
        'down': down,
        'egi': egi,
        'agi': agi,
        'expenses': total_expenses,
        'noi': noi,
        'cap_rate': cap_rate,
        'ads': ads,
        'monthly': monthly,
        'cf': cf,
        'coc': coc,
        'dscr': dscr,
    }

# Market inputs from the report's calculation file
markets = {
    "Tokyo 23 Wards": {
        'price': 66_000_000, 'rent': 220_000, 'vacancy': 0.022,
        'prop_tax_rate': 0.0040, 'ins_rate': 0.0015,
        'report_noi': 1_494_960, 'report_ads': 2_846_352,
        'report_coc': -0.0683, 'report_dscr': 0.53, 'report_cap': 0.0227,
    },
    "Koto Ward": {
        'price': 51_000_000, 'rent': 190_000, 'vacancy': 0.025,
        'prop_tax_rate': 0.0040, 'ins_rate': 0.0015,
        'report_noi': 1_301_280, 'report_ads': 2_265_624,
        'report_coc': -0.0630, 'report_dscr': 0.57, 'report_cap': 0.0255,
    },
    "Osaka City": {
        'price': 37_200_000, 'rent': 105_000, 'vacancy': 0.032,
        'prop_tax_rate': 0.0035, 'ins_rate': 0.0012,
        'report_noi': 673_440, 'report_ads': 1_776_516,
        'report_coc': -0.1065, 'report_dscr': 0.38, 'report_cap': 0.0181,
    },
    "Fukuoka City": {
        'price': 28_500_000, 'rent': 95_000, 'vacancy': 0.038,
        'prop_tax_rate': 0.0035, 'ins_rate': 0.0012,
        'report_noi': 642_960, 'report_ads': 1_321_188,
        'report_coc': -0.0801, 'report_dscr': 0.49, 'report_cap': 0.0226,
    },
    "Sapporo City": {
        'price': 24_300_000, 'rent': 80_000, 'vacancy': 0.045,
        'prop_tax_rate': 0.0035, 'ins_rate': 0.0012,
        'report_noi': 534_960, 'report_ads': 1_124_316,
        'report_coc': -0.0787, 'report_dscr': 0.48, 'report_cap': 0.0220,
    },
}

report_sensitivity = {
    "Tokyo 23 Wards": {"dscr_215": 0.53, "dscr_265": 0.49, "dscr_315": 0.46},
    "Koto Ward": {"dscr_215": 0.57, "dscr_265": 0.52, "dscr_315": 0.48},
    "Osaka City": {"dscr_215": 0.38, "dscr_265": 0.34, "dscr_315": 0.31},
    "Fukuoka City": {"dscr_215": 0.49, "dscr_265": 0.44, "dscr_315": 0.40},
    "Sapporo City": {"dscr_215": 0.48, "dscr_265": 0.43, "dscr_315": 0.39},
}

if __name__ == '__main__':
    print("INDEPENDENT CALCULATION AUDIT — Five-Market Report")
    print("=" * 90)

    all_errors = []

    for name, m in markets.items():
        correct = calc_market(name, m['price'], m['rent'], m['vacancy'],
                              m['prop_tax_rate'], m['ins_rate'])

        print(f"\n--- {name} ---")
        print(f"  Loan:      YEN {correct['loan']:,.0f} (70% of YEN {m['price']:,})")
        print(f"  Down:      YEN {correct['down']:,.0f}")
        print(f"  Gross rent: YEN {correct['egi']:,.0f}/yr")
        print(f"  Effective gross: YEN {correct['agi']:,.0f}")
        print(f"  Expenses:   YEN {correct['expenses']:,.0f}")
        print(f"  Correct: NOI=YEN {correct['noi']:,.0f} ({correct['cap_rate']*100:.2f}%), "
              f"ADS=YEN {correct['ads']:,.0f}, CoC={correct['coc']*100:.2f}%, DSCR={correct['dscr']:.2f}")
        print(f"  Report:  NOI=YEN {m['report_noi']:,.0f} ({m['report_cap']*100:.2f}%), "
              f"ADS=YEN {m['report_ads']:,.0f}, CoC={m['report_coc']*100:.2f}%, DSCR={m['report_dscr']}")

        # Check each metric
        noi_err = (m['report_noi'] - correct['noi']) / abs(correct['noi']) * 100
        ads_err = (m['report_ads'] - correct['ads']) / correct['ads'] * 100
        coc_err = (m['report_coc'] - correct['coc']) / abs(correct['coc']) * 100
        dscr_err = (m['report_dscr'] - correct['dscr']) / correct['dscr'] * 100
        cap_err = (m['report_cap'] - correct['cap_rate']) / correct['cap_rate'] * 100

        if abs(noi_err) > 1: all_errors.append((name, "NOI", m['report_noi'], correct['noi'], f"{noi_err:+.1f}%"))
        if abs(ads_err) > 1: all_errors.append((name, "ADS", m['report_ads'], correct['ads'], f"{ads_err:+.1f}%"))
        if abs(coc_err) > 1: all_errors.append((name, "CoC", f"{m['report_coc']*100:.2f}%", f"{correct['coc']*100:.2f}%", f"{coc_err:+.1f}%"))
        if abs(dscr_err) > 1: all_errors.append((name, "DSCR", m['report_dscr'], round(correct['dscr'],2), f"{dscr_err:+.1f}%"))
        if abs(cap_err) > 1: all_errors.append((name, "CapRate", f"{m['report_cap']*100:.2f}%", f"{correct['cap_rate']*100:.2f}%", f"{cap_err:+.1f}%"))

    print(f"\n{'='*90}")
    print(f"CALCULATION ERRORS: {len(all_errors)}")
    print(f"{'='*90}")
    for e in all_errors:
        print(f"  {e[0]} {e[1]}: report={e[2]}, correct={e[3]}, error={e[4]}")

    # DSCR sensitivity check
    print(f"\n{'='*90}")
    print(f"DSCR SENSITIVITY — Independent Recalculation vs Report")
    print(f"{'='*90}")
    for name, m in markets.items():
        loan = m['price'] * 0.70
        egi = m['rent'] * 12
        agi = egi - egi * m['vacancy']
        exp = egi * 0.15 + egi * 0.08 + m['price'] * m['prop_tax_rate'] + m['price'] * m['ins_rate']
        noi = agi - exp
        dsrs = []
        for r in [0.0215, 0.0265, 0.0315]:
            ads = annual_debt_service(loan, r, 30)
            dsrs.append(noi / ads)
        rs = report_sensitivity[name]
        print(f"  {name}: correct=[{dsrs[0]:.2f}, {dsrs[1]:.2f}, {dsrs[2]:.2f}] "
              f"report=[{rs['dscr_215']:.2f}, {rs['dscr_265']:.2f}, {rs['dscr_315']:.2f}]")
