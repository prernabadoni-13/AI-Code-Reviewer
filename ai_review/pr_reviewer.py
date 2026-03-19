import os
import requests
from typing import Dict, Any

GITHUB_API = "https://api.github.com"

def get_token():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise RuntimeError(
            "\n❌ GitHub token not found.\n"
            "👉 Set it via: export GITHUB_TOKEN=your_token\n"
            "👉 Get a token from: https://github.com/settings/tokens\n"
            "👉 Required scopes: repo, pull_requests"
        )
    return token

def parse_pr_url(pr_url: str) -> tuple:
    parts = pr_url.rstrip("/").split("/")
    owner = parts[-4]
    repo = parts[-3]
    pr_number = parts[-1]
    return owner, repo, pr_number

def get_pr_diff(owner: str, repo: str, pr_number: str) -> list:
    token = get_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(
            f"\n❌ Could not fetch PR files. Status: {response.status_code}\n"
            f"👉 Make sure your token has 'repo' scope\n"
            f"👉 Response: {response.json().get('message', '')}"
        )

    files = response.json()
    result = []
    for f in files:
        result.append({
            "path": f["filename"],
            "content": f.get("patch", ""),
            "sha": f.get("sha", "")
        })
    return result

def get_pr_commit_sha(owner: str, repo: str, pr_number: str) -> str:
    token = get_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    return response.json()["head"]["sha"]

def post_pr_review(owner: str, repo: str, pr_number: str,
                   commit_sha: str, issues: list, complexity: list):
    token = get_token()
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # build inline comments
    comments = []
    for issue in issues:
        emoji = {"error": "🔴", "warning": "🟡", "info": "🔵"}.get(
            issue.get("severity"), "⚪"
        )
        source = issue.get("source", "llm")
        source_tag = "🤖 LLM" if source == "llm" else "📏 Rule"
        comments.append({
            "path": issue.get("file"),
            "line": issue.get("line", 1),
            "side": "RIGHT",
            "body": f"{emoji} **[{issue.get('severity').upper()}]** ({source_tag}): {issue.get('message')}"
        })

    # build summary
    total = len(issues)
    errors = len([i for i in issues if i.get("severity") == "error"])
    warnings = len([i for i in issues if i.get("severity") == "warning"])
    infos = len([i for i in issues if i.get("severity") == "info"])

    summary = f"""## 🤖 AI Code Review Summary

| | Count |
|---|---|
| 🔴 Errors | {errors} |
| 🟡 Warnings | {warnings} |
| 🔵 Info | {infos} |
| **Total** | **{total}** |

"""
    if complexity:
        summary += "### 📊 Complexity Analysis\n"
        for c in complexity:
            score = c.get("score", 0)
            emoji = "🟢" if score <= 3 else "🟡" if score <= 6 else "🔴"
            summary += f"- {emoji} `{c.get('file')}` — `{c.get('function')}` score={score}/10: {c.get('message')}\n"

    if total == 0:
        summary += "\n✅ No issues found! Great work.\n"

    # post review
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    payload = {
        "commit_id": commit_sha,
        "body": summary,
        "event": "COMMENT",
        "comments": comments
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in (200, 201):
        return True
    else:
        raise RuntimeError(
            f"\n❌ Failed to post review. Status: {response.status_code}\n"
            f"👉 Response: {response.json()}"
        )