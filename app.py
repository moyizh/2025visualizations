import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Streamlit page setup
st.set_page_config(page_title="Advanced Data Visualization Tool", layout="wide")

# Title and description
st.title("Advanced Data Visualization Tool")
st.write("Upload your dataset (CSV or Excel) and explore interactive visualizations!")

# Sidebar for settings
st.sidebar.title("Settings")
st.sidebar.write("Customize your visualizations")

# File uploader
uploaded_file = st.file_uploader("Upload your dataset (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Load the uploaded file
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    # Display a preview of the dataset
    st.write("### Data Preview")
    st.dataframe(data)

    # Select numeric and text columns
    numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
    text_columns = data.select_dtypes(include=['object']).columns

    # Visualization options
    st.write("### Visualization Options")
    chart_type = st.selectbox(
        "Choose a chart type", 
        ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Histogram", "Word Cloud"]
    )

    if chart_type != "Word Cloud":
        column = st.selectbox("Select a column for visualization", numeric_columns)

    # Additional scatter plot settings
    if chart_type == "Scatter Plot" and len(numeric_columns) > 1:
        second_column = st.selectbox("Select another column for comparison", numeric_columns)

    # Customize color palette
    color_palette = st.sidebar.selectbox(
        "Select a color palette", 
        sns.color_palette().as_hex()
    )

    # Generate visualizations
    if chart_type == "Bar Chart":
        st.bar_chart(data[column])

    elif chart_type == "Line Chart":
        st.line_chart(data[column])

    elif chart_type == "Pie Chart":
        fig, ax = plt.subplots()
        data[column].value_counts().plot.pie(autopct="%1.1f%%", colors=color_palette, ax=ax)
        st.pyplot(fig)

    elif chart_type == "Scatter Plot":
        fig, ax = plt.subplots()
        ax.scatter(data[column], data[second_column], c=color_palette[0], alpha=0.7)
        ax.set_xlabel(column)
        ax.set_ylabel(second_column)
        st.pyplot(fig)

    elif chart_type == "Histogram":
        fig, ax = plt.subplots()
        ax.hist(data[column], bins=20, color=color_palette[0], alpha=0.7)
        ax.set_xlabel(column)
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

    elif chart_type == "Word Cloud" and len(text_columns) > 0:
        text_column = st.selectbox("Select a text column for the Word Cloud", text_columns)
        text_data = " ".join(data[text_column].astype(str))
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

    else:
        st.warning("The selected chart type requires specific data types.")
        
    # Display basic statistics
    st.write("### Data Statistics")
    st.write(data.describe())

else:
    st.info("Please upload a dataset to start.")
