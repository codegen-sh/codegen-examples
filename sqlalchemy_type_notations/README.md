# Enhance SQLAlchemy Type Annotations

This codemod demonstrates how to automatically add type annotations to SQLAlchemy models in your Python codebase. This conversion improves code maintainability and IDE support by adding proper type hints to model attributes and relationships.

This primarily leverages two APIs:
- [`codebase.files`](/api-reference/Codebase#files) for finding relevant files
- [`file.edit(...)`](/api-reference/Codebase#files) for updating model definitions

## What This Example Does

The codemod handles three key transformations:

1. **Convert Column Definitions to Mapped Types**
```python python
# From:
id = Column(Integer, primary_key=True)
name = Column(String)
   
# To:
id: Mapped[int] = mapped_column(primary_key=True)
name: Mapped[str] = mapped_column()
```

2. **Update Relationship Definitions**
```python python
 # From:
addresses = relationship("Address", backref="user")
   
# To:
addresses: Mapped[List["Address"]] = relationship(back_populates="user")
```

3. **Update Relationship Definitions**
```python python
# From:
description = Column(String, nullable=True)
   
# To:
description: Mapped[Optional[str]] = mapped_column(nullable=True)
```

## Example Implementation

For a complete example of the transformation, see:

```python python
from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship, backref
from database import Base

class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    books = relationship("Book", backref="publisher")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String)
    publisher_id = Column(Integer, ForeignKey("publishers.id"))
```

And its transformed version:

```python python
from typing import List, Optional
from sqlalchemy import Column, Integer, String, ForeignKey
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
```

## Running the Transformation

1. Install the codegen package:
    ```bash
    pip install codegen
    ```

2. Run the codemod:
    ```bash
    python3 run.py
    ```

This will:
1. Initialize the codebase from the target repository
2. Find and process files containing `useSuspenseQuery`
3. Apply the transformations
4. Print detailed information to the terminal, including:
   - Files being processed
   - Before/after diffs for each transformation
   - Summary statistics of modified files and functions

The script will output progress and changes to the terminal as it runs, allowing you to review each transformation in real-time.