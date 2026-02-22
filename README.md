This project is a Python application that extracts, transforms, and visualizes mental health indicators from the CDC Chronic Disease Indicators dataset. It allows users to:

-Explore trends over time for selected demographic groups in a specific state.

-Compare all groups in a category within a state for the latest year.

-Compare a specific demographic group across two selected states for the latest year.

-View a table of the filtered raw data.

-Interact with visualizations through an intuitive Streamlit interface.



HOW YOU RUN MY PROJECT:

BEFORE YOU BEGIN: Make sure you have Python installed and create a virtual environment:

python3 -m venv .venv source .venv/bin/activate # Mac

OR

.venv\Scripts\activate # Windows

THEN

pip install -r requirements.txt

THEN BEGIN:

Run the ETL pipeline to download and clean the CDC dataset python code/etl.py

YOU SHOULD SEE THIS IN YOUR TERMINAL: 

''' Loading raw dataset... Raw dataset loaded: 309215 rows, 34 columns. Filtering for mental health indicators... Mental health rows found: 16976

Preview of cleaned mental health dataset: year state ... group value 70 2019 Alabama ... Age 18-44 21.0 87 2019 Arkansas ... Age 18-44 27.8 124 2019 Guam ... Multiracial, non-Hispanic 13.0 133 2019 Idaho ... Age 45-64 22.3 134 2019 Idaho ... Male 11.5

[5 rows x 6 columns]

Total cleaned rows: 11732 ''' 

A cleaned file should be saved to cache named cleaned_mental_health_data.csv

Run the Streamlit app streamlit run code/streamlit_app.py or streamlit run code/streamlit_app.py

The app will appear in your browser

Inside the app, you can: Select a state to see mental–health indicator trends

Choose a demographic group (age, gender, race, or grade)

Use visualizations such as: Line plot over time, Comparison between two states, Distribution of values

Make sure you run the tests to make sure everything runs smoothly. You can go into the test column or into the code to run these tests.

OTHER THINGS YOU SHOULD KNOW:

-The ETL process is handled in etl.py:

-load_data() fetches the raw CDC dataset.

-transform_data() filters for mental health indicators, cleans the data, renames columns, and converts values to numeric.

-load_clean_data() caches the cleaned CSV for faster loading.

-Column names in the cleaned data are all lowercase: year, state, question, category, group, value.

-If you want to refresh the cache (re-run the ETL), delete cache/cleaned_mental_health_data.csv and restart the app.

-Visualizations use Matplotlib, and all charts are generated dynamically based on the selected filters.

-Recommended Python version: 3.11+
