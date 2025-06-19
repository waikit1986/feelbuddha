from db.database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
import uuid


class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    wall_id = Column(
        UUID(as_uuid=True),
        ForeignKey("walls.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
    reporting_user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", onupdate="CASCADE"),
        nullable=False,
        index=True
    )

    wall = relationship("Wall")
    user = relationship("User")