import os
import random
from shiny import App
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import click


class StickyCookie(BaseHTTPMiddleware):
    def __init__(
        self, app: App, value: str, key: str = "sticky", verbose: bool = False
    ):
        super().__init__(app)
        self.value = value
        self.key = key
        self.verbose = verbose

    async def dispatch(self, request, call_next):
        sticky = request.cookies.get(self.key)
        if sticky and self.verbose:

            if sticky != self.value:
                # there is no garrantee that the cookie value will
                # be hash mapped to here by nginx.
                click.secho(
                    f"sticky missmatch: {sticky} != {self.value}", fg="red", bold=True
                )
            else:
                click.secho(
                    f"sticky match: {sticky} == {self.value}", fg="green", bold=True
                )
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
        Middleware(StickyCookie, value=INSTANCE_COOKIE, key="sticky", verbose=False)
    )
    return app
