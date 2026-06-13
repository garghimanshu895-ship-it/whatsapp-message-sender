import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Analytics Dashboard")

# ==========================
# Load Files
# ==========================

history_file = Path("data/history.csv")
contacts_file = Path("data/contacts.csv")

if history_file.exists():
    history = pd.read_csv(history_file)
else:
    history = pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Phone",
            "Message",
            "Status"
        ]
    )

if contacts_file.exists():
    contacts = pd.read_csv(contacts_file)
else:
    contacts = pd.DataFrame(
        columns=[
            "Name",
            "Phone",
            "Email",
            "Category"
        ]
    )

# ==========================
# KPI Cards
# ==========================

total_messages = len(history)

success_messages = len(
    history[
        history["Status"] == "Success"
    ]
) if not history.empty else 0

failed_messages = len(
    history[
        history["Status"] == "Failed"
    ]
) if not history.empty else 0

success_rate = (
    round(
        success_messages /
        total_messages * 100,
        2
    )
    if total_messages > 0
    else 0
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📨 Total Messages",
        total_messages
    )

with col2:
    st.metric(
        "✅ Successful",
        success_messages
    )

with col3:
    st.metric(
        "❌ Failed",
        failed_messages
    )

with col4:
    st.metric(
        "📈 Success Rate",
        f"{success_rate}%"
    )

st.divider()

# ==========================
# Messages Per Day
# ==========================

st.subheader("📅 Messages Per Day")

if not history.empty:

    daily_messages = (
        history["Date"]
        .value_counts()
        .sort_index()
    )

    st.line_chart(
        daily_messages
    )

else:
    st.info(
        "No message data available"
    )

st.divider()

# ==========================
# Success vs Failed
# ==========================

st.subheader("📊 Success vs Failed")

if not history.empty:

    status_count = (
        history["Status"]
        .value_counts()
    )

    st.bar_chart(
        status_count
    )

else:
    st.info(
        "No status data available"
    )

st.divider()

# ==========================
# Contact Categories
# ==========================

st.subheader("👥 Contact Categories")

if not contacts.empty:

    category_count = (
        contacts["Category"]
        .value_counts()
    )

    st.bar_chart(
        category_count
    )

else:
    st.info(
        "No contact data available"
    )

st.divider()

# ==========================
# Top Contacted Numbers
# ==========================

st.subheader("📞 Top Contacted Numbers")

if not history.empty:

    top_contacts = (
        history["Phone"]
        .value_counts()
        .head(10)
    )

    st.bar_chart(
        top_contacts
    )

else:
    st.info(
        "No phone activity available"
    )

st.divider()

# ==========================
# Recent Activity
# ==========================

st.subheader("🕒 Recent Activity")

if not history.empty:

    st.dataframe(
        history.tail(10),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No recent activity"
    )