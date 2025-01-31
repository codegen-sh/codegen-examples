import codegen
from codegen import Codebase
from codegen.sdk.core.detached_symbols.function_call import FunctionCall
from codegen.sdk.codebase.config import CodebaseConfig, GSFeatureFlags

codebase = Codebase("./input_repo", config=CodebaseConfig(feature_flags=GSFeatureFlags(disable_graph=True)))

# Values for soft delete models and join methods
soft_delete_models = {
    "User",
    "ProductWorkflow",
    "TransactionCanonical",
    "BillParametersLogEntry",
    "SpendEventCanonical",
    "TrackingCategory",
    "Payee",
    "Card",
    "ApprovalInstance",
    "Merchant",
    "Transaction",
}
join_methods = {"join", "outerjoin", "innerjoin"}

# Loop through all files and function calls
for file in codebase.files:
    for call in file.function_calls:
        # Get the arguments as a list
        call_args = list(call.args)

        # Skip if the function call is not a join method
        if str(call.name) not in join_methods:
            continue

        # Skip if the function call has no arguments
        if len(call_args) == 0:
            continue

        # Get the model name from the first argument
        model_name = str(call_args[0].value)

        # Skip if the model name is not in the soft delete models
        if model_name not in soft_delete_models:
            continue

        # Construct the deleted_at check expression
        print(f"Found join method for model {model_name} in file {file.filepath}")
        deleted_at_check = f"{model_name}.deleted_at.is_(None)"

        # If there is only one argument, add the deleted_at check
        if len(call_args) == 1:
            print(f"Adding deleted_at check to function call {call.source}")
            call_args.append(deleted_at_check)
        elif len(call_args) >= 2:
            # Get the second argument
            second_arg = call_args[1].value

            # Skip if the second argument is already the deleted_at check
            if second_arg.source == deleted_at_check:
                print(f"Skipping {file.filepath} because the deleted_at check is already present")
                continue

            # If the second argument is an and_ call, add the deleted_at check if it's not already present
            if isinstance(second_arg, FunctionCall) and second_arg.name == "and_":
                if deleted_at_check in {str(x) for x in second_arg.args}:
                    print(f"Skipping {file.filepath} because the deleted_at check is already present")
                    continue
                else:
                    print(f"Adding deleted_at check to and_ call in {file.filepath}")
                    second_arg.args.append(deleted_at_check)
            else:
                print(f"Adding deleted_at check to {file.filepath}")
                call_args[1].edit(f"and_({second_arg.source}, {deleted_at_check})")

            # Check if the file imports and_
            if any("and_" in imp.name for imp in file.imports):
                print(f"File {file.filepath} imports and_")
            else:
                print(f"File {file.filepath} does not import and_. Adding import.")
                file.add_import_from_import_string("from sqlalchemy import and_")
