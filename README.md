# Codegen Examples

[![Documentation](https://img.shields.io/badge/docs-docs.codegen.com-blue)](https://docs.codegen.com)

A collection of example transformations using [Codegen](https://github.com/codegen-sh/graph-sitter).

## Setup

We recommend using [`uv`](https://github.com/astral-sh/uv) with Python 3.13 for the best experience.

```bash
# Install uv if you haven't already
brew install uv

# Create and activate a Python 3.13 virtual environment
uv venv --python 3.13.0 && source .venv/bin/activate

# Install Codegen
uv pip install codegen

# Optional: Install Jupyter for interactive exploration
uv pip install jupyterlab && jupyter lab
```

## Examples

Each directory contains a self-contained example with:
- A README explaining the transformation
- Sample code to transform
- The Codegen script that performs the transformation

## Learn More

- [Documentation](https://docs.codegen.com)
- [Getting Started Guide](https://docs.codegen.com/introduction/getting-started)
- [Tutorials](https://docs.codegen.com/tutorials/at-a-glance)
- [API Reference](https://docs.codegen.com/api-reference)

## Contributing

Have a useful example to share? We'd love to include it! Please see our [Contributing Guide](CONTRIBUTING.md) for instructions.
