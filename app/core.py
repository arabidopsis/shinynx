from __future__ import annotations
from typing import TYPE_CHECKING
from shiny import ui, render
from starlette.responses import PlainTextResponse
from .sticky import INSTANCE_COOKIE
from .shared import JS

if TYPE_CHECKING:
    from shiny import Inputs, Outputs, Session

# https://github.com/posit-dev/py-shiny/blob/7ba8f90a44ee25f41aa8c258eceeba6807e0017a/examples/load_balance/app.py

app_ui = ui.page_fluid(
    ui.markdown(
        f"""
        ## Sticky load balancing test

        The purpose of this app is to determine if HTTP requests made by the client are
        correctly routed back to the same Python process where the session resides. It
        is only useful for testing deployments that load balance traffic across more
        than one Python process.

        If this test fails, it means that sticky load balancing is not working, and
        certain Shiny functionality (like file upload/download or server-side selectize)
        are likely to randomly fail.

        We are targetting the shiny instance with "sticky" cookie value: <code>{INSTANCE_COOKIE}</code>
        """
    ),
    ui.tags.div(
        {"class": "card"},
        ui.tags.div(
            {"class": "card-body font-monospace"},
            ui.tags.div("Attempts: ", ui.tags.span("0", id="count")),
            ui.tags.div("Status: ", ui.tags.span(id="status")),
            ui.tags.div("Backend: ", ui.tags.span(id="source")),
            ui.output_ui("out"), # see def out() in server
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.ui
    def out():
        # Register a dynamic route for the client to try to connect to.
        # It does nothing, just the 200 status code is all that the client
        # will care about.
        url = session.dynamic_route(
            "test",
            lambda req: PlainTextResponse("OK", headers={"Cache-Control": "no-cache"}),
        )

        # Send JS code to the client to repeatedly hit the dynamic route.
        # It will succeed if and only if we reach the correct Python
        # process.

        return [
            ui.tags.script(f"window.URL = '{url}';"),
            ui.tags.script(JS),
        ]
