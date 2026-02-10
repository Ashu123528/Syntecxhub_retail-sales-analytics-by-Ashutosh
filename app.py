import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Retail Sales Analytics Dashboard", layout="wide")
sns.set_style("whitegrid")

# Load data
df = pd.read_csv("retail_sales_data.csv")
df["order_date"] = pd.to_datetime(df["order_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# Sidebar filters
st.sidebar.header("Filters")

region_filter = st.sidebar.multiselect(
    "Select Region",
    df["region"].unique(),
    default=df["region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category",
    df["category"].unique(),
    default=df["category"].unique()
)

filtered_df = df[
    (df["region"].isin(region_filter)) &
    (df["category"].isin(category_filter))
]

# ===== TITLE =====
st.title("🛒 Retail Sales Analytics Dashboard")
st.markdown("**Company-level dashboard for business decision making**")

# ===== KPIs =====
total_sales = filtered_df["sales"].sum()
total_profit = filtered_df["profit"].sum()
profit_margin = (total_profit / total_sales) * 100

top_region = (
    filtered_df.groupby("region")["sales"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("category")["profit"]
    .sum()
    .idxmax()
)

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Sales", f"{total_sales:,.0f}")
k2.metric("📈 Total Profit", f"{total_profit:,.0f}")
k3.metric("📉 Profit Margin", f"{profit_margin:.2f}%")
k4.metric("🏆 Top Region", top_region)

st.info(f"✅ **Best Performing Category:** {best_category}")

st.divider()

# ===== VISUALS ROW 1 =====
c1, c2 = st.columns(2)

with c1:
    st.subheader("Total Sales by Category")
    fig, ax = plt.subplots()
    sns.barplot(data=filtered_df, x="category", y="sales", estimator=sum, ax=ax)
    st.pyplot(fig)

with c2:
    st.subheader("Profit Distribution by Category")
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, x="category", y="profit", ax=ax)
    st.pyplot(fig)

st.divider()

# ===== VISUALS ROW 2 =====
c3, c4 = st.columns(2)

with c3:
    st.subheader("Region × Category Sales Heatmap")
    pivot = filtered_df.pivot_table(
        values="sales",
        index="region",
        columns="category",
        aggfunc="sum"
    )
    fig, ax = plt.subplots()
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="Blues", ax=ax)
    st.pyplot(fig)

with c4:
    st.subheader("Sales vs Profit Relationship")
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=filtered_df,
        x="sales",
        y="profit",
        hue="category",
        style="region",
        ax=ax
    )
    st.pyplot(fig)

st.divider()

# ===== TREND =====
st.subheader("📅 Monthly Sales Trend")
monthly_sales = filtered_df.groupby("month")["sales"].sum().reset_index()

fig, ax = plt.subplots(figsize=(12,4))
sns.lineplot(data=monthly_sales, x="month", y="sales", marker="o", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

st.divider()

# ===== INSIGHTS =====
st.subheader("📌 Business Insights (What company should do)")

st.markdown("""
- **Technology category** drives high profit but shows volatility → pricing strategy needed  
- **Top region** generates maximum sales → inventory & marketing focus here  
- **Profit margin (%)** gives quick health check of business performance  
""")
