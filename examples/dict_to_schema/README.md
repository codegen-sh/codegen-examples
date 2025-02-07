# Dict to Schema

This example demonstrates how to automatically convert Python dictionary literals into Pydantic models. The codemod makes this process simple by handling all the tedious manual updates automatically.

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
   - Inserts new Pydantic models in appropriate locations
   - Updates dictionary assignments to use the new models
   - Automatically adds required Pydantic imports

## Example Transformations

### Global Variables
```python
# Before
app_config = {"host": "localhost", "port": 8080}

# After
class AppConfigSchema(BaseModel):
    host: str = "localhost"
    port: int = 8080

app_config = AppConfigSchema(**{"host": "localhost", "port": 8080})
```

### Class Attributes
```python
# Before
class Service:
    defaults = {"timeout": 30, "retries": 3}

# After
class DefaultsSchema(BaseModel):
    timeout: int = 30
    retries: int = 3

class Service:
    defaults = DefaultsSchema(**{"timeout": 30, "retries": 3})
```

## Running the Conversion

```bash
# Initialize Codegen in your project
codegen init

# Run the codemod
codegen run dict_to_schema
```

## Learn More

- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Codegen Documentation](https://docs.codegen.com)
