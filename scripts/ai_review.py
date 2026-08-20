#!/usr/bin/env python3
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen

api_key = os.environ.get('OPENAI_API_KEY')
model = os.environ.get('REVIEWER_MODEL', 'gpt-5.6-sol')
if not api_key:
    raise SystemExit('OPENAI_API_KEY is required')

paths = [
    Path('docs/japan-real-estate-agent-protocol.md'),
    Path('reports/five-market-comparison-2026-08-21.md'),
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]
parts = []
for path in paths:
    if path.exists():
        content = path.read_text(errors='replace')
        if len(content) > 120_000:
            content = content[:120_000] + '\n[TRUNCATED]\n'
        parts.append(f'===== {path} =====\n{content}')

prompt = '''You are the independent adversarial reviewer for a Japan Real Estate Intelligence Agent.

Review the repository artifacts supplied below. Do not trust any self-reported VERIFIED, PASS, COMPLETE, or APPROVED label.

Check:
1. Arithmetic: recalculate material financing, amortization, ADS, NOI, DSCR, cap rate, cash-on-cash, and sensitivity calculations that can be reproduced from stated inputs.
2. Geography: Tokyo 23 wards vs central 5 wards vs Greater Tokyo; Koto-ku vs Tokyo Bay; Osaka City vs Osaka Prefecture; Fukuoka City vs Fukuoka Prefecture; Sapporo City vs Chitose.
3. Normalization: property type, unit size, observation period, metric definition, gross vs net, asking vs transaction, Grade A vs all-grade.
4. Evidence: exact value must be locatable in the evidence. HTTP 403 means inaccessible evidence, not proof of falsity. Recommend replacement evidence or downgrade the claim.
5. Contradictions across reports, claims, evidence, and calculations.
6. PENDING/DISPUTED inputs driving rankings or material conclusions.
7. Unsupported forecasts and infrastructure catalysts.
8. Any unresolved BLOCKER means FAIL.

Do not create a new investment ranking.

Return Markdown with:
Overall status: PASS / FAIL / PASS_WITH_WARNINGS
Material errors count
BLOCKER findings
MAJOR findings
MINOR findings
Required fixes
Unresolved evidence questions
Approval eligibility'''

payload = {'model': model, 'input': prompt + '\n\nREPOSITORY ARTIFACTS:\n' + '\n\n'.join(parts)}
request = Request(
    'https://api.openai.com/v1/responses',
    data=json.dumps(payload).encode(),
    headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
    method='POST',
)
with urlopen(request, timeout=120) as response:
    result = json.loads(response.read().decode())

output = result.get('output_text')
if not output:
    chunks = []
    for item in result.get('output', []):
        for content in item.get('content', []):
            if isinstance(content, dict) and content.get('type') == 'output_text':
                chunks.append(content.get('text', ''))
    output = '\n'.join(chunks).strip()
if not output:
    raise SystemExit('No reviewer output returned')

Path('verification/automatic-review.md').write_text(
    '# Automatic External Review\n\n' + f'Model: `{model}`\n\n' + output + '\n'
)
print(output)
