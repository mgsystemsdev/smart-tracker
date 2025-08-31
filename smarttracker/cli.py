"""
Smart Tracker Command Line Interface.

A Typer-based CLI for interacting with Smart Tracker from the command line.
"""

import typer
from typing import Optional
from smarttracker import __version__

# Create the main Typer app
app = typer.Typer(
    name="smarttracker",
    help="Smart Tracker - A flexible tracking application",
    add_completion=False
)

def version_callback(value: bool):
    """Callback for version option."""
    if value:
        typer.echo(f"Smart Tracker version: {__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None, 
        "--version", 
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """
    Smart Tracker CLI - Your personal tracking application.
    
    Use this command-line interface to interact with Smart Tracker
    features directly from your terminal.
    """
    pass

@app.command()
def hello(
    name: str = typer.Option("World", "--name", "-n", help="Name to greet"),
    enthusiastic: bool = typer.Option(False, "--enthusiastic", "-e", help="Add extra enthusiasm")
):
    """
    Say hello - a friendly greeting command.
    
    This is a sample command to demonstrate the CLI functionality.
    Future commands will provide actual tracking features.
    """
    greeting = f"Hello, {name}!"
    
    if enthusiastic:
        greeting += " 🎉✨"
        typer.echo(typer.style(greeting, fg=typer.colors.GREEN, bold=True))
        typer.echo(typer.style("Welcome to Smart Tracker!", fg=typer.colors.BLUE))
    else:
        typer.echo(greeting)
    
    typer.echo(f"Smart Tracker v{__version__} is ready for your tracking needs!")

@app.command()
def info():
    """
    Display information about Smart Tracker.
    
    Shows version, features, and usage information.
    """
    typer.echo(typer.style("📊 Smart Tracker", fg=typer.colors.BLUE, bold=True))
    typer.echo(f"Version: {__version__}")
    typer.echo()
    typer.echo("Features:")
    typer.echo("  ✅ Web interface (Streamlit)")
    typer.echo("  ✅ Command-line interface (Typer)")
    typer.echo("  ✅ Modular package structure")
    typer.echo("  ✅ Ready for extension")
    typer.echo()
    typer.echo("Usage:")
    typer.echo("  smarttracker hello --name YourName")
    typer.echo("  smarttracker hello --enthusiastic")
    typer.echo("  smarttracker --version")
    typer.echo()
    typer.echo("To run the web interface:")
    typer.echo("  python main.py streamlit")

if __name__ == "__main__":
    app()
