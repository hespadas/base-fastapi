from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import mapper_registry as registry
from datetime import datetime

@registry.mapped_as_dataclass
class BlacklistedToken:
    __tablename__ = "blacklisted_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    token: Mapped[str] = mapped_column(unique=True)
    blacklisted_at: Mapped[datetime] = mapped_column(default=datetime.now())