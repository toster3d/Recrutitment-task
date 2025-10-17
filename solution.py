from typing import Final

import pandas as pd

# Type aliases for clarity
DataFrame = pd.DataFrame

# Constants for validation
ALLOWED_CHARS: Final[set[str]] = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ +-*"
)
OPERATORS: Final[tuple[str, ...]] = ("+", "-", "*")


def add_virtual_column(
    df: DataFrame,
    rule: str,
    new_column: str,
) -> DataFrame:
    """Add a virtual column to a DataFrame based on a mathematical rule.

    This function validates column names and rules, then performs a mathematical
    operation on two columns and returns a DataFrame with the new computed column.

    Args:
        df: Input DataFrame to which the new column will be added.
        rule: Mathematical rule defining the computation for the new column.
              Supported operations: addition (+), subtraction (-), multiplication (*).
              Example: "label_one + label_two" or "col1 * col2".
        new_column: Name of the new column to add. Must follow snake_case convention
                    with at least one underscore.

    Returns:
        DataFrame with the added column, or an empty DataFrame if validation fails
        (invalid rule, invalid column name, or non-existent column in the rule).

    Examples:
        >>> df = pd.DataFrame({"a_col": [1, 2], "b_col": [3, 4]})
        >>> result = add_virtual_column(df, "a_col + b_col", "sum_col")
        >>> result
           a_col  b_col  sum_col
        0      1      3        4
        1      2      4        6
    """
    # Step 1: Validate new column name (must follow snake_case)
    # Note: In production data engineering environments, it's recommended to also
    # reject names starting/ending with underscores (_userid, userid_) due to:
    # - Conflicts with Python's private variable conventions
    # - SQL quotation requirements
    # - Limitations in BI tools (Tableau, Power BI, etc.)
    if not new_column or "_" not in new_column:
        return DataFrame()

    for char in new_column:
        if not (char.isalnum() or char == "_"):
            return DataFrame()

    # Step 2: Strip leading and trailing whitespace from the rule
    rule = rule.strip()

    # Step 3: Validate characters in the rule (before splitting)
    #
    # Why validate characters before checking column existence?
    # - Real-world DataFrames often have hundreds or thousands of columns
    # - Character validation: O(n) where n = rule length (~20 chars)
    # - Column existence check: O(m) where m = number of columns (could be 1000+)
    # - For typical cases: 20 operations << 1000 operations
    #
    # Edge case consideration:
    # This task uses a DataFrame with only 2 columns, so checking columns first
    # might be faster for long rules with errors at the end. However, we optimize
    # for the common data engineering scenario where DataFrames have dozens or
    # hundreds of columns, while rules remain short.
    #
    # Alternative approaches for specific use cases:
    # - Hybrid validation: if len(df.columns) < 10: skip char validation
    # - Regex validation: faster but requires an additional library
    # - Early exit: check only first N characters for quick failure detection

    for char in rule:
        if char not in ALLOWED_CHARS:
            return DataFrame()

    # Step 4: Handle addition operation
    if "+" in rule:
        separated_parts = rule.split("+")
        # Ensure exactly 2 parts (one column + operator + another column)
        if len(separated_parts) != 2:
            return DataFrame()

        column_one = separated_parts[0].strip()
        column_two = separated_parts[1].strip()

        # Verify that column names are not empty
        if not column_one or not column_two:
            return DataFrame()

        # Check if both columns exist in the DataFrame
        if column_one not in df.columns or column_two not in df.columns:
            return DataFrame()

        # Perform the operation and return result
        result = df.copy()
        result[new_column] = df[column_one] + df[column_two]
        return result

    # Step 5: Handle subtraction operation
    elif "-" in rule:
        separated_parts = rule.split("-")
        if len(separated_parts) != 2:
            return DataFrame()

        column_one = separated_parts[0].strip()
        column_two = separated_parts[1].strip()

        if not column_one or not column_two:
            return DataFrame()

        if column_one not in df.columns or column_two not in df.columns:
            return DataFrame()

        result = df.copy()
        result[new_column] = df[column_one] - df[column_two]
        return result

    # Step 6: Handle multiplication operation
    elif "*" in rule:
        separated_parts = rule.split("*")
        if len(separated_parts) != 2:
            return DataFrame()

        column_one = separated_parts[0].strip()
        column_two = separated_parts[1].strip()

        if not column_one or not column_two:
            return DataFrame()

        if column_one not in df.columns or column_two not in df.columns:
            return DataFrame()

        result = df.copy()
        result[new_column] = df[column_one] * df[column_two]
        return result

    # Step 7: No recognized operator or invalid rule
    else:
        return DataFrame()
