from __future__ import annotations

import click
import uvicorn

from .utils import run_app


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.option("-w", "--workers", default=4)
@click.option("-e", "--express", is_flag=True, help="is an shiny express app")
@click.option(
    "--log-level",
    type=click.Choice(list(uvicorn.config.LOG_LEVELS.keys())),
    default="info",
    help="Log level.",
    show_default=True,
)
@click.option(
    "-d",
    "--working-dir",
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    default=".",
    help="working directory",
    show_default=True,
)
@click.argument("app")
@click.argument("uvicornargs", nargs=-1)
def run(
    workers: int,
    log_level: str,
    app: str,
    working_dir: str,
    express: bool,
    uvicornargs: tuple[str, ...],
):
    """Run uvicorn processes running app.{asgi|esgi}:app"""

    run_app(
        app,
        workers=workers,
        log_level=log_level,
        express=express,
        working_dir=working_dir,
        uvicornargs=uvicornargs,
    )


if __name__ == "__main__":
    run()
