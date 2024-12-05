from __future__ import annotations


import sys
import subprocess
from dataclasses import dataclass


import click


@dataclass
class Runner:
    name: str
    cmd: list[str]
    directory: str = "."
    env: dict[str, str] | None = None
    showcmd: bool = False
    shell: bool = False

    def getenv(self) -> dict[str, str] | None:
        if not self.env:
            return None
        return self.env  # return {**os.environ, **self.env}

    def start(self) -> subprocess.Popen[bytes]:
        if self.showcmd:
            click.secho(" ".join(str(s) for s in self.cmd), fg="blue")

        return subprocess.Popen(
            self.cmd,
            cwd=self.directory,
            env=self.getenv(),
            shell=self.shell,
        )


@click.command()
@click.option("-w", "--workers", default=4)
@click.option("-m", "--method", type=click.Choice(["core", "express"]), default="core")
def run(workers: int, method: str):
    """Run uvicorn processes running app.{asgi|esgi}:app"""

    # we can't use `shiny run` since it *only* uses ports and not unix domain sockets
    m = {"core": "asgi", "express": "esgi"}[method]
    # Don't allow shiny to use uvloop! (see _main.py)
    # https://github.com/posit-dev/py-shiny/issues/1373
    procs = [
        Runner(
            f"app{i}",
            [
                sys.executable,
                "-m",
                "uvicorn",
                "--loop=asyncio",
                "--lifespan=on",
                "--uds",
                f"app{i}.sock",
                f"app.{m}:app",
            ],
            env=dict(ENDPOINT=f"app{i}.sock"),
        )
        for i in range(1, workers + 1)
    ]

    todo = [p.start() for p in procs]

    try:
        for t in todo:
            t.wait()

    except KeyboardInterrupt:
        for t in todo:
            t.wait(0.5)
        return

if __name__ == '__main__':
    run()
