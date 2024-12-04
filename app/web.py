from __future__ import annotations

import os

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
        return self.env # return {**os.environ, **self.env}

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
def run(workers: int):
    """Run uvicorn processes running app.asgi:app"""
    import sys
    procs = [
        Runner(f"app{i}", [sys.executable, '-m', "uvicorn", "--uds", f"app{i}.sock", "app.asgi:app"],
            env=dict(ENDPOINT= f"app{i}.sock"))
        for i in range(1, workers + 1)
    ]

    todo = [p.start() for p in procs]

    try:
        for t in todo:
            t.wait()

    except KeyboardInterrupt:
        for t in todo:
            t.wait(.5)
        return


run()
