from db.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
import uuid

from db.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
import uuid


class Reading(Base):
    __tablename__ = "readings"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    card = Column(String, nullable=False)
    situation = Column(String, nullable=False)
    emotion = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    total_tokens = Column(Integer, nullable=False)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    username = Column(
        String,
        ForeignKey("users.username"),
        nullable=False
    )

    user = relationship("User", back_populates="readings", foreign_keys=[user_id])

    