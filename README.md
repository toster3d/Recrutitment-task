# Virtual Column Implementation

Function for adding computed columns to pandas DataFrames based on mathematical operations.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

## Setup

```bash
# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Run all quality checks
uv run ruff format . && uv run ruff check . && uv run mypy solution.py --strict && uv run pytest
```

## Implementation

The `add_virtual_column` function performs binary operations (+, -, *) on two DataFrame columns and returns a new DataFrame with the computed result.

### Key Features

**Validation**
- Column names must use snake_case (contain underscore)
- DataFrame columns cannot contain operators (+, -, *) to prevent parsing ambiguity
- Rules must contain exactly one operator
- Both source columns must exist in DataFrame

**Design Decisions**
- DRY principle: Helper function eliminates code duplication
- Performance: Set intersection (O(n*k)) instead of nested loops (O(n*m*k))
- Fail-fast: Character validation before column lookup
- Type safety: Full mypy --strict compliance

**Edge Cases Handled**
- Multiple operators: `a + b - c` → rejected
- Operator in column name: `col-one` → rejected
- Double operators: `a++b` → rejected
- Empty parts: `a+`, `+b` → rejected
- Invalid characters: `a&b` → rejected

## Project Structure

```
.
├── pyproject.toml              # Dependencies and tool configuration
├── solution.py                 # Implementation with type hints
├── test_virtual_column 1.py    # Unit tests
└── README.md                   # Documentation
```

## Technology

Python 3.13, pandas 2.3+, pytest 8.4+, ruff 0.14+, mypy 1.18+, uv
