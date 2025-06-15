from db.database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, String, func
from sqlalchemy.orm import relationship
import uuid

from db.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship


class Wall(Base):
    __tablename__ = "walls"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    input_text = Column(String, nullable=False)
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


    