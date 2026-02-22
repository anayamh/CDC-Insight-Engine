import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from etl import load_clean_data

# Title of the web application
st.title("Mental Health Indicators Explorer")

# Load transformed mental health dataset
df = load_clean_data()

# -------------------------
# SIDEBAR FILTERS
# -------------------------

# Select a U.S. state
state = st.sidebar.selectbox(
    "Select a state:",
    sorted(df["state"].unique())
)

# Select demographic category (Age, Gender, Race/Ethnicity)
category = st.sidebar.selectbox(
    "Select demographic category:",
    sorted(df["category"].unique())
)

# Select specific subgroup (e.g., Female, 18–24 years, Black)
group = st.sidebar.selectbox(
    "Select subgroup:",
    sorted(df[df["category"] == category]["group"].unique())
)

# Filter dataset for user selections
filtered = df[
    (df["state"] == state) &
    (df["category"] == category) &
    (df["group"] == group)
]

# Subtitle
st.subheader(f"{category} — {group} in {state}")

# If there is data → show chart + table
if filtered.empty:
    st.write("No data available for this selection.")
else:
    # Group by year and average value if duplicates exist
    chart_df = filtered.groupby("year")["value"].mean()

    # -------------------------
    # LINE CHART
    # -------------------------
    fig, ax = plt.subplots()
    ax.plot(chart_df.index, chart_df.values, marker='o', color='pink')
    ax.set_xlabel("year")
    ax.set_ylabel("value")
    ax.set_title("Trend Over Time")
    # Force x-axis to show only integer years

    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    # Display chart in Streamlit
    st.pyplot(fig)

   # -------------------------
    # BAR CHART 1: All groups in same category for latest year
    # -------------------------
    st.subheader(f"{category} — All Groups in {state} (Latest Year)")

    latest_year = filtered["year"].max()
    latest_df = df[
        (df["state"] == state) &
        (df["category"] == category) &
        (df["year"] == latest_year)
    ]

    fig2, ax2 = plt.subplots()
    ax2.bar(latest_df["group"], latest_df["value"], color='#FFEE8C')
    ax2.set_xlabel("Group")
    ax2.set_ylabel("Value")
    ax2.set_title(f"{category} — Groups in {state} ({latest_year})")
    plt.xticks(rotation=45)
    st.pyplot(fig2)

# -------------------------
# SIDEBAR: select two states for comparison
# -------------------------
states_for_comparison = st.sidebar.multiselect(
    "Select up to 2 states to compare for this group:",
    sorted(df["state"].unique()),
    default=[state]  # pre-select the state already chosen
)

if len(states_for_comparison) > 2:
    st.warning("Please select at most 2 states.")
    states_for_comparison = states_for_comparison[:2]

# -------------------------
# BAR CHART 2: Compare selected group in two states
# -------------------------
if states_for_comparison:
    st.subheader(f"{category} — {group} Across Selected States ({latest_year})")

    compare_df = df[
        (df["category"] == category) &
        (df["group"] == group) &
        (df["year"] == latest_year) &
        (df["state"].isin(states_for_comparison))
    ]

    fig3, ax3 = plt.subplots()
    ax3.bar(compare_df["state"], compare_df["value"], color='teal')
    ax3.set_xlabel("State")
    ax3.set_ylabel("Value")
    ax3.set_title(f"{category} — {group} Comparison ({latest_year})")
    st.pyplot(fig3)

    # -------------------------
    # RAW DATA TABLE
    # -------------------------
    st.subheader("Raw Data")
    st.dataframe(filtered)