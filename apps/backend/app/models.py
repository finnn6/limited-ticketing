from datetime import datetime
from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    total_quantity: Mapped[int]
    remaining_quantity: Mapped[int]
    per_user_limit: Mapped[int] = mapped_column(default=1)
    open_at: Mapped[datetime]
    close_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())