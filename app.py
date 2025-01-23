import sys

try:
    import matplotlib.pyplot as plt
    print("Matplotlib imported successfully!")
except ImportError as e:
    print("Error importing matplotlib:", e)
    sys.exit(1)  # Exit the program if matplotlib is not available

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page title and layout
st.set_page_config(page_title=" CSV Visualization Tool", layout="wide")

# Add a title and description to the app
st.title(" CSV Visualization Tool")
st.write("Upload your CSV file to generate visualizations.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file:
    # Load the CSV data into a DataFrame
    data = pd.read_csv(uploaded_file)

    # Display a preview of the data
    st.write("### Data Preview")
    st.dataframe(data)

    # Select numeric columns for visualization
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_columns) > 0:
        st.write("### Visualization Options")
        # Dropdowns for chart type and column selection
        chart_type = st.selectbox("Choose a chart type", ["Bar Chart", "Line Chart", "Pie Chart"])
        column = st.selectbox("Select a column to visualize", numeric_columns)

        # Generate visualizations based on user selection
        if chart_type == "Bar Chart":
            st.bar_chart(data[column])

        elif chart_type == "Line Chart":
            st.line_chart(data[column])

        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            data[column].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
            st.pyplot(fig)

    else:
        st.warning("The uploaded CSV file does not contain numeric columns for visualization.")
else:
    st.info("Please upload a CSV file to start.")
