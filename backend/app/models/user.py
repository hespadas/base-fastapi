from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import registry, Mapped, mapped_column

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    create_at: Mapped[datetime] = mapped_column(server_default=func.now(), init=False)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"

    def __str__(self):
        return f"User {self.username} with email {self.email}"
