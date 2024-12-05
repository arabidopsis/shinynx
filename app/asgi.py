from shiny import App
from .sticky import init_sticky
from .core import app_ui, server
from .utils import add_route

app = App(app_ui, server)


init_sticky(app)


async def about(req):
    from starlette.responses import HTMLResponse

    return HTMLResponse(str(app_ui))


add_route(app, "/about", about, name="about")
