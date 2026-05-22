import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(page_title="Interactive Dashboard", layout="wide")

st.title("📊 Interactive Electronic Product Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
product_df = pd.read_csv("cleaned_products.csv")
electronic_df = pd.read_csv("electronics_cleaned.csv")

# Merge option (if common column exists)
df = electronic_df.copy()

# -----------------------------
# SIDEBAR FILTERS (INTERACTIVE SLICERS)
# -----------------------------
st.sidebar.header("🔎 Filters")

# Category filter
if "category" in df.columns:
    category = st.sidebar.multiselect(
        "Select Category",
        df["category"].unique(),
        default=df["category"].unique()
    )
    df = df[df["category"].isin(category)]

# Product filter
if "product" in df.columns:
    product = st.sidebar.multiselect(
        "Select Product",
        df["product"].unique(),
        default=df["product"].unique()
    )
    df = df[df["product"].isin(product)]

# -----------------------------
# KPI CARDS (LIVE UPDATE)
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Records", len(df))

with col2:
    if "sales" in df.columns:
        st.metric("Total Sales", int(df["sales"].sum()))
    else:
        st.metric("Total Sales", "N/A")

with col3:
    if "price" in df.columns:
        st.metric("Avg Price", round(df["price"].mean(), 2))
    else:
        st.metric("Avg Price", "N/A")

st.write("---")

# -----------------------------
# CHARTS SECTION
# -----------------------------
col1, col2 = st.columns(2)

# -----------------------------
# BAR CHART (INTERACTIVE)
# -----------------------------
with col1:
    st.subheader("📊 Sales by Category")

    if "category" in df.columns and "sales" in df.columns:
        fig_bar = px.bar(
            df,
            x="category",
            y="sales",
            color="category",
            text="sales"
        )
        fig_bar.update_traces(textposition="outside")
        st.plotly_chart(fig_bar, use_container_width=True)

# -----------------------------
# PIE / DONUT CHART
# -----------------------------
with col2:
    st.subheader("🍩 Category Distribution")

    if "category" in df.columns:
        fig_pie = px.pie(
            df,
            names="category",
            values="sales" if "sales" in df.columns else None,
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

st.write("---")

# -----------------------------
# ADVANCED INTERACTIVE TABLE
# -----------------------------
st.subheader("📋 Interactive Data Table")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# DOWNLOAD BUTTON (INTERACTIVE FEATURE)
# -----------------------------
csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv"
)