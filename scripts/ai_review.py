#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = os.environ.get('REVIEWER_MODEL', 'gpt-5.6-sol')
if not API_KEY:
    raise SystemExit('OPENAI_API_KEY is required')

paths = [
    Path('docs/japan-real-estate-agent-protocol.md'),
    Path('reports/five-market-comparison-2026-08-21.md'),
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]
parts = []
for p in paths:
    if p.exists():
        data = p.read_text(errors='replace')
        # Keep each file bounded to avoid runaway prompt size in CI.
        if len(data) > 120_000:
            data = data[:120_000] + '\n[TRUNCATED BY REVIEWER]\n'
        parts.append(f'\n===== FILE: {p} =====\n{data}')

prompt = '''You are the independent adversarial reviewer for a Japan Real Estate Intelligence Agent.

Do not trust the agent's own status labels. Review the supplied repository artifacts and attempt to falsify them.

Mandatory checks:
1. Recalculate any material financing/DSCR/NOI/cap-rate/cash-on-cash/amortization calculations that can be reproduced from stated inputs.
2. Check geography exactly: Tokyo 23 wards vs central 5 wards vs Greater Tokyo; Koto-ku vs Tokyo Bay; Osaka City vs Osaka Prefecture; Fukuoka City vs Fukuoka Prefecture; Sapporo City vs Chitose.
3. Check property type, unit size, observation date, metric definition, gross-vs-net yield, asking-vs-transaction data, and Grade-A-vs-all-grade data.
4. Check whether every VERIFIED material claim has an exact evidence location. HTTP 403 means inaccessible evidence, not proof the claim is false; recommend an accessible replacement source or downgrade the claim.
5. Check contradictions across claims/evidence/calculations/report.
6. Check whether any PENDING/DISPUTED claim drives a ranking or material conclusion.
7. Check whether forecasts have explicit assumptions and calculations.
8. Treat any unresolved BLOCKER as FAIL.

Return concise Markdown with:
- Overall status: PASS / FAIL / PASS_WITH_WARNINGS
- Material error count
- BLOCKER findings
- MAJOR findings
- MINOR findings
- Required fixes
- Questions requiring evidence
- Whether the report is eligible for APPROVED

Do not create a new investment ranking. Do not assume the agent is correct.'''

payload = {
    'model': MODEL,
    'input': prompt + '\n\nREPOSITORY ARTIFACTS:\n' + '\n'.join(parts),
}
req = Request(
    'https://api.openai.com/v1/responses',
    data=json.dumps(payload).encode('utf-8'),
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'},
    method='POST',
)
with urlopen(req, timeout=120) as resp:
    result = json.loads(resp.read().decode('utf-8'))

output = result.get('output_text')
if not output:
    # Compatible fallback for response objects where output_text is not surfaced at top level.
    chunks = []
    for item in result.get('output', []):
        for content in item.get('content', []):
            if isinstance(content, dict) and content.get('type') == 'output_text':
                chunks.append(content.get('text', ''))
    output = '\n'.join(chunks).strip()

if not output:
    raise SystemExit('Reviewer returned no text')

Path('verification/automatic-review.md').write_text(
    '# Automatic External Review\n\n' +
    f'Model: `{MODEL}`\n\n' +
    output + '\n'
)
print(output)
