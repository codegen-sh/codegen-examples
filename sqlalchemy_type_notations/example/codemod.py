from graph_sitter import Codebase, FunctionCall

# Adjust the path to match the root of your project
codebase = Codebase("./")

print("#####[ Add Mapped Types to SQLAlchemy ]#####")

column_type_to_mapped_type = {
    "Integer": "Mapped[int]",
    "Optional[Integer]": "Mapped[int | None]",
    "Boolean": "Mapped[bool]",
    "Optional[Boolean]": "Mapped[bool | None]",
    "DateTime": "Mapped[datetime | None]",
    "Optional[DateTime]": "Mapped[datetime | None]",
    "String": "Mapped[str]",
    "Optional[String]": "Mapped[str | None]",
    "Numeric": "Mapped[Decimal]",
    "Optional[Numeric]": "Mapped[Decimal | None]",
}

# Traverse the codebase classes
for cls in codebase.classes:
    for attribute in cls.attributes:
        # Check if there's an assignment and it is a FunctionCall
        if not attribute.assignment:
            continue

        assignment_value = attribute.assignment.value
        if not isinstance(assignment_value, FunctionCall):
            continue

        if assignment_value.name != "Column":
            continue

        db_column_call = assignment_value

        # Make sure we have at least one argument (the type)
        if len(db_column_call.args) == 0:
            continue

        # Check for nullable=True
        is_nullable = any(
            x.name == "nullable" and x.value == "True" for x in db_column_call.args
        )

        # Extract the first argument for the column type (e.g. Integer, String, etc.)
        first_argument = db_column_call.args[0].source or ""
        first_argument = first_argument.split("(")[0].strip()

        # If the type is namespaced (e.g. sa.Integer), get the last part
        if "." in first_argument:
            first_argument = first_argument.split(".")[-1]

        # If nullable, wrap the type in Optional[...] if we track that in our dict
        if is_nullable:
            first_argument = f"Optional[{first_argument}]"

        # Check if we have a corresponding mapped type
        if first_argument not in column_type_to_mapped_type:
            print(f"Skipping unmapped type: {first_argument}")
            continue

        # Build the new mapped type annotation
        new_type = column_type_to_mapped_type[first_argument]

        # Update the assignment type annotation
        attribute.assignment.set_type_annotation(new_type)

        # Ensure we have the necessary imports in the file
        if not cls.file.has_import("Mapped"):
            cls.file.add_import_from_import_string(
                "from sqlalchemy.orm import Mapped\n"
            )

        if "Optional" in new_type and not cls.file.has_import("Optional"):
            cls.file.add_import_from_import_string("from typing import Optional\n")

        if "Decimal" in new_type and not cls.file.has_import("Decimal"):
            cls.file.add_import_from_import_string("from decimal import Decimal\n")

        if "datetime" in new_type and not cls.file.has_import("datetime"):
            cls.file.add_import_from_import_string("from datetime import datetime\n")

# Finally, save the changes made to the codebase
codebase.commit()
