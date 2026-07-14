import streamlit as st
import pandas as pd
from data_cleaning import clean_data
from charts import show_charts

# --------------------------------
# Page Configuration
# --------------------------------
st.set_page_config(
    page_title="AI CSV Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------
# Title
# --------------------------------
st.title("📊 AI-Powered CSV Dashboard Generator")
st.write("Upload any CSV file and automatically clean, analyze, and visualize your data.")

# --------------------------------
# Sidebar
# --------------------------------
st.sidebar.header("📂 Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV File",
    type=["csv"]
)

# --------------------------------
# Read CSV
# --------------------------------
if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Clean Data
    df, report = clean_data(df)

    st.success("✅ CSV Uploaded Successfully!")

    # --------------------------------
    # Data Cleaning Report
    # --------------------------------

    st.subheader("🧹 Data Cleaning Report")

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows Before", report["Rows Before"])
    col2.metric("Rows After", report["Rows After"])
    col3.metric("Duplicates Removed", report["Duplicates Removed"])

    col4, col5 = st.columns(2)

    col4.metric("Missing Before", report["Missing Before"])
    col5.metric("Missing After", report["Missing After"])

    # --------------------------------
    # Dataset Preview
    # --------------------------------

    st.subheader("📄 Cleaned Dataset")

    st.dataframe(df)

    # --------------------------------
    # Dataset Information
    # --------------------------------

    st.subheader("📈 Dataset Information")

    c1, c2, c3 = st.columns(3)

    c1.metric("Rows", df.shape[0])
    c2.metric("Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())

    # Show Charts
    st.divider()
    show_charts(df)

    

else:

    st.info("⬅ Upload a CSV file from the sidebar to begin.")