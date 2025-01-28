# SQLAlchemy 1.6 to 2.0 Migration Example

This codemod demonstrates how to use Codegen to automatically migrate SQLAlchemy 1.6 code to the new 2.0-style query interface. For a complete walkthrough, check out our [tutorial](https://docs.codegen.com/tutorials/sqlalchemy-1.6-to-2.0).

## How the Migration Script Works

The codemod script handles four key transformations:

1. **Update Base Class and Imports**
   ```python
   # From:
   from sqlalchemy.ext.declarative import declarative_base
   Base = declarative_base()
   
   # To:
   from sqlalchemy.orm import DeclarativeBase
   class Base(DeclarativeBase):
       pass
   ```
   Updates the Base class to use the new DeclarativeBase style.

2. **Modernize ORM Relationships**
   ```python
   # From:
   class User(Base):
       addresses = relationship("Address", backref="user")
   
   # To:
   class User(Base):
       addresses = relationship("Address", back_populates="user")
   ```
   Relationships are modernized to use explicit back_populates instead of backref. If no back reference is specified, it defaults to None.

3. **Update Query Method Names**
   ```python
   # From:
   db.session.query(User).filter(User.name == 'john').all()
   db.session.query(User).first()
   
   # To:
   db.session.select(User).where(User.name == 'john').scalars().all()
   db.session.select(User).scalar_one_or_none()
   ```
   Updates query method names to their 2.0 equivalents: `query` → `select`, `filter` → `where`, `all` → `scalars().all`, and `first` → `scalar_one_or_none`.

4. **Update Configurations**
   ```python
   # From:
   create_engine(url)
   sessionmaker(bind=engine)
   relationship("Address")
   
   # To:
   create_engine(url, future=True, pool_pre_ping=True)
   sessionmaker(bind=engine, future=True)
   relationship("Address", lazy="select")
   ```
   Adds future-compatible configurations and default lazy loading settings. Also updates Pydantic configs from `orm_mode` to `from_attributes`.

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