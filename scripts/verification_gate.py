#!/usr/bin/env python3
import re
from pathlib import Path

ROOT = Path('.')
required = [
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]
missing = [str(p) for p in required if not p.exists()]

text_parts = []
for path in required:
    if path.exists():
        text_parts.append(path.read_text(errors='replace'))
text = '\n'.join(text_parts)

checks = []
checks.append(("required_files", not missing, f"missing={missing}"))
checks.append(("no_pending_approval", 'APPROVED' not in text or 'BLOCKERS_REMAINING: 0' in text, 'APPROVED must not coexist with unresolved blockers'))
checks.append(("no_known_math_failure", 'CALCULATION STATUS: FAIL' not in text and 'CALCULATION_STATUS: FAIL' not in text, 'report still declares failed calculations'))
checks.append(("no_known_blockers", not re.search(r'BLOCKERS_REMAINING:\s*(?!0)\d+', text, re.I), 'unresolved blockers remain'))

print('# Deterministic Verification Gate')
print(f'- branch files inspected: {len(required)}')
status = 'PASS'
for name, ok, detail in checks:
    state = 'PASS' if ok else 'FAIL'
    print(f'- {name}: {state} — {detail}')
    if not ok:
        status = 'FAIL'
print(f'- OVERALL: {status}')
if status == 'FAIL':
    raise SystemExit(2)
