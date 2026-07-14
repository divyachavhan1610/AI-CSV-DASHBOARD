import streamlit as st
import pandas as pd
import plotly.express as px


def show_charts(df):

    st.header("📊 Automatic Data Visualizations")

    # ----------------------------------------
    # Detect Column Types
    # ----------------------------------------

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    # Detect Date Columns
    date_cols = []

    for col in df.columns:
        if "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")
            date_cols.append(col)

    # ----------------------------------------
    # Histogram
    # ----------------------------------------

    if numeric_cols:

        st.subheader("📈 Distribution")

        selected_num = st.selectbox(
            "Select Numeric Column",
            numeric_cols,
            key="histogram"
        )

        fig = px.histogram(
            df,
            x=selected_num,
            nbins=20,
            title=f"Distribution of {selected_num}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # Bar Chart
    # ----------------------------------------

    if categorical_cols and numeric_cols:

        st.subheader("📊 Bar Chart")

        x_col = st.selectbox(
            "Category Column",
            categorical_cols,
            key="bar_x"
        )

        y_col = st.selectbox(
            "Numeric Column",
            numeric_cols,
            key="bar_y"
        )

        grouped = df.groupby(x_col)[y_col].sum().reset_index()

        fig = px.bar(
            grouped,
            x=x_col,
            y=y_col,
            text_auto=True,
            title=f"{y_col} by {x_col}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # Pie Chart
    # ----------------------------------------

    if categorical_cols and numeric_cols:

        st.subheader("🥧 Pie Chart")

        cat_col = st.selectbox(
            "Category",
            categorical_cols,
            key="pie_category"
        )

        value_col = st.selectbox(
            "Value",
            numeric_cols,
            key="pie_value"
        )

        pie_df = df.groupby(cat_col)[value_col].sum().reset_index()

        fig = px.pie(
            pie_df,
            names=cat_col,
            values=value_col,
            title=f"{value_col} by {cat_col}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # Line Chart
    # ----------------------------------------

    if date_cols and numeric_cols:

        st.subheader("📉 Line Chart")

        date_col = st.selectbox(
            "Date Column",
            date_cols,
            key="line_date"
        )

        value_col = st.selectbox(
            "Numeric Value",
            numeric_cols,
            key="line_value"
        )

        temp = df.copy()

        temp["Month"] = temp[date_col].dt.to_period("M").astype(str)

        monthly = (
            temp.groupby("Month")[value_col]
            .sum()
            .reset_index()
        )

        fig = px.line(
            monthly,
            x="Month",
            y=value_col,
            markers=True,
            title=f"Monthly {value_col}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # Scatter Plot
    # ----------------------------------------

    if len(numeric_cols) >= 2:

        st.subheader("🔵 Scatter Plot")

        x_axis = st.selectbox(
            "X-Axis",
            numeric_cols,
            key="scatter_x"
        )

        y_axis = st.selectbox(
            "Y-Axis",
            numeric_cols,
            index=1,
            key="scatter_y"
        )

        fig = px.scatter(
            df,
            x=x_axis,
            y=y_axis,
            title=f"{y_axis} vs {x_axis}"
        )

        st.plotly_chart(fig, use_container_width=True)

    # ----------------------------------------
    # Correlation Heatmap
    # ----------------------------------------

    if len(numeric_cols) >= 2:

        st.subheader("🔥 Correlation Heatmap")

        corr = df[numeric_cols].corr()

        fig = px.imshow(
            corr,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        st.plotly_chart(fig, use_container_width=True)