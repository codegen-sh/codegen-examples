# FreezeGun to TimeMachine Migration Example

This example demonstrates how to use Codegen to automatically migrate test code
from FreezeGun to TimeMachine for time mocking.

## What This Example Does

The migration script handles three key transformations:

1. **Update Imports**
   ```python
   # From:
   from freezegun import freeze_time

   # To:
   from time_machine import travel
   ```

2. **Convert Decorator Usage**
   ```python
   # From:
   @freeze_time("2023-01-01")
   def test_function():
       pass

   # To:
   @travel("2023-01-01", tick=False)
   def test_function():
       pass
   ```

3. **Add tick Parameter**
   ```python
   # From:
   @freeze_time()

   # To:
   @travel(tick=False)
   ```

## Running the Example

```bash
# Install Codegen
pip install codegen

# Run the migration
python run.py
```

The script will process all Python test files in your codebase and apply the
transformations to migrate from FreezeGun to TimeMachine.

## Understanding the Code

- `run.py` - The migration script
- `guide.md` - Additional notes and explanations

## Learn More

- [TimeMachine Documentation](https://github.com/adamchainz/time-machine)
- [FreezeGun Documentation](https://github.com/spulec/freezegun)
- [Codegen Documentation](https://docs.codegen.com)
