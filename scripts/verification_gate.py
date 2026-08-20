#!/usr/bin/env python3
import re
from pathlib import Path

required = [
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]
missing = [str(p) for p in required if not p.exists()]
text = '\n'.join(p.read_text(errors='replace') for p in required if p.exists())

checks = [
    ('required_files', not missing, f'missing={missing}'),
    ('no_known_calculation_failure', 'CALCULATION STATUS: FAIL' not in text and 'CALCULATION_STATUS: FAIL' not in text, 'existing report declares calculation failure'),
    ('no_unresolved_blockers', not re.search(r'BLOCKERS_REMAINING:\s*(?!0)\d+', text, re.I), 'unresolved blockers remain'),
]
print('# Deterministic Verification Gate')
status = 'PASS'
for name, ok, detail in checks:
    state = 'PASS' if ok else 'FAIL'
    print(f'- {name}: {state} — {detail}')
    if not ok:
        status = 'FAIL'
print(f'- OVERALL: {status}')
# This gate is advisory; the AI review is the independent reviewer.
