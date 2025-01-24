from sqlalchemy.orm import Mapped

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True)
    email: Mapped[str] = Column(String(255), unique=True)
    username: Mapped[str] = Column(String(100))
    is_active: Mapped[bool] = Column(Boolean, default=True)
    organization_id: Mapped[int] = Column(Integer, ForeignKey("organizations.id"))

    # Relationships
    organization = relationship("Organization", back_populates="users")
    transactions = relationship("Transaction", back_populates="user")
