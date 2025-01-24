## FreezeGun to TimeMachine Migration Guide

Use the codemod to convert FreezeGun imports to TimeMachine imports.

```python
# From:
with freeze_time("2023-01-01"):
    ...

# To:
with travel("2023-01-01", tick=False):
    ...
```

## How to Migrate

### Understanding run.py

The migration script (`run.py`) is structured into several key components:

1. **Initialization**
   ```python
   codebase = Codebase.from_repo("getmoto/moto", commit="786a8ada7ed0c7f9d8b04d49f24596865e4b7901")
   ```
   This initializes the codebase to be processed. You can replace the repository
   and commit with your own codebase.

2. **File Processing**
   ```python
   for file in codebase.files:
       if "tests" not in file.filepath:
           continue
   ```
   The script iterates through all files, focusing only on test files since
   FreezeGun is primarily used in tests.

3. **Import Updates**
   ```python
   for imp in file.imports:
       if imp.symbol_name and 'freezegun' in imp.source:
           if imp.name == 'freeze_time':
               imp.edit('from time_machine import travel')
           else:
               imp.set_import_module('time_machine')
   ```
   This section:
   - Identifies FreezeGun imports
   - Converts `freeze_time` to `travel`
   - Updates any other FreezeGun imports to use TimeMachine

4. **Function Call Updates**
   ```python
   for fcall in file.function_calls:
       if 'freeze_time' not in fcall.source:
           continue
   ```
   The script finds all `freeze_time` function calls for conversion.

5. **Parameter Handling**
   ```python
   if not fcall.get_arg_by_parameter_name('tick'):
       # Add tick parameter logic
   ```
   This ensures the `tick=False` parameter is added to maintain FreezeGun's
   default behavior.

6. **Source Transformation**
   ```python
   new_source = fcall.source
   # Replace freeze_time with travel
   if '.' in new_source:
       new_source = new_source.replace('freeze_time', 'travel')
   else:
       new_source = 'travel' + new_source[len('freeze_time'):]
   ```
   This handles the actual transformation of the code, replacing FreezeGun
   syntax with TimeMachine syntax.

---

## Common Issues and Solutions

### Different Default Behaviors

FreezeGun and TimeMachine have different default behaviors regarding time
progression:

- FreezeGun defaults to not moving time forward
- TimeMachine defaults to moving time forward

Our migration adds `tick=False` to maintain FreezeGun's behavior. If you want
time to progress naturally, you can remove this parameter or set it to `True`.

### Timezone Handling

TimeMachine has more explicit timezone handling. If you encounter
timezone-related issues:

1. Ensure your datetime strings include timezone information when needed
2. Use `datetime.timezone.utc` for UTC times
3. Consider using `zoneinfo` for other timezones

---

## Need Help?

If you encounter issues or have specific edge cases not addressed by the
codemods, reach out to the Codegen support team or visit the
[Codegen Documentation](https://www.codegen.sh/docs) for detailed guidance.

Start your TimeMachine migration today and enjoy the benefits of a more modern
time mocking library!
