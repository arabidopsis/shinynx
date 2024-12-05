from pathlib import Path
from .utils import appify


app = appify(Path(__file__).parent / "express.py")
