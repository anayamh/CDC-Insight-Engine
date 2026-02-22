import pandas as pd
import os

# Public CDC dataset URL (Chronic Disease Indicators)
URL = "https://data.cdc.gov/api/views/hksd-2xuw/rows.csv?accessType=DOWNLOAD"


def load_data():
    """
    EXTRACT STEP:
    Loads the raw CDC dataset directly from the API URL.
    """
    print("Loading raw dataset...")
    df = pd.read_csv(URL)
    print(f"Raw dataset loaded: {len(df)} rows, {df.shape[1]} columns.")
    return df


def transform_data(df):
    """
    TRANSFORM STEP:
    - Filters the dataset for mental health indicators only
    - Selects relevant columns
    - Renames columns to simpler and more readable names
    - Converts 'value' to numeric
    - Drops missing values in key fields
    - Reorders columns to match strict test expectations
    - Converts all column names to lowercase
    """

    print("Filtering for mental health indicators...")

    # Keep only rows where the Topic contains 'Mental'
    mh_df = df[df["Topic"].str.contains("Mental", case=False, na=False)]
    print(f"Mental health rows found: {len(mh_df)}")

    # Keep only the columns we need
    keep_cols = [
        "YearStart",
        "LocationDesc",
        "Question",
        "DataValue",
        "StratificationCategory1",
        "Stratification1",
    ]
    mh_df = mh_df[keep_cols].copy()

    # Rename columns to more convenient names
    mh_df = mh_df.rename(columns={
        "YearStart": "Year",
        "LocationDesc": "State",
        "StratificationCategory1": "Category",  # e.g., Age, Gender, Race/Ethnicity
        "Stratification1": "Group",             # e.g., 18–24 years, Female, Black
        "DataValue": "Value"
    })

    # Drop rows with missing Category, Group, or Value
    mh_df = mh_df.dropna(subset=["Category", "Group", "Value"])

    # Convert 'Value' column to numeric (float) (FIX)
    mh_df["Value"] = pd.to_numeric(mh_df["Value"], errors="coerce")

    # Reorder columns to match strict test expectations (FIX)
    mh_df = mh_df[["Year", "State", "Question", "Category", "Group", "Value"]]

    # Convert all column names to lowercase to pass tests (FIX)
    mh_df = mh_df.rename(columns=str.lower)

    return mh_df

def load_clean_data(cache_file="cache/cleaned_mental_health_data.csv"):
    """
    Convenience function:
    Runs load_data() → transform_data() → saves to cache
    """
    df = load_data()
    df_clean = transform_data(df)
    
    # Create cache directory if it doesn't exist
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    
    # Save cleaned data to cache
    df_clean.to_csv(cache_file, index=False)
    print(f"Cleaned data saved to cache: {cache_file}")
    
    return df_clean

if __name__ == "__main__":
    # ETL workflow
    df_clean = load_clean_data()

    print("\nPreview of cleaned mental health dataset:")
    print(df_clean.head())
    print(f"\nTotal cleaned rows: {len(df_clean)}")