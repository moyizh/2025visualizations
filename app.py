import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import docx

# 配置 Streamlit 页面
st.set_page_config(page_title="Visualization Tool", layout="wide")

# 页面标题
st.title("Visualization Tool")
st.write("Upload your CSV, Excel, or Word file to generate visualizations.")

# 文件上传
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx", "xls", "docx"])

# 生成文字云的函数
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    return fig

if uploaded_file:
    file_type = uploaded_file.name.split(".")[-1]  # 获取文件类型

    if file_type in ["csv", "xlsx", "xls"]:
        # 处理 CSV 或 Excel 文件
        if file_type == "csv":
            data = pd.read_csv(uploaded_file)
        else:
            data = pd.read_excel(uploaded_file)

        # 数据预览
        st.write("### Data Preview")
        st.dataframe(data)

        # 检测数值列
        numeric_columns = data.select_dtypes(include=["float64", "int64"]).columns

        if len(numeric_columns) > 0:
            # 图表选项
            st.write("### Visualization Options")
            chart_type = st.selectbox("Select chart type", ["Line Chart", "Bar Chart", "Pie Chart"])
            column = st.selectbox("Select a column to visualize", numeric_columns)

            # 生成图表
            if chart_type == "Line Chart":
                st.line_chart(data[column])
            elif chart_type == "Bar Chart":
                st.bar_chart(data[column])
            elif chart_type == "Pie Chart":
                fig, ax = plt.subplots()
                data[column].value_counts().plot.pie(autopct="%1.1f%%", ax=ax)
                st.pyplot(fig)
        else:
            st.warning("The uploaded file does not contain numeric columns for visualization.")

    elif file_type == "docx":
        # 处理 Word 文件
        doc = docx.Document(uploaded_file)
        text = " ".join([para.text for para in doc.paragraphs])
        st.write("### Word Cloud from Word Document")
        fig = generate_wordcloud(text)
        st.pyplot(fig)

    else:
        st.error("Unsupported file type. Please upload a CSV, Excel, or Word file.")

else:
    st.info("Please upload a file to start.")
