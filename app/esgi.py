from pathlib import Path
from shiny import App
from shiny.express import wrap_express_app
from app.sticky import init_sticky

def appify(express_py_file: Path) -> App:
    app = wrap_express_app(express_py_file)
    init_sticky(app)
    return app



app = appify(Path(__file__).parent / "express.py")

