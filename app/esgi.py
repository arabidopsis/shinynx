from pathlib import Path
from shinyma.utils import appify


app = appify(Path(__file__).parent / "express.py")
