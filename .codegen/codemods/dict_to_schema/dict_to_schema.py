import codegen
from codegen import Codebase
from typing import Dict, Any, List, Union, get_type_hints
from dataclasses import dataclass
import sys
import ast


def infer_type(value) -> str:
    """Infer type hint from a value."""
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        return "List[Any]"
    elif isinstance(value, dict):
        return "Dict[str, Any]"
    return "Any"


def print_progress(current: int, total: int, width: int = 40) -> None:
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(100 * current / total)
    print(f"\r[{bar}] {percent}% ({current}/{total})", end="", file=sys.stderr)
    if current == total:
        print(file=sys.stderr)


@codegen.function('dict-to-schema')
def run(codebase: Codebase):
    """Convert dictionary literals to dataclasses with proper type hints."""
    files_modified = 0
    models_created = 0

    # Process all Python files in the codebase
    total_files = len([f for f in codebase.files if str(f.path).endswith('.py')])
    print("\n\033[1;36m📁 Scanning files for dictionary literals...\033[0m")
    print(f"Found {total_files} Python files to process")
    
    def process_dict_assignment(source: str, name: str) -> tuple[str, str]:
        """Process dictionary assignment and return model definition and initialization."""
        dict_str = source.split("=", 1)[1].strip()
        if not dict_str.startswith("{") or not dict_str.endswith("}"):
            return None, None

        dict_items = parse_dict_str(dict_str)
        if not dict_items:
            return None, None

        class_name = name.title()
        fields = []
        for key, value, comment in dict_items:
            type_hint = infer_type_from_value(value)
            field = f"    {key}: {type_hint} | None = None"
            if comment:
                field += f"  # {comment}"
            fields.append(field)

        model_def = f"@dataclass\nclass {class_name}:\n" + "\n".join(fields)
        init_code = f"{name} = {class_name}(**{dict_str})"
        return model_def, init_code

    for i, file in enumerate([f for f in codebase.files if str(f.path).endswith('.py')], 1):
        needs_imports = False
        file_modified = False

        print_progress(i, total_files)
        print(f"\n\033[1;34m🔍 Processing: {file.path}\033[0m")

        for global_var in file.global_vars:
            try:
                def parse_dict_str(dict_str: str) -> list:
                    """Parse dictionary string into list of (key, value, comment) tuples."""
                    items = []
                    lines = dict_str.strip("{}").split("\n")
                    for line in lines:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                            
                        # Split line into key-value and comment
                        parts = line.split("#", 1)
                        kv_part = parts[0].strip().rstrip(",")
                        comment = parts[1].strip() if len(parts) > 1 else None
                        
                        if ":" not in kv_part:
                            continue
                            
                        key, value = kv_part.split(":", 1)
                        key = key.strip().strip('"\'')
                        value = value.strip()
                        items.append((key, value, comment))
                    return items

                def infer_type_from_value(value: str) -> str:
                    """Infer type hint from a string value."""
                    value = value.strip()
                    if value.startswith('"') or value.startswith("'"):
                        return "str"
                    elif value in ("True", "False"):
                        return "bool"
                    elif "." in value and value.replace(".", "").isdigit():
                        return "float"
                    elif value.isdigit():
                        return "int"
                    return "Any"

                if "{" in global_var.source and "}" in global_var.source:
                    model_def, init_code = process_dict_assignment(global_var.source, global_var.name)
                    if not model_def:
                        continue

                    print("\n" + "═" * 60)
                    print(f"\033[1;32m🔄 Converting global variable '{global_var.name}' to schema\033[0m")
                    print("─" * 60)
                    print("\033[1;34m📝 Original code:\033[0m")
                    print(f"    {global_var.source}")
                    print("\n\033[1;35m✨ Generated schema:\033[0m")
                    print("    " + model_def.replace("\n", "\n    "))
                    print("\n\033[1;32m✅ Updated code:\033[0m")
                    print(f"    {init_code}")
                    print("═" * 60)

                    global_var.file.add_symbol_from_source(model_def + "\n")
                    global_var.edit(init_code)
                    needs_imports = True
                    models_created += 1
                    file_modified = True
                elif "[" in global_var.source and "]" in global_var.source and "{" in global_var.source:
                    list_str = global_var.source.split("=", 1)[1].strip()
                    if not list_str.startswith("[") or not list_str.endswith("]"):
                        continue

                    dict_start = list_str.find("{")
                    dict_end = list_str.find("}")
                    if dict_start == -1 or dict_end == -1:
                        continue

                    dict_str = list_str[dict_start:dict_end + 1]
                    model_def, _ = process_dict_assignment(f"temp = {dict_str}", global_var.name.rstrip('s'))
                    if not model_def:
                        continue

                    list_init = f"[{global_var.name.rstrip('s').title()}(**item) for item in {list_str}]"

                    print("\n" + "═" * 60)
                    print(f"\033[1;32m🔄 Converting list items in '{global_var.name}' to schema\033[0m")
                    print("─" * 60)
                    print("\033[1;34m📝 Original code:\033[0m")
                    print(f"    {global_var.source}")
                    print("\n\033[1;35m✨ Generated schema:\033[0m")
                    print("    " + model_def.replace("\n", "\n    "))
                    print("\n\033[1;32m✅ Updated code:\033[0m")
                    print(f"    {global_var.name} = {list_init}")
                    print("═" * 60)

                    global_var.file.add_symbol_from_source(model_def + "\n")
                    global_var.edit(list_init)
                    needs_imports = True
                    models_created += 1
                    file_modified = True
            except Exception as e:
                print(f"\n❌ Error processing global variable '{global_var.name}':")
                print(f"   {str(e)}")
                print("   Skipping this variable and continuing...\n")

        if needs_imports:
            print(f"   ➕ Adding dataclass imports to {file.path}")
            file.add_import_from_import_string("from dataclasses import dataclass")
            file.add_import_from_import_string("from typing import Any, Dict, List, Optional")

        # Process class attributes
        for cls in file.classes:
            for attr in cls.attributes:
                try:
                    if "{" in attr.source and "}" in attr.source:
                        model_def, init_code = process_dict_assignment(attr.source, attr.name)
                        if not model_def:
                            continue

                        cls.insert_before(model_def + "\n")
                        attr.edit(init_code.split("=", 1)[1].strip())
                        needs_imports = True
                        models_created += 1
                        file_modified = True
                except Exception as e:
                    print(f"\n❌ Error processing class attribute '{attr.name}':")
                    print(f"   {str(e)}")
                    print("   Skipping this attribute and continuing...\n")

        if file_modified:
            print(f"   ✅ Successfully modified {file.path}")
            files_modified += 1

    print("\n" + "═" * 60)
    print("\033[1;35m📊 Summary of Changes\033[0m")
    print("═" * 60)
    print(f"\033[1;32m✨ Files modified: {files_modified}\033[0m")
    print(f"\033[1;32m🔄 Schemas created: {models_created}\033[0m")
    print("═" * 60)
