import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="Scheduler",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ Message Scheduler")

# ==========================
# Load Files
# ==========================

contacts_file = Path("data/contacts.csv")
scheduled_file = Path("data/scheduled.csv")

if not scheduled_file.exists():

    pd.DataFrame(
        columns=[
            "Name",
            "Phone",
            "Date",
            "Time",
            "Message"
        ]
    ).to_csv(
        scheduled_file,
        index=False
    )

if not contacts_file.exists():
    st.error("Contacts file not found")
    st.stop()

contacts = pd.read_csv(
    contacts_file,
    dtype={"Phone": str}
)

if contacts.empty:
    st.warning("Add contacts first")
    st.stop()

scheduled = pd.read_csv(scheduled_file)

# ==========================
# Schedule Form
# ==========================

st.subheader("➕ Schedule New Message")

contact_name = st.selectbox(
    "Select Contact",
    contacts["Name"]
)

selected_contact = contacts[
    contacts["Name"] == contact_name
].iloc[0]

phone = selected_contact["Phone"]

message = st.text_area(
    "Message"
)

col1, col2 = st.columns(2)

with col1:
    selected_date = st.date_input(
        "Select Date"
    )

with col2:
    selected_time = st.time_input(
        "Select Time"
    )

# ==========================
# Save Schedule
# ==========================

if st.button(
    "Save Schedule",
    use_container_width=True
):

    if not message.strip():

        st.error(
            "Please enter a message"
        )

    else:

        new_schedule = pd.DataFrame(
            {
                "Name": [contact_name],
                "Phone": [phone],
                "Date": [selected_date],
                "Time": [selected_time],
                "Message": [message]
            }
        )

        scheduled = pd.concat(
            [scheduled, new_schedule],
            ignore_index=True
        )

        scheduled.to_csv(
            scheduled_file,
            index=False
        )

        st.success(
            "Schedule Added Successfully"
        )

        st.rerun()

st.divider()

# ==========================
# View Scheduled Messages
# ==========================

st.subheader("📋 Scheduled Messages")

if scheduled.empty:

    st.info(
        "No scheduled messages"
    )

else:

    st.dataframe(
        scheduled,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# ==========================
# Delete Schedule
# ==========================

st.subheader("🗑 Delete Schedule")

if not scheduled.empty:

    schedule_index = st.selectbox(
        "Select Schedule",
        scheduled.index
    )

    if st.button(
        "Delete Selected Schedule",
        use_container_width=True
    ):

        scheduled = scheduled.drop(
            schedule_index
        )

        scheduled.to_csv(
            scheduled_file,
            index=False
        )
        

        st.success(
            "Schedule Deleted"
        )

        st.rerun()