from db.database import Base
from sqlalchemy import UUID, Column, String, DateTime
from sqlalchemy.orm import relationship
import uuid

from sqlalchemy import Column, String, UUID
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    last_login = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    deleted_request = Column(DateTime(timezone=True), nullable=True)
    
    readings = relationship("Reading", back_populates="user", foreign_keys="[Reading.user_id]")