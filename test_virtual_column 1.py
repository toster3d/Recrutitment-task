import pandas as pd

from solution import add_virtual_column


def test_sum_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(df, "label_one+label_two", "label_three")
    assert df_result.equals(df_expected), (
        f"The function should sum the columns: label_one and label_two.\n\n"
        f"Result:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    )


def test_multiplication_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame(
        [[1, 1, 1]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(df, "label_one * label_two", "label_three")
    assert df_result.equals(df_expected), (
        f"The function should multiply the columns: label_one and label_two.\n\n"
        f"Result:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    )


def test_subtraction_of_two_columns():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame(
        [[1, 1, 0]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(df, "label_one - label_two", "label_three")
    assert df_result.equals(df_expected), (
        f"The function should subtract the columns: label_one and label_two.\n\n"
        f"Result:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    )


def test_empty_result_when_invalid_labels():
    df = pd.DataFrame([[1, 2]] * 3, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label_one + label_two", "label3")
    assert df_result.empty, (
        f'Should return an empty df when the "new_column" is invalid.\n\n'
        f"Result:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    )


def test_empty_result_when_invalid_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_result = add_virtual_column(df, "label&one + label_two", "label_three")
    assert df_result.empty, (
        f"Should return an empty df when the role have invalid character: '&'.\n\n"
        f"Result:\n\n{df_result}\n\nExpected:\n\nEmpty df"
    )
    df_result = add_virtual_column(df, "label_five + label_two", "label_three")
    assert df_result.empty, (
        f"Should return an empty df when the role have a column which isn't "
        f"in the df: 'label_five'.\n\nResult:\n\n{df_result}\n\n"
        f"Expected:\n\nEmpty df"
    )


def test_when_extra_spaces_in_rules():
    df = pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(df, "label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), (
        f"Should work when the role have spaces between the operation and "
        f"the column.\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    )
    df_result = add_virtual_column(df, "  label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), (
        f"Should work when the role have extra spaces in the start/end.\n\n"
        f"Result:\n\n{df_result}\n\nExpected:\n\n{df_expected}"
    )
