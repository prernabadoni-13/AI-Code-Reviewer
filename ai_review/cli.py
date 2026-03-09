import typer
import os
from ai_review.scanner import scan_repo
from ai_review.engines.llm_engine import OllamaLLMEngine
from ai_review.engines.formatter import format_issues

app = typer.Typer()

@app.command()
def review(
    path: str = ".",
    model: str = typer.Option(
        None,
        "--model", "-m",
        help="Ollama model to use (default: phi3:mini or OLLAMA_MODEL env var)"
    )
):
    typer.echo(f"Reviewing project: {path}")
    engine = OllamaLLMEngine(model=model)  # passes None if not set, engine handles default
    project_data = scan_repo(path)
    try:
        result = engine.review_project(project_data)
        issues = result.get("issues", [])
        output = format_issues(issues)
        typer.echo(output)
    except Exception as e:
        typer.echo(f"❌ Review failed: {e}")


# --- Sub-command 2: Setup ---
@app.command()
def setup():
    """
    Setup configuration for AI Review Tool
    """
    typer.echo("⚙️ Running setup...")
    # Placeholder for future setup logic

# CLI entry
if __name__ == "__main__":
    app()