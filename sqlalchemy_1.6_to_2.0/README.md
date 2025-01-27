# SQLAlchemy 1.6 to 2.0 Migration Example

This codemod demonstrates how to use Codegen to automatically migrate SQLAlchemy 1.6 code to the new 2.0-style query interface. For a complete walkthrough, check out our [tutorial](https://docs.codegen.com/tutorials/sqlalchemy-1.6-to-2.0).

## How the Migration Script Works

The codemod script handles four key transformations:

1. **Convert Query to Select**
   ```python
   # From:
   session.query(User).filter_by(name='john').all()
   
   # To:
   session.execute(
       select(User).where(User.name == 'john')
   ).scalars().all()
   ```
   This transformation replaces the legacy Query interface with the new Select-based API, providing better type safety and consistency.

2. **Update Session Execution**
   ```python
   # From:
   users = session.query(User).all()
   first_user = session.query(User).first()
   
   # To:
   users = session.execute(select(User)).scalars().all()
   first_user = session.execute(select(User)).scalars().first()
   ```
   Session execution is updated to use the new execute() method, which provides clearer separation between SQL construction and execution.

3. **Modernize ORM Relationships**
   ```python
   # From:
   class User(Base):
       addresses = relationship("Address", backref="user")
   
   # To:
   class User(Base):
       addresses = relationship("Address", back_populates="user", use_list=True)
   class Address(Base):
       user = relationship("User", back_populates="addresses")
   ```
   Relationships are modernized to use explicit back_populates instead of backref, making bidirectional relationships more maintainable and explicit.

4. **Add Type Annotations**
   ```python
   # From:
   class User(Base):
       __tablename__ = "users"
       id = Column(Integer, primary_key=True)
       name = Column(String)
       addresses = relationship("Address")
   
   # To:
   class User(Base):
       __tablename__ = "users"
       id: Mapped[int] = mapped_column(primary_key=True)
       name: Mapped[str] = mapped_column()
       addresses: Mapped[List["Address"]] = relationship()
   ```
   Type annotations are added using SQLAlchemy 2.0's Mapped[] syntax, enabling better IDE support and runtime type checking.

## Running the Example

```bash
# Install Codegen
pip install codegen

# Run the migration
python run.py
```

The script will process all Python files in the `input_repo` directory and apply the transformations in the correct order.

## Learn More

- [Full Tutorial](https://docs.codegen.com/tutorials/sqlalchemy-1.6-to-2.0)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/en/20/)
- [What's New in SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html)
- [Codegen Documentation](https://docs.codegen.com) 