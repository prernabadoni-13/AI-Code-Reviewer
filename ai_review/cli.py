import typer

app = typer.Typer(help="AI Review Tool CLI")

# --- Sub-command 1: Review ---
@app.command()
def review(path: str = "."):
    """
    Run code review on the specified folder (default=current folder)
    """
    typer.echo(f"🔍 Running AI Review on: {path}")
    # Placeholder: later we'll call scanner & analyzer here

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
