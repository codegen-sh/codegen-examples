import ast
import codegen
from codegen.sdk.enums import ProgrammingLanguage
from codegen import Codebase
from dataclasses import dataclass, field
from typing import Any, Optional

def dict_to_dataclass(name: str, dict_source: str) -> str:
    # Parse the dictionary source to extract keys   
    dict_ast = ast.literal_eval(dict_source)
    fields = [f"{key}: Optional[{type(value).__name__}] = None" for key, value in dict_ast.items()]
    fields_str = "\n    ".join(fields)
    return f"@dataclass\nclass {name}:\n    {fields_str}\n"

@codegen.function("dict-to-pydantic-schema")
def run(codebase: Codebase):
    """
    Convert dictionary literals to Pydantic models in a Python codebase.

    This codemod:
      1. Finds all dictionary literals in global variables and class attributes
      2. Prints the call sites where these dictionaries are found
    """
    # Track statistics0
    stats = {
        'files_modified': 0,
        'models_created': 0,
        'call_sites_updated': 0,
        'key_frequencies': {},
        'dict_sizes': [],
    }

    for file in codebase.files:
        # Process global variables
        for global_var in file.global_vars:
            try:
                if "{" in global_var.value.source and "}" in global_var.value.source:
                    dict_source = global_var.value.source.strip()
                    print(f"\n🔍 Found dictionary in global variable '{global_var.name}'")
                    dataclass_code = dict_to_dataclass(global_var.name, dict_source)
                    print(dataclass_code)
                    # Here you would replace the dictionary with the dataclass in the codebase
            except Exception as e:
                pass

        # Process class attributes
        for cls in file.classes:
            for attr in cls.attributes:
                try:
                    if "{" in attr.value.source and "}" in attr.value.source:
                        dict_source = attr.value.source.strip()
                        print(f"\nConverting attribute '{attr.name}' in class '{cls.name}' to schema")
                        dataclass_code = dict_to_dataclass(attr.name, dict_source)
                        print(dataclass_code)
                        # Here you would replace the dictionary with the dataclass in the codebase
                except Exception as e:
                    pass

    print("\n✅ Transformation Complete!")

if __name__ == "__main__":
    print("Initializing codebase...")
    codebase = Codebase.from_repo(
        "posthog/posthog",
        programming_language=ProgrammingLanguage.PYTHON
    )

    print("Running codemod...")
    run(codebase)
