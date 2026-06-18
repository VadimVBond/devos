import typer

app = typer.Typer(help="Управление задачами")

@app.command()
def status():
    """Статус текущих задач."""
    typer.echo("Нет активных задач.")
