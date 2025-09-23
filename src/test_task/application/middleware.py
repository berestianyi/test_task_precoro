from typing import Optional
from flask import request, g
from flask_login import current_user
from src.test_task.application import settings
from src.test_task.services.user.uuid import UuidIntGenerator


def init_cookie_middleware(app):
    @app.before_request
    def prepare_owner_cookie():
        g._new_owner_cookie = None
        g._delete_owner_cookie = False

        if current_user.is_authenticated:
            if request.cookies.get(settings.COOKIE_NAME):
                g._delete_owner_cookie = True
            return

        if not request.cookies.get(settings.COOKIE_NAME):
            g._new_owner_cookie = str(UuidIntGenerator().generate())

    @app.after_request
    def set_or_delete_owner_cookie(response):
        if g.get("_delete_owner_cookie"):
            response.delete_cookie(
                settings.COOKIE_NAME,
                path=settings.COOKIE_PATH,
                domain=settings.COOKIE_DOMAIN,
                samesite="Lax",
            )
        elif g.get("_new_owner_cookie"):
            response.set_cookie(
                settings.COOKIE_NAME,
                g._new_owner_cookie,
                max_age=settings.COOKIE_MAX_AGE,
                httponly=True,
                samesite="Lax",
                secure=False,
                path=settings.COOKIE_PATH,
                domain=settings.COOKIE_DOMAIN,
            )
        return response


def get_owner_cookie() -> Optional[int]:
    val = request.cookies.get(settings.COOKIE_NAME)
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        return None
