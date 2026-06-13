import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Smart WhatsApp Automation Dashboard")

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

contacts_file = data_dir / "contacts.csv"
history_file = data_dir / "history.csv"
scheduled_file = data_dir / "scheduled.csv"

if not contacts_file.exists():
    pd.DataFrame(
        columns=[
            "Name",
            "Phone",
            "Email",
            "Category"
        ]
    ).to_csv(contacts_file, index=False)

if not history_file.exists():
    pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Phone",
            "Message",
            "Status"
        ]
    ).to_csv(history_file, index=False)

if not scheduled_file.exists():
    pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Phone",
            "Message"
        ]
    ).to_csv(scheduled_file, index=False)


contacts = pd.read_csv(contacts_file)
history = pd.read_csv(history_file)
scheduled = pd.read_csv(scheduled_file)


st.subheader("📈 Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👥 Total Contacts",
        len(contacts)
    )

with col2:
    st.metric(
        "📨 Messages Sent",
        len(history)
    )

with col3:
    st.metric(
        "⏰ Scheduled Messages",
        len(scheduled)
    )

with col4:

    if (
        not history.empty
        and "Status" in history.columns
    ):

        success = len(
            history[
                history["Status"] == "Success"
            ]
        )

        success_rate = round(
            success / len(history) * 100,
            2
        )

    else:
        success_rate = 0

    st.metric(
        "📈 Success Rate",
        f"{success_rate}%"
    )

st.divider()

st.subheader("👥 Contacts by Category")

if not contacts.empty:

    category_count = (
        contacts["Category"]
        .value_counts()
    )

    st.bar_chart(category_count)

else:
    st.info(
        "No contacts available"
    )

st.divider()

st.subheader("📋 Recent Contacts")

if not contacts.empty:

    st.dataframe(
        contacts.tail(5),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No contacts found"
    )

st.divider()

st.subheader("📨 Message Analytics")

if (
    not history.empty
    and "Status" in history.columns
):

    status_count = (
        history["Status"]
        .value_counts()
    )

    st.bar_chart(status_count)

else:
    st.info(
        "No message history available"
    )

st.divider()

st.subheader("⏰ Upcoming Scheduled Messages")

if not scheduled.empty:
    st.dataframe(
        scheduled.tail(5),
        use_container_width=True,
        hide_index=True
    )

else:
    st.info(
        "No scheduled messages"
    )

st.divider()

st.caption(
    "Smart WhatsApp Automation System | Developed using Streamlit, Pandas and Python"
)