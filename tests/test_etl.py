import pytest
import pandas as pd
from code.etl import load_data, transform_data, load_clean_data

# ---------------------------------------------------------
# TEST 1: Ensure the full dataset loads without errors
# ---------------------------------------------------------
def test_load_data():
    """
    Test that the raw data loads correctly.
    """
    df = load_data()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    assert "Topic" in df.columns  # Key column must exist


def test_transform_data_columns():
    """
    Test that transform_data() returns the expected cleaned columns.
    """
    df = load_data()
    clean = transform_data(df)

    expected_columns = [
        "year",
        "state",
        "question",
        "category",
        "group",
        "value"
    ]

    assert list(clean.columns) == expected_columns


def test_transform_data_filters_mental():
    """
    Checks that we filtered for mental health topics.
    """
    df = load_data()
    clean = transform_data(df)

    # Ensure that mental health keywords appear in question or category
    assert (
        clean["question"].str.contains("mental", case=False, na=False).any()
        or clean["category"].str.contains("mental", case=False, na=False).any()
    )

# ---------------------------------------------------------
# TEST 4: Values should be numeric and non-negative
# ---------------------------------------------------------
def test_value_valid():
    df_raw = load_data()
    df_clean = transform_data(df_raw)

    assert df_clean["value"].dtype == float
    assert df_clean["value"].min() >= 0


def test_value_is_numeric():
    """
    Ensure the Value column contains numeric data only.
    """
    df = load_clean_data()
    assert pd.api.types.is_numeric_dtype(df["value"])


def test_no_missing_key_fields():
    """
    Ensure no nulls remain in crucial fields after cleaning.
    """
    df = load_clean_data()
    assert df["category"].notna().all()
    assert df["group"].notna().all()
    assert df["value"].notna().all()