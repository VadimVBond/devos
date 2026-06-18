import typer

app = typer.Typer(name="devos", help="DevOS: AI-powered development platform")

@app.command()
def info():
    """Показать информацию о DevOS."""
    typer.echo("DevOS Platform Core v0.1.0")

if __name__ == "__main__":
    app()
