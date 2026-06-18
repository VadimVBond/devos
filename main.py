import typer
from devos.cli.commands import project, ai, task

app = typer.Typer(
    name="devos",
    help="DevOS: AI Developer Operating Layer",
    no_args_is_help=True
)

# Подключение групп команд
app.add_typer(project.app, name="project")
app.add_typer(ai.app, name="ai")
app.add_typer(task.app, name="task")

@app.command()
def info():
    """Показать информацию о системе DevOS."""
    typer.secho("🔧 DevOS Kernel v0.1.0", fg=typer.colors.CYAN, bold=True)
    typer.echo("Orchestration Layer for AI-Driven Development")

if __name__ == "__main__":
    app()
