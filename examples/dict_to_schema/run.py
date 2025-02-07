import codegen
from codegen.sdk.enums import ProgrammingLanguage
from codegen import Codebase
import sys
import time

def print_progress(current: int, total: int, width: int = 40) -> None:
    """Print a progress bar showing current/total progress."""
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(100 * current / total)
    print(f"\r[{bar}] {percent}% ({current}/{total})", end="", file=sys.stderr)
    if current == total:
        print(file=sys.stderr)


@codegen.function("dict-to-pydantic-schema")
def run(codebase: Codebase):
    """Convert dictionary literals to Pydantic models in a Python codebase.

    This codemod:
    1. Finds all dictionary literals in global variables and class attributes
    2. Creates corresponding Pydantic models
    3. Updates the assignments to use the new models
    4. Adds necessary Pydantic imports
    """
    files_modified = 0
    models_created = 0

    total_files = len(codebase.files)
    print("\n\033[1;36m📁 Scanning files for dictionary literals...\033[0m")
    print(f"Found {total_files} Python files to process")
    
    for i, file in enumerate(codebase.files, 1):
        needs_imports = False
        file_modified = False

        print_progress(i, total_files)
        print(f"\n\033[1;34m🔍 Processing: {file.path}\033[0m")

        for global_var in file.global_vars:
            try:
                if "{" in global_var.source and "}" in global_var.source:
                    dict_content = global_var.value.source.strip("{}")
                    if not dict_content.strip():
                        continue

                    class_name = global_var.name.title() + "Schema"
                    model_def = f"""class {class_name}(BaseModel):
    {dict_content.replace(",", "\n    ")}"""

                    print("\n" + "═" * 60)
                    print(f"\033[1;32m🔄 Converting global variable '{global_var.name}' to schema\033[0m")
                    print("─" * 60)
                    print("\033[1;34m📝 Original code:\033[0m")
                    print(f"    {global_var.name} = {global_var.value.source}")
                    print("\n\033[1;35m✨ Generated schema:\033[0m")
                    print("    " + model_def.replace("\n", "\n    "))
                    print("\n\033[1;32m✅ Updated code:\033[0m")
                    print(f"    {global_var.name} = {class_name}(**{global_var.value.source})")
                    print("═" * 60)

                    global_var.insert_before(model_def + "\n\n")
                    global_var.set_value(f"{class_name}(**{global_var.value.source})")
                    needs_imports = True
                    models_created += 1
                    file_modified = True
            except Exception as e:
                print(f"\n❌ Error processing global variable '{global_var.name}':")
                print(f"   {str(e)}")
                print("   Skipping this variable and continuing...\n")

        for cls in file.classes:
            for attr in cls.attributes:
                try:
                    if "{" in attr.source and "}" in attr.source:
                        dict_content = attr.value.source.strip("{}")
                        if not dict_content.strip():
                            continue

                        class_name = attr.name.title() + "Schema"
                        model_def = f"""class {class_name}(BaseModel):
    {dict_content.replace(",", "\n    ")}"""

                        print("\n" + "═" * 60)
                        print(f"\033[1;32m🔄 Converting class attribute '{cls.name}.{attr.name}' to schema\033[0m")
                        print("─" * 60)
                        print("\033[1;34m📝 Original code:\033[0m")
                        print(f"    class {cls.name}:")
                        print(f"        {attr.name} = {attr.value.source}")
                        print("\n\033[1;35m✨ Generated schema:\033[0m")
                        print("    " + model_def.replace("\n", "\n    "))
                        print("\n\033[1;32m✅ Updated code:\033[0m")
                        print(f"    class {cls.name}:")
                        print(f"        {attr.name} = {class_name}(**{attr.value.source})")
                        print("═" * 60)

                        cls.insert_before(model_def + "\n\n")
                        attr.set_value(f"{class_name}(**{attr.value.source})")
                        needs_imports = True
                        models_created += 1
                        file_modified = True
                except Exception as e:
                    print(f"\n❌ Error processing attribute '{attr.name}' in class '{cls.name}':")
                    print(f"   {str(e)}")
                    print("   Skipping this attribute and continuing...\n")

        if needs_imports:
            print(f"   ➕ Adding Pydantic imports to {file.path}")
            file.add_import_from_import_string("from pydantic import BaseModel")

        if file_modified:
            print(f"   ✅ Successfully modified {file.path}")
            files_modified += 1

    print("\n" + "═" * 60)
    print("\033[1;35m📊 Summary of Changes\033[0m")
    print("═" * 60)
    print(f"\033[1;32m✨ Files modified: {files_modified}\033[0m")
    print(f"\033[1;32m🔄 Schemas created: {models_created}\033[0m")
    print("═" * 60)

if __name__ == "__main__":
    print("\n\033[1;36m🔍 Initializing codebase...\033[0m")
    print("Cloning repository, this may take a moment...")
    codebase = Codebase.from_repo("fastapi/fastapi", programming_language=ProgrammingLanguage.PYTHON)
    
    print("\n\033[1;35m🚀 Running dict-to-pydantic-schema codemod\033[0m")
    print("\n\033[1;34mℹ️  This codemod will:\033[0m")
    print("   1. Find dictionary literals in your code")
    print("   2. Convert them to Pydantic models")
    print("   3. Update assignments to use the new models")
    print("   4. Add required imports\n")
    run(codebase)
