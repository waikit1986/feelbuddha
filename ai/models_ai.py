from db.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship
import uuid


class Reading(Base):
    __tablename__ = "readings"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    emotion = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    username = Column(String, ForeignKey("users.username"), unique=True, nullable=False)
    user = relationship("User", back_populates="readings")