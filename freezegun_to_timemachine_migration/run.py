from codegen import Codebase

codebase = Codebase.from_repo(
    "getmoto/moto", commit="786a8ada7ed0c7f9d8b04d49f24596865e4b7901")

print("🚀 Starting FreezeGun to TimeMachine conversion...")

# Process files in suma/tests directory
for file in codebase.files:
    if "tests" not in file.filepath:
        continue

    print(f"📝 Processing: {file.filepath}")

    # Update imports
    for imp in file.imports:
        if imp.symbol_name and 'freezegun' in imp.source:
            if imp.name == 'freeze_time':
                imp.edit('from time_machine import travel')
            else:
                imp.set_import_module('time_machine')

    # Find all function calls in the file
    for fcall in file.function_calls:
        if fcall.name == 'freeze_time':
            # Add tick=False if not present
            if not fcall.get_arg_by_parameter_name('tick'):
                fcall.set_kwarg('tick', 'False')

            # Rename freeze_time to travel
            fcall.rename('travel')
            codebase.commit()

print("✅ FreezeGun to TimeMachine conversion completed successfully!")
