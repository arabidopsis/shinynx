from __future__ import annotations

from pathlib import Path

from .utils import appify
from .utils import try_module
from .utils import unescape_from_var_name


# If someone requests app.eapp:_2f_path_2f_to_2f_app_2e_py, then we will call
# wrap_express_app(Path("/path/to/app.py")) and return the result.
def __getattr__(name: str) -> object:
    name = unescape_from_var_name(name)
    name = try_module(name)
    return appify(Path(name))
