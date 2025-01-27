# Transform useSuspenseQuery to useSuspenseQueries

This codemod demonstrates how to convert multiple `useSuspenseQuery` calls to a single `useSuspenseQueries` calls in your React codebase. This conversion improves code readability and performance by batching multiple queries into a single call, reducing the number of re-renders and network requests.

This primarily leverages two APIs:
- [`codebase.files`](/api-reference/Codebase#files) for finding relevant files
- [`file.add_import_from_import_string(...)`](/codebase-sdk/core/File#add-import-from-import-string) for managing imports

## Finding Files with useSuspenseQuery

To identify files that need updating, we can iterate through the codebase and check for the presence of `useSuspenseQuery`:

```python python
# Iterate through all files in the codebase
for file in codebase.files:
    if "useSuspenseQuery" not in file.source:
        continue
    print(f"Found useSuspenseQuery in: {file.filepath}")
```

## Managing Import Statements

Before making changes, we need to ensure the correct imports are present:

```python python
# Define the required import statement
import_str = "import { useQuery, useSuspenseQueries } from '@tanstack/react-query'"

# Add import to relevant files
for file in codebase.files:
    if "useSuspenseQuery" in file.source:
        file.add_import_from_import_string(import_str)
        print(f"Added import to {file.filepath}")
```

## Converting Query Calls

The main transformation involves collecting multiple `useSuspenseQuery` calls and converting them to a single `useSuspenseQueries` call:

```python python
# Iterate through functions in the file
for function in file.functions:
    if "useSuspenseQuery" not in function.source:
        continue

    results = []  # Store variable names
    queries = []  # Store query configurations
    old_statements = []  # Track statements to replace

    # Find useSuspenseQuery assignments
    for assignment in function.code_block.assignment_statements:
        if not isinstance(assignment.right, FunctionCall):
            continue

        fcall = assignment.right
        if fcall.name != "useSuspenseQuery":
            continue

        old_statements.append(assignment)
        results.append(assignment.left.source)
        queries.append(fcall.args[0].value.source)

    # Convert to useSuspenseQueries if needed
    if old_statements:
        new_query = f"const [{', '.join(results)}] = useSuspenseQueries({{queries: [{', '.join(queries)}]}})"
        
        # Replace old statements with new query
        for assignment in old_statements:
            assignment.edit(new_query)
```

## Example Transformation

Here's an example of how the code transformation works:

Before:
```typescript
const result1 = useSuspenseQuery(queryConfig1)
const result2 = useSuspenseQuery(queryConfig2)
const result3 = useSuspenseQuery(queryConfig3)
```

After:
```typescript
const [result1, result2, result3] = useSuspenseQueries({
  queries: [queryConfig1, queryConfig2, queryConfig3]
})
```

## Running the Transformation

1. Install the codegen package:
    ```bash
    pip install codegen
    ```

2. Run the codemod:
    ```bash
    python3 run.py
    ```

This will:
1. Initialize the codebase from the target repository
2. Find and process files containing `useSuspenseQuery`
3. Apply the transformations
4. Print detailed information to the terminal, including:
   - Files being processed
   - Before/after diffs for each transformation
   - Summary statistics of modified files and functions

The script will output progress and changes to the terminal as it runs, allowing you to review each transformation in real-time.
