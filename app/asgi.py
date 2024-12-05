from shiny import App
from .sticky import init_sticky
from .core import app_ui, server

app = App(app_ui, server)


init_sticky(app)
