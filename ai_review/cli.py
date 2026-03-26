import typer
import os
from ai_review.scanner import scan_repo
from ai_review.engines.combined_engine import CombinedEngine
from ai_review.engines.formatter import format_issues
from ai_review.reporter import generate_html_report

app = typer.Typer(help="AI Code Review Tool")

@app.command()
def review(
    path: str = typer.Argument(".", help="Path to the project to review"),
    model: str = typer.Option(
        None, "--model", "-m",
        help="Ollama model to use (default: llama3.2 or OLLAMA_MODEL env var)"
    ),
    html: bool = typer.Option(
        False, "--html",
        help="Generate HTML report and open in browser"
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

        if html:
            # generate HTML report and open in browser
            report_path = generate_html_report(issues, complexity, path)
            typer.echo(f"\n✅ Review complete!")
            typer.echo(f"📄 Report saved: {report_path}")
            typer.echo(f"🌐 Opening in browser...")
        else:
            # normal terminal output
            typer.echo(format_issues(issues))

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
    url: str = typer.Argument(..., help="GitHub PR URL"),
    model: str = typer.Option(None, "--model", "-m")
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

        files = get_pr_diff(owner, repo_name, pr_number)
        typer.echo(f"📄 Found {len(files)} changed files")

        project_data = {"files": files}

        typer.echo("⚙️  Running rule-based checks...")
        typer.echo("🤖 Running LLM review...")
        engine = CombinedEngine(model=model)
        result = engine.review_project(project_data)

        issues = result.get("issues", [])
        complexity = result.get("complexity", [])

        typer.echo(f"📝 Found {len(issues)} issues — posting to PR...")

        commit_sha = get_pr_commit_sha(owner, repo_name, pr_number)
        post_pr_review(owner, repo_name, pr_number, commit_sha, issues, complexity)

        typer.echo(f"✅ Review posted on PR #{pr_number}!")
        typer.echo(f"👉 View at: {url}")

    except Exception as e:
        typer.echo(f"❌ PR review failed: {e}")

@app.command()
def setup():
    """Check and setup all dependencies for AI Code Review Tool."""
    import subprocess
    import shutil

    typer.echo("⚙️  Running setup checks...\n")

    if shutil.which("ollama"):
        typer.echo("✅ Ollama is installed")
    else:
        typer.echo("❌ Ollama is not installed")
        typer.echo("👉 Install it from: https://ollama.com/download\n")

    model = os.getenv("OLLAMA_MODEL", "llama3.2")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if model in result.stdout:
            typer.echo(f"✅ Model '{model}' is available")
        else:
            typer.echo(f"❌ Model '{model}' not found")
            typer.echo(f"👉 Run: ollama pull {model}\n")
    except Exception:
        typer.echo(f"❌ Could not check models — is Ollama running?\n")

    if os.getenv("GITHUB_TOKEN"):
        typer.echo("✅ GitHub token is set")
    else:
        typer.echo("❌ GitHub token not set")
        typer.echo("👉 Get one from: https://github.com/settings/tokens")
        typer.echo("👉 Then run: export GITHUB_TOKEN=your_token\n")

    typer.echo("\n🎉 Setup check complete!")
    typer.echo("👉 Run 'ai-review review' to start reviewing code")
    typer.echo("👉 Run 'ai-review review --html' to get an HTML report")
    typer.echo("👉 Run 'ai-review pr <url>' to review a GitHub PR")

if __name__ == "__main__":
    app()