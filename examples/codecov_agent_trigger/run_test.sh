#! /bin/bash

# Set environment variables
export ENV_VAR_1=1
export ENV_VAR_2=2
export ENV_VAR_3=3

# Run the tests
cd path/to/your/package
pytest -v --cov=./path/to/your/tests --cov-report=xml:coverage.xml "$@"
