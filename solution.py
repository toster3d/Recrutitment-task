from typing import Final

import pandas as pd

# Type aliases for clarity
DataFrame = pd.DataFrame

# Constants for validation
ALLOWED_CHARS: Final[set[str]] = set(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_ +-*"
)
OPERATORS: Final[tuple[str, ...]] = ("+", "-", "*")

# Characters that are NOT allowed in DataFrame column names to avoid ambiguity
# with operators used in rules. Column names should follow snake_case convention.
FORBIDDEN_IN_COLUMN_NAMES: Final[set[str]] = set(OPERATORS)


def _parse_and_validate_rule(rule: str, operator: str, df: DataFrame) -> tuple[str, str] | None:
    """Parse rule by operator and validate column names.

    This helper function takes a mathematical rule like "col_a + col_b", splits it
    by the operator, and checks that both resulting column names are valid and exist
    in the DataFrame. It's designed to eliminate code duplication since we handle
    three different operators in essentially the same way.

    Args:
        rule: Mathematical rule to parse (e.g., "sales + tax").
        operator: The operator to split by ('+', '-', or '*').
        df: DataFrame to validate column existence against.

    Returns:
        A tuple containing (column_one, column_two) if everything checks out,
        or None if something goes wrong (wrong number of parts, empty names,
        or columns that don't exist in the DataFrame).
    """
    separated_parts = rule.split(operator)

    # We're expecting exactly two parts here - the column name before the operator
    # and the column name after it. If we get more or fewer than two parts, something's
    # wrong with the rule.
    if len(separated_parts) != 2:
        return None

    column_one = separated_parts[0].strip()
    column_two = separated_parts[1].strip()

    # Both column names need to actually contain something after we strip whitespace.
    # An empty string means the rule was something weird like "+ col_b" or "col_a +".
    if not column_one or not column_two:
        return None

    # Finally, let's make sure both columns actually exist in the DataFrame. No point
    # trying to do math on columns that aren't there.
    if column_one not in df.columns or column_two not in df.columns:
        return None

    return (column_one, column_two)


def add_virtual_column(
    df: DataFrame,
    rule: str,
    new_column: str,
) -> DataFrame:
    """Add a virtual column to a DataFrame based on a mathematical rule.

    This function validates column names and rules, then performs a mathematical
    operation on two columns and returns a DataFrame with the new computed column.

    Important: Column names in the DataFrame must NOT contain operators (+, -, *).
    For example, "col-one" or "user+id" are not supported to avoid parsing ambiguity.
    Use snake_case convention (col_one, user_id) for all column names.

    Args:
        df: Input DataFrame to which the new column will be added.
            Column names must use snake_case and not contain +, -, or * characters.
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
    # First, we need to make sure none of the existing column names in the DataFrame
    # contain any mathematical operators. This is crucial because if someone named a
    # column "col-one", and then wrote a rule like "col-one - col-two", we wouldn't
    # know if that's supposed to be subtracting two columns or referencing a column
    # literally named "col-one". By enforcing snake_case naming (like col_one instead
    # of col-one), we avoid this entire category of parsing problems. We're using set
    # intersection here which is more efficient than nested loops.
    for column_name in df.columns:
        if FORBIDDEN_IN_COLUMN_NAMES & set(str(column_name)):
            return DataFrame()

    # Now let's validate the name of the new column we're about to create. We require
    # it to follow snake_case convention, which means it must contain at least one
    # underscore and only use letters, numbers, and underscores. In a production
    # environment, we'd probably also want to reject column names that start or end
    # with underscores (like _userid or userid_) because they can cause headaches with
    # Python's naming conventions, need special quoting in SQL, and sometimes don't
    # play nice with BI tools like Tableau or Power BI.
    if not new_column or "_" not in new_column:
        return DataFrame()

    for char in new_column:
        if not (char.isalnum() or char == "_"):
            return DataFrame()

    # Let's clean up any whitespace from the beginning and end of the rule before
    # we start parsing it.
    rule = rule.strip()
    # Validate that every character in the rule is allowed. We do this before checking
    # column existence for performance reasons: character validation is O(n) where n is
    # the rule length (typically ~20 chars), while column lookup is O(m) where m is the
    # number of DataFrame columns (often hundreds or thousands). This fail-fast approach
    # optimizes for the common case of wide DataFrames with short rules.
    #
    # For DataFrames with very few columns (<10), checking column existence first
    # might be faster, but I prioritize the typical data engineering scenario where
    # DataFrames are wide and rules are concise.
    for char in rule:
        if char not in ALLOWED_CHARS:
            return DataFrame()

    # Here's an important check: we need to make sure the rule contains exactly one
    # operator. If someone writes something like "a + b - c", we'd have no way to
    # know which operation should happen first, or if they meant something else entirely.
    # This check is technically redundant with len(separated_parts) != 2, but it provides
    # fail-fast validation and clearer intent:we only support binary operations (exactly
    # one operator between two columns).
    operator_count = sum(1 for op in OPERATORS if op in rule)
    if operator_count != 1:
        return DataFrame()

    # Now we handle addition. We use our helper function to parse the rule and validate
    # that both column names are legitimate. If anything looks wrong, we bail out early.
    # Otherwise, we create a copy of the DataFrame and add the new computed column.
    if "+" in rule:
        columns = _parse_and_validate_rule(rule, "+", df)
        if columns is None:
            return DataFrame()

        column_one, column_two = columns
        result = df.copy()
        result[new_column] = df[column_one] + df[column_two]
        return result

    # Subtraction works exactly the same way as addition, just with a different operator.
    # The helper function handles all the parsing and validation for us.
    elif "-" in rule:
        columns = _parse_and_validate_rule(rule, "-", df)
        if columns is None:
            return DataFrame()

        column_one, column_two = columns
        result = df.copy()
        result[new_column] = df[column_one] - df[column_two]
        return result

    # And multiplication follows the same pattern. Notice how much cleaner this is
    # compared to repeating all the validation logic three times.
    elif "*" in rule:
        columns = _parse_and_validate_rule(rule, "*", df)
        if columns is None:
            return DataFrame()

        column_one, column_two = columns
        result = df.copy()
        result[new_column] = df[column_one] * df[column_two]
        return result

    # If we've gotten this far, it means the rule didn't contain any of our supported
    # operators, which means it's not valid. This shouldn't actually be reachable given
    # our earlier check for operator_count, but it's here as a safety net.
    else:
        return DataFrame()
