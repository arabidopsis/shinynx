from __future__ import annotations

from shiny.express import render
from shiny.express import session
from shiny.express import ui
from starlette.responses import PlainTextResponse

from .shared import JS
from shinynx.sticky import INSTANCE_COOKIE

ui.markdown(
    f"""
## Sticky load balancing test (Express)

The purpose of this app is to determine if HTTP requests made by the client are
correctly routed back to the same Python process where the session resides. It
is only useful for testing deployments that load balance traffic across more
than one Python process.

If this test fails, it means that sticky load balancing is not working, and
certain Shiny functionality (like file upload/download or server-side selectize)
are likely to randomly fail.

We are targetting the shiny instance with "sticky" cookie value: <code>{INSTANCE_COOKIE}</code>
""",
)


with ui.tags.div(class_="card"):

    with ui.tags.div(class_="card-body font-monospace"):

        ui.tags.div("Attempts: ", ui.tags.span("0", id="count"))
        ui.tags.div("Status: ", ui.tags.span(id="status"))
        ui.tags.div("Backend: ", ui.tags.span(id="source"))


# @output
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
