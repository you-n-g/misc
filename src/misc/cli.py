"""Command Line Interface."""
import time
from pathlib import Path

import typer
import wan
from loguru import logger

app = typer.Typer()


@app.command()
def run() -> None:
    """Run command."""


@app.command()
def check_health(p: Path) -> None:
    # the file should be edited in last 5 hours
    if p.stat().st_mtime < time.time() - 5 * 3600:
        info = f"{p} is not edited for at least 5 hours"
        logger.info(info)
        wan.ntf(info)
    else:
        logger.info("It is edited recently")


@app.command()
def start_teleread() -> None:
    from misc.teleread.server import start_client

    start_client()


typer_click_object = typer.main.get_command(app)

if __name__ == "__main__":
    app()  # pragma: no cover
