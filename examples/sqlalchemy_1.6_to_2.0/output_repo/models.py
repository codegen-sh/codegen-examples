from typing import List, Optional
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    books: Mapped[List["Book"]] = relationship(
        "Book", 
        back_populates="publisher",
        lazy='selectin'
    )

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    publisher_id: Mapped[Optional[int]] = mapped_column(
        Integer, 
        ForeignKey("publishers.id"),
        nullable=True
    )
    publisher: Mapped[Optional["Publisher"]] = relationship(
        "Publisher", 
        back_populates="books"
    )