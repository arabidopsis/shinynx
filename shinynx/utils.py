from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from typing import Callable
from typing import TYPE_CHECKING

from shiny.express import wrap_express_app

from .sticky import init_sticky

if TYPE_CHECKING:
    from shiny import App
    from starlette.requests import Request


def appify(express_py_file: Path) -> App:
    """Turn an Express app file into an App"""
    app = wrap_express_app(express_py_file)
    init_sticky(app)
    # if debug is not None:
    #     app._debug = debug
    return app


def add_route(
    app: App,
    path: str,
    func: Callable[[Request], Any],
    name: str | None = None,
) -> None:
    """See also https://shiny.posit.co/py/docs/routing.html."""
    from starlette.routing import Route

    route = Route(path, func, name=name)
    # need to insert this! Can't append! so add_route can't work.
    app.starlette_app.router.routes.insert(0, route)


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


def run_app(
    app: str,
    *,
    workers: int = 3,
    working_dir: str = ".",
    log_level: str = "info",
    express: bool = False,
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
                app_to_uvicorn_app(app, express=express),
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


def app_to_uvicorn_app(app: str, express: bool = False) -> str:
    if express:
        ret = f"shinynx.express:{escape_to_var_name(app)}"
    else:
        if ":" not in app:
            app += ":app"
        ret = f"shinynx.core:{escape_to_var_name(app)}"
    return ret


def try_module(name: str) -> str:
    try:
        module = importlib.util.find_spec(name, None)
        if module is None or module.origin is None:
            return name
        return module.origin
    except ModuleNotFoundError:
        return name


def escape_to_var_name(x: str) -> str:
    """
    Given a string, escape it to a valid Python variable name which contains
    [a-zA-Z0-9_]. All other characters will be escaped to _<hex>_. Also, if the first
    character is a digit, it will be escaped to _<hex>_, because Python variable names
    can't begin with a digit.
    """
    encoded = ""
    is_first = True

    for char in x:
        if is_first and re.match("[0-9]", char):
            encoded += f"_{ord(char):x}_"
        elif re.match("[a-zA-Z0-9]", char):
            encoded += char
        else:
            encoded += f"_{ord(char):x}_"

        if is_first:
            is_first = False

    return encoded


def unescape_from_var_name(x: str) -> str:
    """
    Given a string that was escaped to a Python variable name, unescape it -- that is,
    convert it back to a regular string.
    """

    def replace_func(match: re.Match[str]) -> str:
        return chr(int(match.group(1), 16))

    decoded = re.sub("_([a-zA-Z0-9]+)_", replace_func, x)
    return decoded
