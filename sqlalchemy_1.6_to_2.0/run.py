import codegen
from codegen import Codebase


@codegen.function("sqlalchemy-1.6-to-2.0")
def run(codebase: Codebase):
    """Migrate SQLAlchemy code from 1.6 to 2.0 style.

    Updates:
    1. Base class inheritance and imports
    2. Relationship definitions (backref -> back_populates)
    3. Query syntax to 2.0 style
    4. Configuration and lazy loading defaults
    """
    changes_by_file = {}

    for file in codebase.files:
        print(f"🔍 Processing {file.filepath}")

        changes = []
        for updater in [
            update_base_class,
            update_relationships,
            update_query_syntax,
            update_configurations,
        ]:
            if file_changes := updater(file):
                changes.extend(file_changes)

        if changes:
            changes_by_file[file.filepath] = changes

    # Print summary
    print("\n📝 Changes made:")
    for filepath, changes in changes_by_file.items():
        print(f"\n{filepath}:")
        for change in changes:
            print(f"{change}")


def update_base_class(file):
    """Update Base class inheritance and imports."""
    changes = []

    # Update imports
    if any("Base" in cls.parent_class_names for cls in file.classes):
        file.add_import_from_import_string("from sqlalchemy.orm import DeclarativeBase")
        changes.append(
            "- from sqlalchemy.ext.declarative import declarative_base\n+ from sqlalchemy.orm import DeclarativeBase"
        )

        for imp in file.imports:
            if imp.symbol_name == "declarative_base":
                imp.remove()

    # Update Base classes
    for cls in file.classes:
        if cls.name == "Base":
            cls.set_parent_class("DeclarativeBase")
            changes.append("- class Base(object):\n+ class Base(DeclarativeBase):")
        elif "Base" in cls.parent_class_names and not any(
            c.name == "Base" for c in file.classes
        ):
            cls.insert_before("\nclass Base(DeclarativeBase):\n    pass\n")
            changes.append("+ class Base(DeclarativeBase):\n+     pass")

    return changes if changes else None


def update_relationships(file):
    """Modernize relationship definitions."""
    changes = []

    def process_relationship(symbol):
        for call in symbol.function_calls:
            if call.name != "relationship":
                continue

            arg_names = [arg.name for arg in call.args if arg.name]
            if "backref" in arg_names:
                backref_arg = next(arg for arg in call.args if arg.name == "backref")
                old_value = f'relationship("{call.args[0].value.source}", backref="{backref_arg.value.source}"'
                call.set_kwarg("back_populates", backref_arg.value.source)
                backref_arg.remove()
                new_value = f'relationship("{call.args[0].value.source}", back_populates="{backref_arg.value.source}"'
                changes.append(f"- {old_value}\n+ {new_value}")
            elif "back_populates" not in arg_names:
                old_value = f'relationship("{call.args[0].value.source}"'
                call.set_kwarg("back_populates", "None")
                new_value = (
                    f'relationship("{call.args[0].value.source}", back_populates=None'
                )
                changes.append(f"- {old_value}\n+ {new_value}")

    for item in [
        *file.functions,
        *[m for c in file.classes for m in c.methods],
        *[a for c in file.classes for a in c.attributes],
    ]:
        process_relationship(item)

    return changes if changes else None


def update_query_syntax(file):
    """Update to SQLAlchemy 2.0 query style."""
    changes = []

    query_updates = {
        "query": "select",
        "filter": "where",
        "all": "scalars().all",
        "first": "scalar_one_or_none",
    }

    def process_queries(function):
        for call in function.function_calls:
            if new_name := query_updates.get(call.name):
                old_name = call.name
                call.set_name(new_name)
                changes.append(f"- db.session.{old_name}()\n+ db.session.{new_name}()")

    for item in [*file.functions, *[m for c in file.classes for m in c.methods]]:
        process_queries(item)

    return changes if changes else None


def update_configurations(file):
    """Update engine, session, and relationship configurations."""
    changes = []

    # Update engine and session config
    for call in file.function_calls:
        if call.name == "create_engine" and not any(
            arg.name == "future" for arg in call.args
        ):
            old_call = "create_engine(url)"
            call.set_kwarg("future", "True")
            call.set_kwarg("pool_pre_ping", "True")
            changes.append(
                f"- {old_call}\n+ create_engine(url, future=True, pool_pre_ping=True)"
            )
        elif call.name == "sessionmaker" and not any(
            arg.name == "future" for arg in call.args
        ):
            old_call = "sessionmaker(bind=engine)"
            call.set_kwarg("future", "True")
            changes.append(f"- {old_call}\n+ sessionmaker(bind=engine, future=True)")
        elif call.name == "relationship" and not any(
            arg.name == "lazy" for arg in call.args
        ):
            old_call = f'relationship("{call.args[0].value.source}"'
            call.set_kwarg("lazy", '"select"')
            changes.append(f'- {old_call}\n+ {old_call}, lazy="select")')

    # Update Pydantic configs
    for cls in file.classes:
        if cls.name == "Config":
            for attr in cls.attributes:
                if attr.name == "orm_mode":
                    old_attr = "orm_mode = True"
                    attr.set_name("from_attributes")
                    attr.set_value("True")
                    changes.append(f"- {old_attr}\n+ from_attributes = True")

    return changes if changes else None


if __name__ == "__main__":
    print("\nInitializing codebase...")
    codebase = Codebase("./input_repo")
    run(codebase)
