from __future__ import annotations

import webbrowser
import click


@click.command()
@click.option("-n", "--nbrowser", default=4)
def run(nbrowser: int):
    """Fire up browsers"""

    url = "http://127.0.0.1:8080"
    for _ in range(nbrowser):
        webbrowser.open_new_tab(url)

run()
