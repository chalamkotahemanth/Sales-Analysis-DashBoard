import streamlit as st
import pandas as pd
import plotly.express as px

# Load the Excel file
df = pd.read_csv("Sample - Superstore2.csv")

# Drop rows with missing data
df.dropna(inplace=True)

# Fix mixed date formats safely
df["Order Date"] = pd.to_datetime(df["Order Date"], format='mixed', dayfirst=False, errors='coerce')

# Title of the dashboard
st.title("📊 Sales Analysis Dashboard")

# Sidebar Filters
region = st.sidebar.selectbox("Select Region", df["Region"].unique())
category = st.sidebar.multiselect("Select Category", df["Category"].unique(), default=df["Category"].unique())

# Filter data based on sidebar
filtered_df = df[(df["Region"] == region) & (df["Category"].isin(category))]

# KPIs
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
col2.metric("📈 Total Profit", f"${total_profit:,.2f}")
col3.metric("🧾 Total Orders", total_orders)

# Sales Over Time
st.subheader("📆 Monthly Sales Trend")
monthly_sales = filtered_df.groupby(filtered_df["Order Date"].dt.to_period("M")).sum(numeric_only=True).reset_index()
monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig1 = px.line(monthly_sales, x="Order Date", y="Sales", title="Monthly Sales")
st.plotly_chart(fig1)

# Sales by Sub-Category
st.subheader("📦 Sales by Sub-Category")
subcategory_sales = filtered_df.groupby("Sub-Category")["Sales"].sum().sort_values()
fig2 = px.bar(subcategory_sales, orientation='h', title="Sales by Sub-Category")
st.plotly_chart(fig2)

# Profit vs Discount
st.subheader("💸 Profit vs Discount")
fig3 = px.scatter(filtered_df, x="Discount", y="Profit", size="Sales", color="Category", title="Profit vs Discount")
st.plotly_chart(fig3)

st.markdown("Built with ❤️ using Streamlit")
