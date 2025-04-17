def generate_codecov_agent_prompt(pr_number, repo_name):
    return f"""
# Overview
Hello Codegen, I just generated a new PR {pr_number} for repo {repo_name} however, it failed the codecove (code coverage) check.
Please view the PR checks, see the codecov report, and **update the PR** to fix the codecov check by adding any missing tests.

Please make sure to run the tests you add locally to ensure they are working.

DO NOT COMMIT TESTS IF THEY ARE FAILING.

# Use these commands to run the tests:

# Install Python Dependencies
```
cd path/to/your/package
uv venv
source .venv/bin/activate
uv pip install .
```


# Run Tests
```
chmod +x ./run_test.sh
run_test.sh
```

Good luck!
"""