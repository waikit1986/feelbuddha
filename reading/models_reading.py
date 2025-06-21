from db.database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, Integer, func
from sqlalchemy.orm import relationship
import uuid

from db.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship


class Reading(Base):
    __tablename__ = "readings"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    tradition = Column(String, nullable=False)
    input_text = Column(String, nullable=False)
    sutra_name = Column(String, nullable=False)
    sutra_excerpt = Column(String, nullable=False)
    saint = Column(String, nullable=False)
    advice = Column(String, nullable=False)
    practice = Column(String, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        index=True
    )
    username = Column(
        String,
        ForeignKey("users.username", onupdate="CASCADE"),
        nullable=False
    )

    user = relationship("User", foreign_keys=[user_id])


    