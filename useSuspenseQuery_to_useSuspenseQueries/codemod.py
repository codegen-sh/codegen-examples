from graph_sitter import Codebase, FunctionCall

codebase = Codebase("./")

# Import statement for useSuspenseQueries
import_str = "import { useQuery, useSuspenseQueries } from '@tanstack/react-query'"

# Iterate through all files in the codebase
for file in codebase.files:
    if "useSuspenseQuery" not in file.source:
        continue
    print(file.filepath)
    # Add the import statement for useQuery and useSuspenseQueries
    file.add_import_from_import_string(import_str)
    print(f"Added import to {file.filepath}")

    # Iterate through all functions in the file
    for function in file.functions:
        # Skip functions that do not call useSuspenseQuery
        if "useSuspenseQuery" not in function.source:
            continue

        results = []  # To store the left-hand side of assignments
        queries = []  # To store the arguments passed to useSuspenseQuery
        old_statements = []  # To keep track of old statements to be replaced

        # Iterate through assignment statements in the function
        for a in function.code_block.assignment_statements:
            # Ensure the right-hand side is a function call
            if not isinstance(a.right, FunctionCall):
                continue

            fcall = a.right
            # Check if the function call is useSuspenseQuery
            if fcall.name != "useSuspenseQuery":
                continue

            # Store the instance of the old useSuspenseQuery call
            old_statements.append(a)
            results.append(a.left.source)  # Collect the variable names
            queries.append(fcall.args[0].value.source)  # Collect the query arguments

        # If useSuspenseQuery was called at least once, convert to useSuspenseQueries
        if old_statements:
            new_query = f"const [{', '.join(results)}] = useSuspenseQueries({{queries: [{', '.join(queries)}]}})"
            print(
                f"Converting useSuspenseQuery to useSuspenseQueries in {function.name}"
            )

            # Print the diff
            print("\nOriginal code:")
            print("\n".join(stmt.source for stmt in old_statements))
            print("\nNew code:")
            print(new_query)
            print("-" * 50)

            # Replace the old statements with the new query
            for a in old_statements:
                a.edit(new_query)

codebase.commit()
