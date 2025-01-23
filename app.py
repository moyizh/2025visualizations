
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the page title and layout
st.set_page_config(page_title="Advanced CSV Visualization Tool", layout="wide")

# Add a title and description
st.title("Advanced CSV Visualization Tool")
st.write("Upload your dataset and explore interactive visualizations!")

# Sidebar for additional options
st.sidebar.title("Settings")
st.sidebar.write("Customize your visualization")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load the file based on extension
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Display the data preview
    st.write("### Data Preview")
    st.dataframe(data)

    # Select numeric columns
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    if len(numeric_columns) > 0:
        # Visualization options
        st.write("### Visualization Options")
        chart_type = st.selectbox("Choose a chart type", ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram"])
        column = st.selectbox("Select a column for visualization", numeric_columns)
        
        # Additional settings for Scatter Plot
        if chart_type == "Scatter Plot":
            second_column = st.selectbox("Select another column for comparison", numeric_columns)

        # Generate the selected visualization
        if chart_type == "Bar Chart":
            st.bar_chart(data[column])

        elif chart_type == "Line Chart":
            st.line_chart(data[column])

        elif chart_type == "Pie Chart":
            fig, ax = plt.subplots()
            data[column].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
            st.pyplot(fig)

        elif chart_type == "Scatter Plot":
            fig, ax = plt.subplots()
            ax.scatter(data[column], data[second_column], alpha=0.7)
            ax.set_xlabel(column)
            ax.set_ylabel(second_column)
            st.pyplot(fig)

        elif chart_type == "Histogram":
            fig, ax = plt.subplots()
            ax.hist(data[column], bins=20, alpha=0.7)
            ax.set_xlabel(column)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

    else:
        st.warning("The dataset does not contain numeric columns for visualization.")

    # Display basic statistics
    st.write("### Data Analysis")
    st.write(data.describe())
else:
    st.info("Please upload a dataset to start.")
