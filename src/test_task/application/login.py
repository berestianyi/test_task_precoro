from typing import Optional
from flask import current_app
from flask_login import UserMixin

from src.test_task.application import login_manager

class UserDTO(UserMixin):
    def __init__(self, id: int, email: str):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id: str) -> Optional[UserDTO]:
    try:
        uow_factory = current_app.service_container.user_uow
        with uow_factory() as uow:
            user = uow.user_repo.get_by_id(int(user_id))
            if user:
                return UserDTO(id=user.id, email=user.email)
    except Exception as e:
        current_app.logger.error("user_loader failed", exc_info=e)
        return None
