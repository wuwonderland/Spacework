#!/usr/bin/env python3
import os
import urllib.parse
import urllib.request
from pathlib import Path

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
if not bot_token or not chat_id:
    raise SystemExit('TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required')

branch = os.environ.get('GITHUB_REF_NAME', 'unknown')
sha = os.environ.get('GITHUB_SHA', 'unknown')[:12]
review_file = Path('verification/automatic-review.md')
review = review_file.read_text(errors='replace') if review_file.exists() else 'No AI review file was produced.'

# Keep Telegram as a status channel, not the research database.
lines = [x.strip() for x in review.splitlines() if x.strip()]
summary = '\n'.join(lines[:8])
message = (
    'Japan Real Estate Agent — automatic review\n\n'
    f'Branch: {branch}\nCommit: {sha}\n\n'
    f'{summary}\n\n'
    'Full evidence/review: GitHub repository.'
)

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message[:3900]}).encode()
req = urllib.request.Request(url, data=data, method='POST')
with urllib.request.urlopen(req, timeout=30) as resp:
    if resp.status != 200:
        raise SystemExit(f'Telegram notification failed: HTTP {resp.status}')
print('Telegram notification sent')
