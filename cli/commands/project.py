import typer

app = typer.Typer(help="Управление проектами")

@app.command()
def list():
    """Список всех проектов в реестре."""
    typer.echo("Список проектов пуст.")
