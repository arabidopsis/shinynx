from __future__ import annotations

from uvicorn.importer import import_from_string

from .utils import init_sticky
from .utils import unescape_from_var_name


def __getattr__(name: str) -> object:
    name = unescape_from_var_name(name)
    app = import_from_string(name)
    return init_sticky(app)
