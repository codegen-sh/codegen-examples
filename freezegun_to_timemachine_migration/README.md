# FreezeGun to TimeMachine Migration Example

This example demonstrates how to use Codegen to automatically migrate test code from FreezeGun to TimeMachine for time mocking. The migration script makes this process simple by handling all the tedious manual updates automatically.

## How the Migration Script Works

The script (`run.py`) automates the entire migration process in a few key steps:

1. **Codebase Loading**
   ```python
   codebase = Codebase.from_repo(
       "getmoto/moto", commit="786a8ada7ed0c7f9d8b04d49f24596865e4b7901")
   ```
   - Loads your codebase into Codegen's intelligent code analysis engine
   - Provides a simple SDK for making codebase-wide changes
   - Supports specific commit targeting for version control

2. **Test File Processing**
   ```python
   for file in codebase.files:
       if "tests" not in file.filepath:
           continue
       print(f"📝 Processing: {file.filepath}")
   ```
   - Iterates through all files in the codebase
   - Focuses only on test files where time mocking is used
   - Provides helpful progress feedback during migration

3. **Import Updates**
   ```python
   for imp in file.imports:
       if imp.symbol_name and 'freezegun' in imp.source:
           if imp.name == 'freeze_time':
               imp.edit('from time_machine import travel')
           else:
               imp.set_import_module('time_machine')
   ```
   - Converts FreezeGun imports to TimeMachine equivalents
   - Handles both direct imports (`freeze_time`) and other freezegun imports
   - Uses Codegen's import APIs for precise updates

4. **Function Call Transformation**
   ```python
   for fcall in file.function_calls:
       if fcall.name == 'freeze_time':
           # Add tick=False if not present
           if not fcall.get_arg_by_parameter_name('tick'):
               fcall.set_kwarg('tick', 'False')
           # Rename freeze_time to travel
           fcall.rename('travel')
   ```
   - Identifies freeze_time calls using name matching
   - Adds the required `tick=False` parameter using Codegen's argument APIs
   - Renames the function calls from `freeze_time` to `travel`
   - Commits changes after each transformation

## Why This Makes Migration Easy

1. **Zero Manual Updates**
   - Codegen SDK handles all the file searching and updating
   - No tedious copy-paste work

2. **Consistent Changes**
   - Codegen ensures all transformations follow the same patterns
   - Maintains code style consistency

3. **Safe Transformations**
   - Codegen validates changes before applying them
   - Easy to review and revert if needed

## Common Migration Patterns

### Decorator Usage
```python
# FreezeGun
@freeze_time("2023-01-01")
def test_function():
    pass

# Automatically converted to:
@travel("2023-01-01", tick=False)
def test_function():
    pass
```

### Context Manager Usage
```python
# FreezeGun
with freeze_time("2023-01-01"):
    # test code

# Automatically converted to:
with travel("2023-01-01", tick=False):
    # test code
```

### Moving Time Forward
```python
# FreezeGun
freezer = freeze_time("2023-01-01")
freezer.start()
freezer.move_to("2023-01-02")
freezer.stop()

# Automatically converted to:
traveller = travel("2023-01-01", tick=False)
traveller.start()
traveller.shift(datetime.timedelta(days=1))
traveller.stop()
```

## Key Differences to Note

1. **Tick Parameter**
   - TimeMachine requires explicit tick behavior configuration
   - Script automatically adds `tick=False` to match FreezeGun's default behavior

2. **Time Movement**
   - FreezeGun uses `move_to()` with datetime strings
   - TimeMachine uses `shift()` with timedelta objects

3. **Return Values**
   - FreezeGun's decorator returns the freezer object
   - TimeMachine's decorator returns a traveller object

## Running the Migration

```bash
# Install Codegen
pip install codegen

# Run the migration
python run.py
```

## Learn More

- [TimeMachine Documentation](https://github.com/adamchainz/time-machine)
- [FreezeGun Documentation](https://github.com/spulec/freezegun)
- [Codegen Documentation](https://docs.codegen.com)

## Contributing

Feel free to submit issues and enhancement requests!
