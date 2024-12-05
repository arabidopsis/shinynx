from __future__ import annotations

import uvicorn
import click
from .utils import run_app


@click.command()
@click.option("-w", "--workers", default=4)
@click.option(
    "--log-level",
    type=click.Choice(list(uvicorn.config.LOG_LEVELS.keys())),
    default="info",
    help="Log level.",
    show_default=True,
)
@click.option("-m", "--method", type=click.Choice(["core", "express"]), default="core")
def run(workers: int, method: str, log_level: str):
    """Run uvicorn processes running app.{asgi|esgi}:app"""

    # we can't use `shiny run` since it *only* uses ports and not unix domain sockets
    m = {"core": "asgi", "express": "esgi"}[method]
    run_app(f"app.{m}:app", workers=workers, log_level=log_level)


if __name__ == "__main__":
    run()
