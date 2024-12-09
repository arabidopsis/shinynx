from __future__ import annotations
from pathlib import Path
from typing import Callable, Any, TYPE_CHECKING
import sys
import subprocess
from dataclasses import dataclass

from shiny import App
from shiny.express import wrap_express_app
import click

from .sticky import init_sticky

if TYPE_CHECKING:
    from starlette.requests import Request


def appify(express_py_file: Path) -> App:
    """Turn an Express app file into an App"""
    app = wrap_express_app(express_py_file)
    init_sticky(app)
    # if debug is not None:
    #     app._debug = debug
    return app


@dataclass
class Runner:
    cmd: list[str]
    directory: str = "."
    env: dict[str, str] | None = None

    def getenv(self) -> dict[str, str] | None:
        if not self.env:
            return None
        return self.env  # return {**os.environ, **self.env}

    def start(self) -> subprocess.Popen[bytes]:

        return subprocess.Popen(
            self.cmd,
            cwd=self.directory,
            env=self.getenv(),
            shell=False,
        )


def add_route(
    app: App, path: str, func: Callable[[Request], Any], name: str | None = None
) -> None:
    from starlette.routing import Route

    route = Route(path, func, name=name)
    # need to insert this! Can't append! so add_route can't work.
    app.starlette_app.router.routes.insert(0, route)


def run_app(
    app: str,
    *,
    workers: int = 3,
    working_dir: str = ".",
    log_level: str = "info",
    uvicornargs: tuple[str, ...] = (),
) -> None:
    procs = []
    # Don't allow shiny to use uvloop! (see _main.py)
    # https://github.com/posit-dev/py-shiny/issues/1373
    for iw in range(1, workers + 1):
        socket = f"app{iw}.sock"
        runner = Runner(
            [
                sys.executable,
                "-m",
                "uvicorn",
                "--loop=asyncio",
                "--lifespan=on",
                f"--log-level={log_level}",
                "--uds",
                socket,
                *uvicornargs,
                app,
            ],
            env=dict(ENDPOINT=socket),
            directory=working_dir,
        )
        procs.append(runner)

    todo = [p.start() for p in procs]

    try:
        for t in todo:
            t.wait()

    except KeyboardInterrupt:
        for t in todo:
            t.wait(0.5)
