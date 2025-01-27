# Codegen Examples

[![Documentation](https://img.shields.io/badge/docs-docs.codegen.com-blue)](https://docs.codegen.com)

This is a collection of examples using [Codegen](https://codegen.com). You can use these examples to learn how to use Codegen and build custom code transformations.

## Setup

We recommend using [`uv`](https://github.com/astral-sh/uv) with Python 3.13 for the best experience.

First, install uv if you haven't already
```bash
brew install uv
```

Create and activate a Python 3.13 virtual environment
```bash
uv venv && source .venv/bin/activate
```

Install the `codegen` package
```bash
uv sync
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

## License

The [Apache 2.0 license](LICENSE).