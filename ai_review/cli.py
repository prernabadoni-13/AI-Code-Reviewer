import pprint
import typer
from ai_review.scanner import scan_repo

app = typer.Typer(help="AI Review Tool CLI")

# --- Sub-command 1: Review ---
@app.command()
def review(path: str = "."):
    """
    Run code review on the specified folder (default=current folder)
    """
    typer.echo(f"🔍 Running AI Review on: {path}")
    files = scan_repo(".")
    print(f"Scanned {len(files)} files")
    pprint.pprint(files)

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
