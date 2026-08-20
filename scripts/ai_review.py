#!/usr/bin/env python3
import json
import os
import time
import random
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_KEY = os.environ.get('OPENAI_API_KEY')
MODEL = os.environ.get('REVIEWER_MODEL', 'gpt-5.6-sol')
if not API_KEY:
    raise SystemExit('OPENAI_API_KEY is required')

# Keep the reviewer request intentionally compact. The reviewer should inspect
# the most decision-relevant artifacts, not receive the entire repository.
paths = [
    Path('reports/five-market-comparison-2026-08-21.md'),
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]
parts = []
TOTAL_BUDGET = 70_000
remaining = TOTAL_BUDGET
for p in paths:
    if remaining <= 0:
        break
    if p.exists():
        data = p.read_text(errors='replace')
        limit = min(len(data), remaining)
        if len(data) > limit:
            data = data[:limit] + '\n[TRUNCATED BY REVIEWER]\n'
        parts.append(f'\n===== FILE: {p} =====\n{data}')
        remaining -= len(data)

prompt = '''You are the independent adversarial reviewer for a Japan Real Estate Intelligence Agent.

Do not trust the agent's own status labels. Attempt to falsify the supplied artifacts.

Mandatory checks:
1. Recalculate material financing/DSCR/NOI/cap-rate/cash-on-cash/amortization calculations that can be reproduced from stated inputs.
2. Check exact geography: Tokyo 23 wards vs central 5 wards vs Greater Tokyo; Koto-ku vs Tokyo Bay; Osaka City vs Osaka Prefecture; Fukuoka City vs Fukuoka Prefecture; Sapporo City vs Chitose.
3. Check property type, unit size, observation date, metric definition, gross-vs-net yield, asking-vs-transaction data, and Grade-A-vs-all-grade data.
4. VERIFIED requires exact evidence location. HTTP 403 means inaccessible evidence, not proof the claim is false; recommend an accessible replacement source or downgrade.
5. Check contradictions across claims, calculations, and report.
6. PENDING/DISPUTED inputs must not drive rankings or material conclusions.
7. Forecasts require explicit assumptions and calculations.
8. Any unresolved BLOCKER means FAIL.

Return concise Markdown:
- Overall status: PASS / FAIL / PASS_WITH_WARNINGS
- Material error count
- BLOCKER findings
- MAJOR findings
- MINOR findings
- Required fixes
- Evidence questions
- APPROVED eligibility

Do not create a new investment ranking.'''

payload = {
    'model': MODEL,
    'input': prompt + '\n\nREPOSITORY ARTIFACTS:\n' + '\n'.join(parts),
    'max_output_tokens': 3500,
}

req_data = json.dumps(payload).encode('utf-8')
last_error = None
for attempt in range(5):
    req = Request(
        'https://api.openai.com/v1/responses',
        data=req_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
            'User-Agent': 'Spacework-Japan-RE-Reviewer/1.0',
        },
        method='POST',
    )
    try:
        with urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode('utf-8'))
        break
    except HTTPError as exc:
        last_error = exc
        if exc.code == 429 and attempt < 4:
            # Exponential backoff with jitter for transient rate limits.
            delay = (2 ** attempt) * 3 + random.uniform(0, 2)
            print(f'OpenAI 429; retrying in {delay:.1f}s (attempt {attempt + 1}/5)')
            time.sleep(delay)
            continue
        raise
    except (URLError, TimeoutError) as exc:
        last_error = exc
        if attempt < 4:
            delay = (2 ** attempt) * 2 + random.uniform(0, 2)
            print(f'OpenAI transport error; retrying in {delay:.1f}s (attempt {attempt + 1}/5)')
            time.sleep(delay)
            continue
        raise
else:
    raise RuntimeError(f'OpenAI reviewer failed after retries: {last_error}')

output = result.get('output_text')
if not output:
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
