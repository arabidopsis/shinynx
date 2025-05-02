from __future__ import annotations

import os
import random

from shiny import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class StickyCookie(BaseHTTPMiddleware):
    def __init__(
        self,
        app: App,
        value: str,
        key: str = "sticky"
    ):
        super().__init__(app)
        self.key = key
        self.value = value

    async def dispatch(self, request, call_next):
        sticky = request.cookies.get(self.key)
        response = await call_next(request)
        if not sticky:
            response.set_cookie(key=self.key, value=self.value)
        return response


endpoint = os.environ.get("ENDPOINT")


INSTANCE_COOKIE = endpoint if endpoint else f"st-{random.random()}"


def init_sticky(app: App) -> App:
    """Ensure app sends out a "sticky" cookie so it can be identified by nginx"""
    # see hash $cookie_sticky consistent;
    # in sticky.conf
    app.starlette_app.user_middleware.append(
        Middleware(StickyCookie, value=INSTANCE_COOKIE, key="sticky"),
    )
    return app
