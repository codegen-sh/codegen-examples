import codegen
from codegen.sdk.enums import ProgrammingLanguage
from codegen import Codebase


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
    print(f"\n📁 Scanning {total_files} files for dictionary literals...")
    
    for i, file in enumerate(codebase.files, 1):
        needs_imports = False
        file_modified = False

        print(f"\n🔍 Checking file {i}/{total_files}: {file.path}")

        for global_var in file.global_vars:
            try:
                if "{" in global_var.source and "}" in global_var.source:
                    dict_content = global_var.value.source.strip("{}")
                    if not dict_content.strip():
                        continue

                    class_name = global_var.name.title() + "Schema"
                    model_def = f"""class {class_name}(BaseModel):
    {dict_content.replace(",", "\n    ")}"""

                    print("\n" + "=" * 60)
                    print(f"🔄 Converting global variable '{global_var.name}' to schema")
                    print("=" * 60)
                    print("📝 Original code:")
                    print(f"    {global_var.name} = {global_var.value.source}")
                    print("\n✨ Generated schema:")
                    print("    " + model_def.replace("\n", "\n    "))
                    print("\n✅ Updated code:")
                    print(f"    {global_var.name} = {class_name}(**{global_var.value.source})")
                    print("=" * 60)

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

                        print("\n" + "=" * 60)
                        print(f"🔄 Converting class attribute '{cls.name}.{attr.name}' to schema")
                        print("=" * 60)
                        print("📝 Original code:")
                        print(f"    class {cls.name}:")
                        print(f"        {attr.name} = {attr.value.source}")
                        print("\n✨ Generated schema:")
                        print("    " + model_def.replace("\n", "\n    "))
                        print("\n✅ Updated code:")
                        print(f"    class {cls.name}:")
                        print(f"        {attr.name} = {class_name}(**{attr.value.source})")
                        print("=" * 60)

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

    print("\n" + "=" * 60)
    print("📊 Summary of Changes")
    print("=" * 60)
    print(f"✨ Files modified: {files_modified}")
    print(f"🔄 Schemas created: {models_created}")
    print("=" * 60)

if __name__ == "__main__":
    print("\n🔍 Initializing codebase...")
    codebase = Codebase.from_repo("fastapi/fastapi", programming_language=ProgrammingLanguage.PYTHON)
    print("\n🚀 Running dict-to-pydantic-schema codemod...")
    print("\nℹ️  This codemod will:")
    print("   1. Find dictionary literals in your code")
    print("   2. Convert them to Pydantic models")
    print("   3. Update assignments to use the new models")
    print("   4. Add required imports\n")
    run(codebase)
