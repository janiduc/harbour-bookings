"""Create the seed issues in this project's GitHub repository.

Usage (PowerShell):
    $env:GITHUB_TOKEN = "<fine-grained token with Issues: read and write>"
    $env:GITHUB_REPO = "owner/harbour-bookings"
    python scripts/file_issues.py            # create all seed issues
    python scripts/file_issues.py --dry-run  # only print what would be created

Uses only the standard library. Issues that already exist with the same title are skipped,
so the script is safe to run twice.
"""
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent / "issues" / "seed_issues.json"


def call(method, url, token, payload=None):
    req = urllib.request.Request(
        url, method=method, data=json.dumps(payload).encode() if payload else None,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "harbour-bookings-seed"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read() or b"null")


def main():
    dry_run = "--dry-run" in sys.argv
    issues = json.loads(SEED.read_text(encoding="utf-8"))
    if dry_run:
        for issue in issues:
            print(f"would create: {issue['title']}")
        return
    token, repo = os.getenv("GITHUB_TOKEN"), os.getenv("GITHUB_REPO")
    if not token or not repo or "/" not in repo:
        sys.exit("Set GITHUB_TOKEN and GITHUB_REPO=owner/name first.")
    base = f"https://api.github.com/repos/{repo}/issues"
    try:
        existing = {i["title"] for i in call("GET", f"{base}?state=all&per_page=100", token)}
        for issue in issues:
            if issue["title"] in existing:
                print(f"skipped (exists): {issue['title']}")
                continue
            created = call("POST", base, token, issue)
            print(f"created #{created['number']}: {issue['title']}")
    except urllib.error.HTTPError as exc:
        sys.exit(f"GitHub returned HTTP {exc.code}. Check the token's permissions and the repo name.")


if __name__ == "__main__":
    main()
