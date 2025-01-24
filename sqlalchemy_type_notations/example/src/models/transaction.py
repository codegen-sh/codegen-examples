from sqlalchemy.orm import Mapped

from decimal import Decimal

from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from .base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = Column(Integer, primary_key=True)
    amount: Mapped[Decimal] = Column(Numeric(10, 2))
    description: Mapped[str] = Column(String(500))
    reference_id: Mapped[str] = Column(String(100))
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
    organization_id: Mapped[int] = Column(Integer, ForeignKey("organizations.id"))
    created_at: Mapped[datetime | None] = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="transactions")
    organization = relationship("Organization", back_populates="transactions")
