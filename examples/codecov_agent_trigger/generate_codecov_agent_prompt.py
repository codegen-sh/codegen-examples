def generate_codecov_agent_prompt(pr_number, repo_name):
    return f"""
# Overview
Hello Codegen, I just generated a new PR {pr_number} for repo {repo_name} however, it failed the codecove (code coverage) check.
Please view the PR checks, see the codecov report, and **update the PR** to fix the codecov check by adding any missing tests.

Please make sure to run the tests you add locally to ensure they are working.

Please do not write tests for the following files:
- codegen-backend/scripts/process_coverage_report.py
- codegen-backend/scripts/generate_codecov_agent_prompt.py

DO NOT COMMIT TESTS IF THEY ARE FAILING.

# Here are some commands you can use to run the tests:

# Install Python Dependencies
```
cd codegen-backend
uv venv
source .venv/bin/activate
uv pip install .
```


# Run Tests
```
chmod +x ./codegen-backend/scripts/codecov_agent_run_test.sh
cd codegen-backend && ENV=develop ./codegen-backend/scripts/codecov_agent_run_test.sh <optional_test_file_path>
```

Good luck!
"""