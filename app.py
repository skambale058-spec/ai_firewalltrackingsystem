import streamlit as st
import pandas as pd
import plotly.express as px
from utils.ai_model import detect_anomalies
st.set_page_config(
    page_title="AI Firewall Guardian",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Firewall Guardian")
st.caption("AI Based Firewall Threat Detection Dashboard")

uploaded_file = st.sidebar.file_uploader(
    "Upload Firewall Log (CSV)",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/firewall_logs.csv")
    df = detect_anomalies(df)

st.success("Firewall Logs Loaded Successfully")

# ---------------- Metrics ----------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Logs", len(df))
col2.metric("Denied", len(df[df["action"] == "DENY"]))
col3.metric("Allowed", len(df[df["action"] == "ALLOW"]))
col4.metric("Unique IPs", df["source_ip"].nunique())

st.divider()

# ---------------- Logs ----------------

st.subheader("Firewall Logs")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ---------------- Action Chart ----------------

st.subheader("Allowed vs Denied")

fig = px.histogram(
    df,
    x="action",
    color="action",
    text_auto=True
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Protocol ----------------

st.subheader("Protocol Distribution")

fig2 = px.pie(
    df,
    names="protocol",
    hole=.45
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- Ports ----------------

st.subheader("Top Targeted Ports")

port_df = (
    df["port"]
    .value_counts()
    .reset_index()
)

port_df.columns = ["Port", "Count"]

fig3 = px.bar(
    port_df,
    x="Port",
    y="Count",
    color="Count",
    text_auto=True
)

st.plotly_chart(fig3, use_container_width=True)

# ---------------- Top Attackers ----------------

st.subheader("Top Source IPs")

ip_df = (
    df["source_ip"]
    .value_counts()
    .reset_index()
)

ip_df.columns = ["IP", "Count"]

fig4 = px.bar(
    ip_df,
    x="IP",
    y="Count",
    color="Count",
    text_auto=True
)

st.plotly_chart(fig4, use_container_width=True)

st.divider()

st.info("AI Detection Module Coming Next...")
st.divider()

st.subheader("🤖 AI Threat Detection")

critical = df[df["threat_level"] == "Critical"]
high = df[df["threat_level"] == "High"]

c1, c2 = st.columns(2)

c1.metric("Critical Threats", len(critical))
c2.metric("High Threats", len(high))

st.dataframe(
    df[
        [
            "source_ip",
            "port",
            "bytes",
            "risk_score",
            "threat_level"
        ]
    ],
    use_container_width=True,
    hide_index=True
)
