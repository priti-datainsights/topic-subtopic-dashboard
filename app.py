import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Topic & SubTopic Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================

FILE_PATH = "Topic_SubTopic_Cancelled_Offline_May2026.xlsx"

@st.cache_data
def load_data():

    topic_df = pd.read_excel(
        FILE_PATH,
        sheet_name="Topic-SubTopic"
    )

    cancelled_df = pd.read_excel(
        FILE_PATH,
        sheet_name="Cancelled Sessions"
    )

    offline_df = pd.read_excel(
        FILE_PATH,
        sheet_name="Offline Sessions"
    )

    return topic_df, cancelled_df, offline_df


topic_df, cancelled_df, offline_df = load_data()

topic_df["session_date"] = pd.to_datetime(
    topic_df["session_date"],
    errors="coerce"
)

# =========================
# SIDEBAR FILTERS
# =========================

st.sidebar.header("Filters")

state_filter = st.sidebar.multiselect(
    "State",
    sorted(topic_df["state"].dropna().unique())
)

grade_filter = st.sidebar.multiselect(
    "Grade",
    sorted(topic_df["grade"].dropna().unique())
)

subject_filter = st.sidebar.multiselect(
    "Subject",
    sorted(topic_df["subject"].dropna().unique())
)

status_filter = st.sidebar.multiselect(
    "Session Status",
    sorted(topic_df["session_status"].dropna().unique())
)

subproject_filter = st.sidebar.multiselect(
    "Sub Project",
    sorted(topic_df["Sub_Project"].dropna().unique())
)

# =========================
# FILTER DATA
# =========================

filtered_df = topic_df.copy()

if state_filter:
    filtered_df = filtered_df[
        filtered_df["state"].isin(state_filter)
    ]

if grade_filter:
    filtered_df = filtered_df[
        filtered_df["grade"].isin(grade_filter)
    ]

if subject_filter:
    filtered_df = filtered_df[
        filtered_df["subject"].isin(subject_filter)
    ]

if status_filter:
    filtered_df = filtered_df[
        filtered_df["session_status"].isin(status_filter)
    ]

if subproject_filter:
    filtered_df = filtered_df[
        filtered_df["Sub_Project"].isin(subproject_filter)
    ]

# =========================
# HEADER
# =========================

st.title("Topic & Sub Topic Dashboard")

# =========================
# KPI CARDS
# =========================

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Sessions",
    filtered_df["session_id"].nunique()
)

c2.metric(
    "Centers",
    filtered_df["center_id"].nunique()
)

c3.metric(
    "Volunteers",
    filtered_df["vt_ev_id"].nunique()
)

c4.metric(
    "Topics",
    filtered_df["topic_name"].nunique()
)

c5.metric(
    "Sub Topics",
    filtered_df["sub_topic_name"].nunique()
)

# =========================
# TOPIC ANALYSIS
# =========================

st.subheader("Top Topics")

topic_summary = (
    filtered_df
    .groupby("topic_name")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
    .sort_values("Sessions", ascending=False)
    .head(20)
)

st.bar_chart(
    topic_summary.set_index("topic_name")
)

# =========================
# SUB TOPIC ANALYSIS
# =========================

st.subheader("Top Sub Topics")

subtopic_summary = (
    filtered_df
    .groupby("sub_topic_name")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
    .sort_values("Sessions", ascending=False)
    .head(20)
)

st.bar_chart(
    subtopic_summary.set_index("sub_topic_name")
)

# =========================
# STATE ANALYSIS
# =========================

st.subheader("State-wise Sessions")

state_summary = (
    filtered_df
    .groupby("state")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
    .sort_values("Sessions", ascending=False)
)

st.bar_chart(
    state_summary.set_index("state")
)

# =========================
# VOLUNTEER ANALYSIS
# =========================

st.subheader("Volunteer-wise Sessions")

vol_summary = (
    filtered_df
    .groupby("vt_name")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
    .sort_values("Sessions", ascending=False)
    .head(20)
)

st.bar_chart(
    vol_summary.set_index("vt_name")
)

# =========================
# SESSION STATUS
# =========================

st.subheader("Session Status Distribution")

status_summary = (
    filtered_df
    .groupby("session_status")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
)

st.dataframe(status_summary)

# =========================
# TREND
# =========================

st.subheader("Daily Session Trend")

trend = (
    filtered_df
    .groupby("session_date")["session_id"]
    .nunique()
    .reset_index(name="Sessions")
)

st.line_chart(
    trend.set_index("session_date")
)

# =========================
# DATA TABLE
# =========================

st.subheader("Detailed Data")

st.dataframe(
    filtered_df,
    use_container_width=True
)

csv = filtered_df.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "topic_subtopic_data.csv",
    "text/csv"
)
