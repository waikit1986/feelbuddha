from db.database import Base
from sqlalchemy import UUID, Boolean, Column, String, DateTime
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
    apple_sub = Column(String, unique=True, index=True, nullable=True)
    full_name = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    email_verified = Column(Boolean, default=False)
    username = Column(String, unique=True, index=True, nullable=True)
    # password = Column(String, nullable=True)
    
    # Apple Sign-In fields
    
    