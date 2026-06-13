import streamlit as st
import pandas as pd
import pywhatkit as kit
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(
    page_title="Bulk Messaging",
    page_icon="👥",
    layout="wide"
)

st.title("👥 Bulk WhatsApp Messaging")

# ==========================
# Load Data
# ==========================

contacts_file = Path("data/contacts.csv")
history_file = Path("data/history.csv")

if not contacts_file.exists():
    st.error("Contacts file not found")
    st.stop()

contacts = pd.read_csv(
    contacts_file,
    dtype={"Phone": str}
)

if contacts.empty:
    st.warning("No contacts available")
    st.stop()

# ==========================
# Select Contacts
# ==========================

selected_contacts = st.multiselect(
    "Select Contacts",
    contacts["Name"].tolist()
)

message = st.text_area(
    "Message",
    height=150
)

# ==========================
# Preview
# ==========================

if selected_contacts:

    preview_df = contacts[
        contacts["Name"].isin(
            selected_contacts
        )
    ]

    st.subheader("Selected Contacts")

    st.dataframe(
        preview_df,
        use_container_width=True,
        hide_index=True
    )

# ==========================
# Send Bulk Messages
# ==========================

if st.button(
    "🚀 Send Bulk Messages",
    use_container_width=True
):

    if not selected_contacts:

        st.error(
            "Select at least one contact"
        )

    elif not message.strip():

        st.error(
            "Enter a message"
        )

    else:

        progress = st.progress(0)

        if history_file.exists():
            history = pd.read_csv(
                history_file
            )
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

        total = len(
            selected_contacts
        )

        for i, name in enumerate(
            selected_contacts
        ):

            try:

                row = contacts[
                    contacts["Name"] == name
                ].iloc[0]

                phone = str(
    row["Phone"]
).split(".")[0].strip()

                if not phone.startswith("+"):
                    phone = "+91" + phone

                kit.sendwhatmsg_instantly(
                    phone,
                    message,
                    wait_time=15,
                    tab_close=True,
                    close_time=5
                )

                status = "Success"

            except Exception:

                status = "Failed"

            now = datetime.now()

            new_row = pd.DataFrame(
                {
                    "Date": [
                        now.strftime(
                            "%Y-%m-%d"
                        )
                    ],
                    "Time": [
                        now.strftime(
                            "%H:%M:%S"
                        )
                    ],
                    "Phone": [phone],
                    "Message": [message],
                    "Status": [status]
                }
            )

            history = pd.concat(
                [history, new_row],
                ignore_index=True
            )

            progress.progress(
                (i + 1) / total
            )

        history.to_csv(
            history_file,
            index=False
        )

        success_box = st.empty()

        success_box.success(
            f"✅ {total} Messages Processed"
        )

        time.sleep(3)

        success_box.empty()
