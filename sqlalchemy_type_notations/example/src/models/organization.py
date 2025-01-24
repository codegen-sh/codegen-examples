from sqlalchemy.orm import Mapped

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String(200))
    xero_organization_id: Mapped[str] = Column(String(50), unique=True)
    stripe_customer_id: Mapped[str] = Column(String(100))
    created_at: Mapped[datetime | None] = Column(DateTime)
    updated_at: Mapped[datetime | None] = Column(DateTime)

    # Relationships
    users = relationship("User", back_populates="organization")
    transactions = relationship("Transaction", back_populates="organization")
