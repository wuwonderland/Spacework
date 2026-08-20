#!/usr/bin/env python3
import os
import urllib.parse
import urllib.request
from pathlib import Path

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
chat_id = os.environ.get('TELEGRAM_CHAT_ID')
if not bot_token or not chat_id:
    raise SystemExit('Telegram secrets not configured')

branch = os.environ.get('GITHUB_REF_NAME', 'unknown')
sha = os.environ.get('GITHUB_SHA', 'unknown')[:12]
review_path = Path('verification/automatic-review.md')
review = review_path.read_text(errors='replace') if review_path.exists() else 'Automatic review unavailable.'
lines = [line.strip() for line in review.splitlines() if line.strip()]
summary = '\n'.join(lines[:10])
message = (
    'Japan Real Estate Agent — automatic review\n\n'
    f'Branch: {branch}\nCommit: {sha}\n\n'
    f'{summary}\n\n'
    'Full evidence and review are stored in GitHub.'
)

url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message[:3900]}).encode()
req = urllib.request.Request(url, data=data, method='POST')
with urllib.request.urlopen(req, timeout=30) as response:
    if response.status != 200:
        raise SystemExit(f'Telegram notification failed: HTTP {response.status}')
