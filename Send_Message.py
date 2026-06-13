import streamlit as st
import pandas as pd
import pywhatkit as kit
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(
    page_title="Send Message",
    page_icon="📨",
    layout="wide"
)

st.title("📨 Send WhatsApp Message")



contacts_file = Path("data/contacts.csv")
history_file = Path("data/history.csv")

if not contacts_file.exists():
    st.error("contacts.csv not found")
    st.stop()

contacts = pd.read_csv(
    contacts_file,
    dtype={"Phone": str}
)

if contacts.empty:
    st.warning("No contacts available. Please add contacts first.")
    st.stop()



st.subheader("Select Contact")

contact_name = st.selectbox(
    "Choose Contact",
    contacts["Name"]
)

selected_contact = contacts[
    contacts["Name"] == contact_name
].iloc[0]




phone = str(
    selected_contact["Phone"]
).split(".")[0].strip()
if not phone.startswith("+91"):
    phone = "+91" + phone
st.info(f"📞 Phone Number: {phone}")



message = st.text_area(
    "Type Your Message",
    height=150
)



if st.button(
    "🚀 Send WhatsApp Message",
    use_container_width=True
):

    if not message.strip():

        st.error(
            "Please enter a message"
        )

    else:

        try:

            # Add country code if missing

            if not phone.startswith("+"):
                phone = "+91" + phone

            st.info(
                "Opening WhatsApp Web..."
            )

            kit.sendwhatmsg_instantly(
                phone,
                message,
                wait_time=15,
                tab_close=True,
                close_time=5
            )

            now = datetime.now()

        

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

            new_record = pd.DataFrame(
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
                    "Status": ["Success"]
                }
            )

            history = pd.concat(
                [history, new_record],
                ignore_index=True
            )

            history.to_csv(
                history_file,
                index=False
            )

            success_box = st.empty()

            success_box.success(
                "✅ Message Sent Successfully"
            )

            time.sleep(3)

            success_box.empty()

        except Exception as e:

            st.error(
                f"Error: {str(e)}"
            )

            now = datetime.now()

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

            error_record = pd.DataFrame(
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
                    "Status": ["Failed"]
                }
            )

            history = pd.concat(
                [history, error_record],
                ignore_index=True
            )

            history.to_csv(
                history_file,
                index=False
            )