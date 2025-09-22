from typing import Optional
from flask import current_app
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id: str) -> Optional[object]:
    try:
        uow_factory = current_app.container.user_uow
        with uow_factory() as uow:
            user = uow.user_gateway.get_by_id(int(user_id))
            return user

    except Exception:
        current_app.logger.exception("user_loader failed")
        return None