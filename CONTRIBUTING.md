# Contributing to Aegies

Thank you for considering contributing to Aegies! This document outlines the process for contributing to this project.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check the existing issues to see if the problem has already been reported. If not, create a new issue with:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (Python version, OS, etc.)
- Any relevant logs or error messages

### Suggesting Enhancements

Enhancement suggestions are welcome! Please create an issue with:

- A clear description of the proposed feature
- The problem it solves or value it adds
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Write tests** for any new functionality
3. **Ensure all tests pass** (`pytest`)
4. **Follow the code style** (see below)
5. **Update documentation** if needed
6. **Submit a pull request** with a clear description of changes

## Development Setup

```bash
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 (use `black` and `ruff` if available)
- Use type hints for function signatures
- Write docstrings for public functions/classes
- Keep functions small and focused

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=src/dsa_tracker
```

## Commit Messages

Use clear, descriptive commit messages:

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests when applicable

## Code of Conduct

Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md).