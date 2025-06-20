from sqlalchemy import select

from app.core.security.password_utils import get_password_hash
from app.models.user import User
from app.schemas.user_schema import UserSchema
from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: UserSchema) -> User:
        db_user = User(username=user.username, email=user.email, password=get_password_hash(user.password))
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def update(self, user_id: int, user: UserSchema) -> User:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        db_user.username = user.username
        db_user.email = str(user.email)
        db_user.password = get_password_hash(user.password)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_all(self, limit: int = 2) -> list[User]:
        return list(self.session.scalars(select(User).limit(limit)).all())

    def delete(self, user_id: int) -> None:
        db_user = self.session.scalar(select(User).where(User.id == user_id))
        self.session.delete(db_user)
        self.session.commit()

    def get_detail_if_username_or_email_exists(self, username: str = None, email: str = None) -> str | None:
        db_user = self.session.scalar(select(User).where((User.username == username) | (User.email == email)))
        if db_user:
            if db_user.username == username:
                return "User with this username already exists."
            if db_user.email == email:
                return "User with this email already exists."
        return None
