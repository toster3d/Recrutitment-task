# Recruitment Task - Virtual Column

Implementation of a function that adds virtual columns to pandas DataFrames based on mathematical rules.

## Task Description

The `add_virtual_column` function takes a DataFrame, a mathematical rule, and a new column name, returning a DataFrame with the computed column based on the rule.

### Functional Requirements

- Support for mathematical operations: `+`, `-`, `*`
- Column name validation (snake_case with underscore)
- Rule correctness validation
- Whitespace handling in rules
- Empty DataFrame on validation errors
- Type hints for type safety
- Comprehensive edge case handling

## Environment Setup

### System Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) - modern Python package manager

### Installing uv (if not already installed)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Installation

```bash
# Install Python 3.13 and all dependencies
uv sync --all-extras

# Activate environment (optional)
source .venv/bin/activate
```

## 🧪 Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run a specific test
uv run pytest -k test_sum_of_two_columns
```

## Quality Assurance

### Linting and Formatting (Ruff)

```bash
# Check code for errors
uv run ruff check .

# Auto-format code
uv run ruff format .

# Auto-fix issues where possible
uv run ruff check --fix .
```

### Type Checking (mypy)

```bash
# Verify type hints correctness
uv run mypy solution.py
```

### Run Everything

```bash
# Format + lint + type check + tests
uv run ruff format . && uv run ruff check . && uv run mypy solution.py && uv run pytest
```

## Project Structure

```
.
├── pyproject.toml              # Project configuration and dependencies
├── .python-version             # Python version (3.13)
├── .gitignore                  # Git ignore rules
├── README.md                   # This file
├── solution.py                 # Solution implementation
├── test_virtual_column 1.py    # Unit tests
└── task 1.pdf                  # Task description
```

## Technology Stack

- **Python 3.13** - Latest stable Python release
- **pandas 2.3+** - Data manipulation library
- **pytest 8.4+** - Testing framework
- **ruff 0.14+** - Ultra-fast linter and formatter
- **mypy 1.18+** - Static type checker
- **uv** - Modern Python package manager

## Implementation Highlights

### Type Safety

- Strict type hints throughout the codebase
- Type aliases for improved readability
- Full mypy compliance with strict mode

### Performance Considerations

- Character validation before column lookup (O(n) vs O(m) optimization)
- Efficient edge case handling
- Minimal DataFrame copying

### Code Quality

- Comprehensive validation (multi-layer defense)
- Clear, human-readable comments
- Professional code organization
- Complete docstrings with examples

### Edge Cases Handled

- Double operators: `"a++b"`, `"a + +b"` → Rejected
- Operators at boundaries: `"+b"`, `"a+"` → Rejected
- Empty operators: `"+"` → Rejected
- Multiple columns: `"a+b+c"` → Rejected
- Invalid characters: `"a&b"` → Rejected
- Non-existent columns → Rejected
- Whitespace handling → Properly normalized

## Notes for Reviewers

This project demonstrates:

- Modern Python standards (3.13, pyproject.toml, PEP 518)
- Type safety with comprehensive type hints
- Modern tooling (uv, ruff, mypy)
- Complete test coverage
- Clean project structure
- Professional documentation
- Performance awareness and optimization rationale
- Data Engineering best practices awareness
