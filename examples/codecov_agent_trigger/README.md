# Codecov Agent Trigger

[![Documentation](https://img.shields.io/badge/docs-docs.codegen.com-blue)](https://docs.codegen.com)

This example demonstrates how to automatically trigger a Codegen agent to fix code coverage issues when a pull request's coverage falls below a specified threshold. The script integrates with GitHub Actions and Codecov to maintain high code quality standards.

## Overview

The codecov agent trigger consists of two main components:

1. **Coverage Report Processor** (`process_coverage_report.py`)
   - Parses Codecov XML reports
   - Evaluates coverage against thresholds
   - Triggers Codegen agent when needed

2. **Agent Prompt Generator** (`generate_codecov_agent_prompt.py`)
   - Creates contextual prompts for the Codegen agent
   - Provides necessary information for test generation
   - Includes setup and test execution instructions

## How It Works

The workflow operates in several steps:

1. **Coverage Analysis**
   ```python
   coverage_data = parse_coverage_xml(xml_file)
   if coverage_data["coverage_percentage"] < threshold:
       # Trigger agent to fix coverage
   ```
   - Parses XML coverage reports
   - Extracts key metrics (line coverage, branch coverage)
   - Compares against defined threshold (77%)

2. **Agent Triggering**
   ```python
   from codegen import Agent

   new_agent = Agent(token=token, org_id=ORG_ID)
   second_task = new_agent.run(generate_codecov_agent_prompt(pr_number, repo))
   ```
   - Creates new Codegen agent instance
   - Generates contextual prompt
   - Initiates automated fix process

3. **GitHub Integration**
   ```yaml
   - name: Codecov Agent Trigger
     env:
       PR_NUMBER: ${{ github.event.number }}
       REPO: ${{ github.repository }}
       TOKEN: ${{ secrets.CODEGEN_AGENT_TOKEN }}
     run: |
       python process_coverage_report.py coverage.xml $PR_NUMBER $REPO $TOKEN
   ```
   - Runs as part of CI/CD pipeline
   - Passes PR context to processor
   - Manages authentication securely

## Setup

1. Install dependencies:
   ```bash
   pip install codegen
   ```

2. Configure GitHub secrets:
   - `CODECOV_TOKEN`: Your Codecov API token
   - `CODEGEN_AGENT_TOKEN`: Your Codegen agent token
        - Get your codegen token [here](https://www.codegen.sh/token)

3. Add to your GitHub Actions workflow:
   ```yaml
   - name: Upload coverage reports to Codecov
     uses: codecov/codecov-action@v4.5.0
     with:
       token: ${{ secrets.CODECOV_TOKEN }}
       file: coverage.xml

   - name: Codecov Agent Trigger
     run: python process_coverage_report.py coverage.xml $PR_NUMBER $REPO $TOKEN
   ```

## Usage

The script is typically run automatically as part of your CI/CD pipeline, but you can also run it manually:

```bash
python process_coverage_report.py <coverage_xml_file> <pr_number> <repo> <token>
```

Arguments:
- `coverage_xml_file`: Path to the coverage XML report
- `pr_number`: GitHub PR number
- `repo`: GitHub repository name
- `token`: Codegen agent token

## Output

When coverage is below threshold:
```
WARNING: Coverage 75.50% is below threshold of 77%
Agent will be notified.
Agent has been notified. URL: https://codegen.com/tasks/123
```

When coverage meets threshold:
```
Coverage is above threshold.
```

## Coverage Metrics

The script tracks several key metrics:
- Line coverage
- Branch coverage
- Overall coverage percentage
- Lines covered vs. total lines
- Branches covered vs. total branches

## Configuration

The default coverage threshold is set to 77%, but you can modify this in `process_coverage_report.py`:

```python
threshold = 77  # Modify this value to change the coverage threshold
```

## Learn More

- [Codecov Documentation](https://docs.codecov.com)
- [Codegen Documentation](https://docs.codegen.com)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## Contributing

Feel free to submit issues and enhancement requests! We welcome contributions to improve the codecov agent trigger functionality. 