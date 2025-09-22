from contextlib import AbstractContextManager

from sqlalchemy.orm import Session

from src.test_task.persistence.repository.user import UserRepository



class UserUoW(AbstractContextManager):
    def __init__(self, session_factory, user_repo):
        self._session_factory = session_factory
        self._user_repo = user_repo

        self.db: Session | None = None
        self.user_repo: UserRepository | None = None

    def __enter__(self):
        self.db = self._session_factory()
        self.users = self._user_repo(self.db)
        return self

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.db.commit()
            else:
                self.db.rollback()
        finally:
            self.db.close()