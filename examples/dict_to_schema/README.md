# Dict to Schema

This example demonstrates how to automatically convert Python dictionary literals into dataclasses with proper type hints. The codemod makes this process simple by handling all the tedious manual updates automatically.

## How the Conversion Script Works

The script (`run.py`) automates the entire conversion process in a few key steps:

1. **Dictionary Detection**
   - Automatically identifies dictionary literals in your code
   - Processes both global variables and class attributes
   - Skips empty dictionaries to avoid unnecessary conversions

2. **Schema Creation**
   - Generates meaningful model names based on variable names
   - Converts dictionary key-value pairs to class attributes
   - Maintains proper Python indentation

3. **Code Updates**
   - Inserts new dataclass definitions in appropriate locations
   - Updates dictionary assignments to use the new dataclasses
   - Automatically adds required imports for dataclasses and typing

## Example Transformations

### Global Variables
```python
# Before
app_config = {"host": "localhost", "port": 8080}

# After
@dataclass
class AppConfig:
    host: str | None = None
    port: int | None = None

app_config = AppConfig(host="localhost", port=8080)

# List Example
books = [
    {"id": 1, "title": "Book One", "author": "Author A"},
    {"id": 2, "title": "Book Two", "author": "Author B"}
]

# After
@dataclass
class Book:
    id: int | None = None
    title: str | None = None
    author: str | None = None

books = [Book(**item) for item in books]
```

### Class Attributes
```python
# Before
class Service:
    defaults = {"timeout": 30, "retries": 3, "backoff": 1.5}

# After
@dataclass
class Defaults:
    timeout: int | None = None
    retries: int | None = None
    backoff: float | None = None

class Service:
    defaults = Defaults(timeout=30, retries=3, backoff=1.5)
```

## Running the Conversion

```bash
# Initialize Codegen in your project
codegen init

# Run the codemod
codegen run dict_to_schema
```

## Learn More

- [Python Dataclasses Documentation](https://docs.python.org/3/library/dataclasses.html)
- [Codegen Documentation](https://docs.codegen.com)
