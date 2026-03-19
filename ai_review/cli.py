import typer
import os
from ai_review.scanner import scan_repo
from ai_review.engines.combined_engine import CombinedEngine
from ai_review.engines.formatter import format_issues

app = typer.Typer(help="AI Code Review Tool")

@app.command()
def review(
    path: str = typer.Argument(".", help="Path to the project to review"),
    model: str = typer.Option(
        None, "--model", "-m",
        help="Ollama model to use (default: phi3:mini or OLLAMA_MODEL env var)"
    )
):
    """Run AI code review on the specified folder."""
    typer.echo(f"🔍 Reviewing project: {path}")

    engine = CombinedEngine(model=model)
    project_data = scan_repo(path)

    try:
        result = engine.review_project(project_data)
        issues = result.get("issues", [])
        complexity = result.get("complexity", [])

        # print issues
        typer.echo(format_issues(issues))

        # print complexity
        if complexity:
            typer.echo("\n📊 Complexity Analysis:")
            for c in complexity:
                score = c.get("score", 0)
                emoji = "🟢" if score <= 3 else "🟡" if score <= 6 else "🔴"
                typer.echo(
                    f"{emoji}  {c.get('file')}:{c.get('line')} "
                    f"[{c.get('function')}] score={score}/10 — {c.get('message')}"
                )
        else:
            typer.echo("\n📊 Complexity Analysis: No complexity issues found.")

    except Exception as e:
        typer.echo(f"❌ Review failed: {e}")

@app.command()
def pr(
    url: str = typer.Argument(..., help="GitHub PR URL e.g. https://github.com/owner/repo/pull/123"),
    model: str = typer.Option(
        None, "--model", "-m",
        help="Ollama model to use"
    )
):
    """Review a GitHub PR and post inline comments."""
    from ai_review.pr_reviewer import (
        parse_pr_url, get_pr_diff,
        get_pr_commit_sha, post_pr_review
    )

    typer.echo(f"🔍 Fetching PR: {url}")

    try:
        owner, repo_name, pr_number = parse_pr_url(url)
        typer.echo(f"📂 Repo: {owner}/{repo_name} | PR #{pr_number}")

        # get changed files
        files = get_pr_diff(owner, repo_name, pr_number)
        typer.echo(f"📄 Found {len(files)} changed files")

        # build project data from PR diff
        project_data = {"files": files}

        # run combined engine
        typer.echo("⚙️  Running rule-based checks...")
        typer.echo("🤖 Running LLM review...")
        engine = CombinedEngine(model=model)
        result = engine.review_project(project_data)

        issues = result.get("issues", [])
        complexity = result.get("complexity", [])

        typer.echo(f"📝 Found {len(issues)} issues — posting to PR...")

        # get latest commit sha
        commit_sha = get_pr_commit_sha(owner, repo_name, pr_number)

        # post inline comments
        post_pr_review(owner, repo_name, pr_number, commit_sha, issues, complexity)

        typer.echo(f"✅ Review posted on PR #{pr_number}!")
        typer.echo(f"👉 View at: {url}")

    except Exception as e:
        typer.echo(f"❌ PR review failed: {e}")

@app.command()
def setup():
    """Setup configuration for AI Review Tool."""
    typer.echo("⚙️ Setup coming soon...")

if __name__ == "__main__":
    app()