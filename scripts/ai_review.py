#!/usr/bin/env python3
import json
import os
import time
import random
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_KEY = os.environ.get('OPENAI_API_KEY')
PRIMARY_MODEL = os.environ.get('REVIEWER_MODEL', 'gpt-5.6-luna')
ESCALATION_MODEL = os.environ.get('ESCALATION_MODEL', 'gpt-5.6-sol')
MAX_RETRIES = 5

if not API_KEY:
    raise SystemExit('OPENAI_API_KEY is required')

paths = [
    Path('reports/five-market-comparison-2026-08-21.md'),
    Path('calculations/five-market-calculations.md'),
    Path('claims/five-market-claims.md'),
    Path('verification/external-review.md'),
]

MAX_FILE_CHARS = 45_000
MAX_TOTAL_CHARS = 120_000
parts = []
total = 0
for p in paths:
    if not p.exists():
        continue
    data = p.read_text(errors='replace')
    if len(data) > MAX_FILE_CHARS:
        data = data[:MAX_FILE_CHARS] + '\n[TRUNCATED FOR REVIEW]\n'
    remaining = MAX_TOTAL_CHARS - total
    if remaining <= 0:
        break
    data = data[:remaining]
    parts.append(f'\n===== FILE: {p} =====\n{data}')
    total += len(data)

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

def call_model(model: str) -> tuple[str, bool]:
    payload = {
        'model': model,
        'input': prompt + '\n\nREPOSITORY ARTIFACTS:\n' + '\n'.join(parts),
    }
    body = json.dumps(payload).encode('utf-8')
    for attempt in range(MAX_RETRIES):
        req = Request(
            'https://api.openai.com/v1/responses',
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {API_KEY}',
            },
            method='POST',
        )
        try:
            with urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode('utf-8'))
            output = result.get('output_text')
            if not output:
                chunks = []
                for item in result.get('output', []):
                    for content in item.get('content', []):
                        if isinstance(content, dict) and content.get('type') == 'output_text':
                            chunks.append(content.get('text', ''))
                output = '\n'.join(chunks).strip()
            if not output:
                raise RuntimeError('Reviewer returned no text')
            return output, True
        except HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504):
                raise
            if attempt == MAX_RETRIES - 1:
                return f'REVIEW_CALL_FAILED: HTTP {exc.code}', False
            delay = min(30, (2 ** attempt) + random.uniform(0.5, 2.5))
            print(f'OpenAI HTTP {exc.code}; retrying in {delay:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})')
            time.sleep(delay)
        except (URLError, TimeoutError) as exc:
            if attempt == MAX_RETRIES - 1:
                return f'REVIEW_CALL_FAILED: {type(exc).__name__}', False
            delay = min(30, (2 ** attempt) + random.uniform(0.5, 2.5))
            print(f'OpenAI transport error; retrying in {delay:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})')
            time.sleep(delay)

    return 'REVIEW_CALL_FAILED: unknown', False

primary_output, primary_ok = call_model(PRIMARY_MODEL)
output = primary_output
model_used = PRIMARY_MODEL

# Escalate only when the cheap reviewer finds a substantive problem.
upper = primary_output.upper()
needs_escalation = (
    'STATUS: FAIL' in upper
    or 'BLOCKER' in upper
    or 'MAJOR FINDINGS' in upper and 'NONE' not in upper
    or not primary_ok
)

if needs_escalation and ESCALATION_MODEL and ESCALATION_MODEL != PRIMARY_MODEL:
    escalation_output, escalation_ok = call_model(ESCALATION_MODEL)
    if escalation_ok:
        output = escalation_output
        model_used = f'{PRIMARY_MODEL} → {ESCALATION_MODEL}'
    else:
        output = primary_output + '\n\nESCALATION REVIEW FAILED: ' + escalation_output

Path('verification/automatic-review.md').write_text(
    '# Automatic External Review\n\n'
    f'Primary model: `{PRIMARY_MODEL}`\n\n'
    f'Final model used: `{model_used}`\n\n'
    + output + '\n'
)
print(output)
