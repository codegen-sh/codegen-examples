from codegen import Codebase
from codegen.sdk.typescript.file import TSFile, TSImport
from codegen.sdk.enums import ProgrammingLanguage

processed_imports = set()

def run(codebase: Codebase):
    print(len(codebase.files))
    for file in codebase.files:
        
        # Only process files under /src/shared
        if "examples/analize_reexports" not in file.filepath:
            continue
        if '/src/shared' not in file.filepath:
            print("not in shared")
            print(file.filepath)
            continue

        # Gather all reexports that are not external exports
        all_reexports = []
        for export_stmt in file.export_statements:
            for export in export_stmt.exports:
                if export.is_reexport() and not export.is_external_export:
                    all_reexports.append(export)

        # Skip if there are none
        if not all_reexports:
            continue

        for export in all_reexports:
            has_wildcard = False

            # Replace "src/" with "src/shared/"
            resolved_public_file = export.resolved_symbol.filepath.replace("src/", "src/shared/")

            # Get relative path from the "public" file back to the original file
            relative_path = codebase.get_relative_path(
                from_file=resolved_public_file,
                to_file=export.resolved_symbol.filepath
            )

            # Ensure the "public" file exists
            if not codebase.has_file(resolved_public_file):
                target_file = codebase.create_file(resolved_public_file, sync=True)
            else:
                target_file = codebase.get_file(resolved_public_file)

            # If target file already has a wildcard export for this relative path, skip
            if target_file.has_export_statement_for_path(relative_path, "WILDCARD"):
                has_wildcard = True
                continue

            # Compare "public" path to the local file's export.filepath
            if codebase._remove_extension(resolved_public_file) != codebase._remove_extension(export.filepath):

                # A) Wildcard export, e.g. `export * from "..."`
                if export.is_wildcard_export():
                    target_file.insert_before(f'export * from "{relative_path}"')

                # B) Type export, e.g. `export type { Foo, Bar } from "..."`
                elif export.is_type_export():
                    # Does this file already have a type export statement for the path?
                    statement = file.get_export_statement_for_path(relative_path, "TYPE")
                    if statement:
                        # Insert into existing statement
                        if export.is_aliased():
                            statement.insert(0, f"{export.resolved_symbol.name} as {export.name}")
                        else:
                            statement.insert(0, f"{export.name}")
                    else:
                        # Insert a new type export statement
                        if export.is_aliased():
                            target_file.insert_before(
                                f'export type {{ {export.resolved_symbol.name} as {export.name} }} '
                                f'from "{relative_path}"'
                            )
                        else:
                            target_file.insert_before(
                                f'export type {{ {export.name} }} from "{relative_path}"'
                            )

                # C) Normal export, e.g. `export { Foo, Bar } from "..."`
                else:
                    statement = file.get_export_statement_for_path(relative_path, "EXPORT")
                    if statement:
                        # Insert into existing statement
                        if export.is_aliased():
                            statement.insert(0, f"{export.resolved_symbol.name} as {export.name}")
                        else:
                            statement.insert(0, f"{export.name}")
                    else:
                        # Insert a brand-new normal export statement
                        if export.is_aliased():
                            target_file.insert_before(
                                f'export {{ {export.resolved_symbol.name} as {export.name} }} '
                                f'from "{relative_path}"'
                            )
                        else:
                            target_file.insert_before(
                                f'export {{ {export.name} }} from "{relative_path}"'
                            )

            # Now update all import usages that refer to this export
            for usage in export.symbol_usages():
                if isinstance(usage, TSImport) and usage not in processed_imports:
                    processed_imports.add(usage)

                    # Translate the resolved_public_file to the usage file's TS config import path
                    new_path = usage.file.ts_config.translate_import_path(resolved_public_file)

                    if has_wildcard and export.name != export.resolved_symbol.name:
                        name = f"{export.resolved_symbol.name} as {export.name}"
                    else:
                        name = usage.name

                    if usage.is_type_import():
                        new_import = f'import type {{ {name} }} from "{new_path}"'
                    else:
                        new_import = f'import {{ {name} }} from "{new_path}"'

                    usage.file.insert_before(new_import)
                    usage.remove()

            # Remove the old export from the original file
            export.remove()

        # If the file ends up with no exports, remove it entirely
        if not file.export_statements and len(file.symbols) == 0:
            file.remove()


if __name__ == "__main__":
    print("Starting...")
    codebase = Codebase("./", programming_language=ProgrammingLanguage.TYPESCRIPT)
    run(codebase)
    print("Done!")
