from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import declarative_mixin, Mapped, mapped_column


@declarative_mixin
class Timestamp:
    created_at: Mapped[datetime] = mapped_column("created_at", DateTime(), default=datetime.utcnow, nullable=False)
    updated_at:Mapped[datetime] = mapped_column("updated_at", DateTime(), default=datetime.utcnow, nullable=False)
