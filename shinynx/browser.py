from __future__ import annotations

import time
import webbrowser

import click


@click.command()
@click.option("-s", "--sleep", default=0.0, help="sleep between firing up new tab")
@click.option(
    "-n",
    "--nbrowser",
    default=4,
    help="number of browsers to invoke",
    show_default=True,
)
def run(nbrowser: int, sleep: float):
    """Fire up browsers"""

    url = "http://127.0.0.1:8080"
    for _ in range(nbrowser):
        webbrowser.open_new_tab(url)
        if sleep:
            time.sleep(sleep)


if __name__ == "__main__":
    run()
