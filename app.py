import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(
    page_title="Topic & SubTopic Analytics",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    background:#ffffff;
    padding:18px;
    border-radius:12px;
    box-shadow:0 2px 10px rgba(0,0,0,.08);
}

[data-testid="stMetricValue"]{
    font-size:34px;
    font-weight:700;
    color:#0f766e;
}

[data-testid="stSidebar"]{
    background:#0f172a;
}

[data-testid="stSidebar"] *{
    color:white;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA
# ==================================================

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

# ==================================================

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("📊 Filters")

# Keep original data untouched
base_df = topic_df.copy()

# -----------------------
# State
# -----------------------
state_filter = st.sidebar.multiselect(
    "State",
    sorted(base_df["state"].dropna().unique())
)

state_df = base_df.copy()

if state_filter:
    state_df = state_df[
        state_df["state"].isin(state_filter)
    ]

# -----------------------
# Subject
# -----------------------
subject_filter = st.sidebar.multiselect(
    "Subject",
    sorted(state_df["subject"].dropna().unique())
)

subject_df = state_df.copy()

if subject_filter:
    subject_df = subject_df[
        subject_df["subject"].isin(subject_filter)
    ]

# -----------------------
# Grade
# -----------------------
grade_filter = st.sidebar.multiselect(
    "Grade",
    sorted(subject_df["grade"].dropna().unique())
)

grade_df = subject_df.copy()

if grade_filter:
    grade_df = grade_df[
        grade_df["grade"].isin(grade_filter)
    ]

# -----------------------
# Session Status
# -----------------------
status_filter = st.sidebar.multiselect(
    "Session Status",
    sorted(
        grade_df["session_status"].dropna().unique()
    )
)

status_df = grade_df.copy()

if status_filter:
    status_df = status_df[
        status_df["session_status"].isin(status_filter)
    ]

# -----------------------
# Centre
# -----------------------
centre_filter = st.sidebar.multiselect(
    "Centre",
    sorted(
        status_df["center_name"].dropna().unique()
    )
)

filtered_df = status_df.copy()

if centre_filter:
    filtered_df = filtered_df[
        filtered_df["center_name"].isin(centre_filter)
    ]
# ==================================================

st.title("📚 Topic & SubTopic Analytics Dashboard")

# ==================================================
# KPI CARDS
# ==================================================

total_sessions = len(filtered_df)

unique_topics = filtered_df["topic_name"].nunique()

unique_subtopics = filtered_df["sub_topic_name"].nunique()

unique_centers = filtered_df["center_id"].nunique()
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Total Sessions", f"{total_sessions:,}")

with col2:
    st.metric("Unique Topics", f"{unique_topics:,}")

with col3:
    st.metric("Unique Subtopics", f"{unique_subtopics:,}")

with col4:
    st.metric("Active Centers", f"{unique_centers:,}")

# ==================================================
# TABS
# ==================================================

tab1, tab2, tab3 = st.tabs([
    "📚 Topic Analysis",
    "🚫 Cancelled Sessions",
    "📵 Offline Sessions"
])

# ==================================================
# TOPIC ANALYSIS
# ==================================================

with tab1:

    st.subheader("📋 Topic / Sub-topic Session Summary")

    pivot_table = (
        filtered_df
        .groupby(
            ["topic_name", "sub_topic_name"],
            dropna=False
        )
        .size()
        .reset_index(name="#Sessions")
        .sort_values("#Sessions", ascending=False)
    )

    pivot_table = pivot_table.rename(columns={
        "topic_name": "Topic",
        "sub_topic_name": "Sub-topic"
    })

    st.dataframe(
        pivot_table,
        use_container_width=True,
        hide_index=True,
        height=700
    )
# CANCELLED
# ==================================================

with tab2:

    st.subheader("Cancelled Session Analysis")

    st.metric(
        "Total Cancelled Sessions",
        len(cancelled_df)
    )

    cancel_chart = (
        cancelled_df
        .groupby("cancel_reason")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
        .head(15)
    )

    fig4 = px.bar(
        cancel_chart,
        x="Count",
        y="cancel_reason",
        orientation="h",
        title="Cancellation Reasons"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    state_cancel = (
        cancelled_df
        .groupby("State")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    fig5 = px.bar(
        state_cancel,
        x="State",
        y="Count",
        title="Cancelled Sessions by State"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ==================================================
# OFFLINE
# ==================================================

with tab3:

    st.subheader("Offline Session Analysis")

    st.metric(
        "Total Offline Sessions",
        len(offline_df)
    )

    offline_reason = (
        offline_df
        .groupby("Offline reason")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    fig6 = px.bar(
        offline_reason,
        x="Count",
        y="Offline reason",
        orientation="h",
        title="Offline Reasons"
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

    state_offline = (
        offline_df
        .groupby("State")
        .size()
        .reset_index(name="Count")
        .sort_values(
            "Count",
            ascending=False
        )
    )

    fig7 = px.bar(
        state_offline,
        x="State",
        y="Count",
        title="Offline Sessions by State"
    )

    st.plotly_chart(
        fig7,
        use_container_width=True
    )

# ==================================================
# DOWNLOAD
# ==================================================

st.download_button(
    "📥 Download Topic Data",
    filtered_df.to_csv(index=False),
    file_name="topic_data.csv"
)
