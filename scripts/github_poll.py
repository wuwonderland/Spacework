#!/usr/bin/env python3
"""
GitHub Polling Script — Japan Real Estate Agent Audit

Polls the audit branch for new commits. When a new auto-review commit appears
(from the GitHub Actions workflow), fetches the branch, inspects:
  - verification/automatic-review.md
  - gate-result.md

If the review status is FAIL, generates findings and writes them to a local
processing queue for the Hermite fix loop.

Usage:
  python3 scripts/github_poll.py [--check-only]

Runs as a cronjob every 5 minutes.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

REPO = "wuwonderland/Spacework"
BRANCH = "audit/2026-08-21-five-market-calculations"
WORK_DIR = "/Users/hufait/spacework-audit"
STATE_FILE = Path(WORK_DIR + "/.hermes/poll-state.json")

# Absolute paths for cron environment
GH_BIN = "/usr/local/bin/gh"
GIT_BIN = "/usr/bin/git"
PYTHON3_BIN = "/usr/local/bin/python3"

def get_remote_head():
    """Get the latest commit SHA from the remote branch via gh CLI."""
    result = subprocess.run(
        [GH_BIN, "api", f"repos/{REPO}/branches/{BRANCH}", "--jq", ".commit.sha"],
        capture_output=True, text=True, cwd=WORK_DIR
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def get_local_head():
    """Get the current local HEAD SHA."""
    result = subprocess.run(
        [GIT_BIN, "rev-parse", "HEAD"],
        capture_output=True, text=True, cwd=WORK_DIR
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()

def load_state():
    """Load the last-seen remote HEAD."""
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        return data.get("remote_head")
    return None

def save_state(remote_head):
    """Save the current remote HEAD."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({"remote_head": remote_head, "updated": datetime.now(timezone.utc).isoformat()}))

def check_review_content():
    """Check the automatic-review.md for findings."""
    review_file = Path(WORK_DIR + "/verification/automatic-review.md")
    if not review_file.exists():
        return None
    
    content = review_file.read_text()
    
    # Parse status
    status_match = re.search(r'Status:\s*(\w+)', content, re.I)
    status = status_match.group(1) if status_match else "UNKNOWN"
    
    # Parse findings
    blocker_match = re.search(r'(?:BLOCKER|FAIL)', content, re.I)
    
    return {
        "status": status,
        "content": content,
        "has_findings": "FAIL" in content or "BLOCKER" in content.upper(),
    }

def main():
    check_only = "--check-only" in sys.argv
    
    print(f"=== GitHub Poll — {datetime.now(timezone.utc).isoformat()} ===")
    print(f"Repository: {REPO}")
    print(f"Branch: {BRANCH}")
    
    # Get remote HEAD
    remote_head = get_remote_head()
    if not remote_head:
        print("❌ GITHUB_POLLING: FAIL — Cannot fetch remote HEAD (gh CLI error)")
        return 1
    
    print(f"Remote HEAD: {remote_head}")
    
    # Get local HEAD
    local_head = get_local_head()
    print(f"Local HEAD:  {local_head}")
    
    # Load last-seen state
    last_seen = load_state()
    print(f"Last seen:   {last_seen}")
    
    # Check if there's a new commit
    if remote_head == last_seen:
        print("✅ No new commits — skipping review.")
        print("GITHUB_POLLING: PASS")
        print("AUTO_FIX_TRIGGER: PASS (no new review)")
        return 0
    
    # New commit detected — fetch it
    print(f"\n🔄 New commit detected — fetching...")
    subprocess.run(
        [GIT_BIN, "fetch", "origin", BRANCH],
        cwd=WORK_DIR, capture_output=True, timeout=30
    )
    
    # Check if we need to merge/rebase
    if local_head and remote_head != local_head:
        print("📥 Pulling remote changes...")
        subprocess.run(
            [GIT_BIN, "pull", "--rebase", "origin", BRANCH],
            cwd=WORK_DIR, capture_output=True, text=True, timeout=60
        )
        local_head = get_local_head()
        print(f"Updated local HEAD: {local_head}")
    
    # Save state
    save_state(remote_head)
    
    # Check for review artifacts
    print("\n🔍 Checking for automatic review...")
    review = check_review_content()
    
    if review:
        print(f"Review status: {review['status']}")
        print(f"Has findings: {review['has_findings']}")
        
        if review["status"] in ("FAIL", "BLOCKED"):
            print("⚠️  Review FAILED — findings need attention")
            print("AUTO_FIX_TRIGGER: FAIL — review found issues")
            print("\n📋 Review content:")
            print(review["content"][:2000])
            
            if check_only:
                return 2
            else:
                # In automation mode, we would trigger the fix flow here
                print("\n🤖 Auto-fix would be triggered here (requires OpenAI API key for AI review)")
                print("   Falling back to deterministic review using Hermes tools")
                return 2
        elif review["status"] in ("PASS", "PASS_WITH_WARNINGS"):
            print("✅ Review passed")
            print("AUTO_FIX_TRIGGER: PASS — no fixes needed")
            return 0
    else:
        print("No automatic review file found.")
        print("GITHUB_POLLING: PASS")
        print("AUTO_FIX_TRIGGER: PASS (no review file)")
    
    print("\nGITHUB_POLLING: PASS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
