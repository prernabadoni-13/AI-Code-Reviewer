import typer
from ai_review.scanner import scan_repo
from ai_review.engines.llm_engine import OllamaLLMEngine
from ai_review.engines.formatter import format_issues

app = typer.Typer()


@app.command()
def review(path: str = "."):
    typer.echo(f"Reviewing project: {path}")

    engine = OllamaLLMEngine()

    project_data = scan_repo(path)

    try:
        result = engine.review_project(project_data)
        issues = result.get("issues", [])

        output = format_issues(issues)
        typer.echo(output)

    except Exception as e:
        typer.echo(f"❌ Review failed: {e}")