import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE SETTINGS
# -----------------------------
st.set_page_config(
    page_title="UAC Healthcare Analytics",
    layout="wide"
)

st.title("📊 System Capacity & Care Load Analytics")
st.write("Healthcare Analytics Dashboard for Unaccompanied Children")

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_excel("UAC_Feature_Engineered_Data.xlsx")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------
# SIDEBAR FILTER
# -----------------------------
st.sidebar.header("Filters")

start = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered = df[
    (df["Date"] >= pd.to_datetime(start)) &
    (df["Date"] <= pd.to_datetime(end))
]

# -----------------------------
# KPI CARDS
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Load",
    int(filtered["Total System Load"].iloc[-1])
)

col2.metric(
    "Maximum Load",
    int(filtered["Total System Load"].max())
)

col3.metric(
    "Average Load",
    round(filtered["Total System Load"].mean(),2)
)

# -----------------------------
# GRAPH 1
# -----------------------------
st.subheader("Total System Load")

fig = px.line(
    filtered,
    x="Date",
    y="Total System Load"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# GRAPH 2
# -----------------------------
st.subheader("CBP vs HHS")

fig = px.line(
    filtered,
    x="Date",
    y=[
        "Children in CBP custody",
        "Children in HHS Care"
    ]
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# GRAPH 3
# -----------------------------
st.subheader("Net Intake")

fig = px.line(
    filtered,
    x="Date",
    y="Net Intake"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# GRAPH 4
# -----------------------------
st.subheader("Backlog")

fig = px.line(
    filtered,
    x="Date",
    y="Backlog"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# GRAPH 5
# -----------------------------
st.subheader("Rolling Average")

fig = px.line(
    filtered,
    x="Date",
    y=[
        "7-Day Rolling Avg",
        "14-Day Rolling Avg"
    ]
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("Key Insights")

st.write(
    "Highest System Load:",
    filtered["Total System Load"].max()
)

st.write(
    "Highest Net Intake:",
    filtered["Net Intake"].max()
)

st.write(
    "Highest Backlog:",
    filtered["Backlog"].max()
)

# -----------------------------
# DOWNLOAD
# -----------------------------
st.subheader("Download Data")

csv = filtered.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Filtered_Data.csv",
    mime="text/csv"
)
