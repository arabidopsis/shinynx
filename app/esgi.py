from pathlib import Path
from shiny import App
from shiny.express import wrap_express_app
from .sticky import init_sticky


def appify(express_py_file: Path) -> App:
    _app = wrap_express_app(express_py_file)
    init_sticky(_app)
    # if debug is not None:
    #     app._debug = debug
    return _app


app = appify(Path(__file__).parent / "express.py")
