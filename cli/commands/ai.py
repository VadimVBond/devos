import typer

app = typer.Typer(help="Взаимодействие с AI")

@app.command()
def ask(query: str):
    """Задать вопрос AI роутеру."""
    typer.echo(f"Запрос к AI: {query}")
