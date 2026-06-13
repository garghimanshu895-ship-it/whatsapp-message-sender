import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Contacts Manager")

st.title("👥 Contacts Manager")

# ==========================
# Create file if not exists
# ==========================

data_path = Path("data/contacts.csv")

if not data_path.exists():
    df = pd.DataFrame(
        columns=["Name", "Phone", "Email", "Category"]
    )
    df.to_csv(data_path, index=False)

# ==========================
# Load Contacts
# ==========================

df = pd.read_csv(
    data_path,
    dtype={"Phone": str}
)

# ==========================
# Add Contact Section
# ==========================

st.subheader("➕ Add New Contact")

col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Name")

with col2:
    phone = st.text_input("Phone Number")

email = st.text_input("Email")

category = st.selectbox(
    "Category",
    ["Friend", "Family", "College", "Work"]
)

if st.button("Add Contact"):

    if not name.strip():
        st.error("Name is required")

    elif not phone.strip():
        st.error("Phone number is required")

    elif phone in df["Phone"].astype(str).values:
        st.warning("Phone number already exists")

    else:

        new_contact = pd.DataFrame(
            {
                "Name": [name.strip()],
                "Phone": [phone.strip()],
                "Email": [email.strip()],
                "Category": [category]
            }
        )

        df = pd.concat(
            [df, new_contact],
            ignore_index=True
        )

        df.to_csv(
            data_path,
            index=False
        )

        st.success("✅ Contact Added Successfully")
        

st.divider()

# ==========================
# Search Section
# ==========================

st.subheader("🔍 Search Contact")

search = st.text_input("Search by Name")

if search:

    filtered_df = df[
        df["Name"]
        .astype(str)
        .str.strip()
        .str.contains(
            search.strip(),
            case=False,
            na=False
        )
    ]

    if filtered_df.empty:
        st.warning("No contact found")

else:
    filtered_df = df

# ==========================
# Contact Statistics
# ==========================

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Contacts",
        len(df)
    )

with col2:
    st.metric(
        "Categories",
        df["Category"].nunique()
        if not df.empty else 0
    )

st.divider()

# ==========================
# Display Contacts
# ==========================

st.subheader("📋 Contact List")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ==========================
# Delete Contact
# ==========================

st.subheader("🗑 Delete Contact")

if not df.empty:

    contact_to_delete = st.selectbox(
        "Select Contact",
        df["Name"]
    )

    if st.button("Delete Contact"):

        df = df[
            df["Name"] != contact_to_delete
        ]

        df.to_csv(
            data_path,
            index=False
        )

        st.success(
            f"{contact_to_delete} deleted successfully"
        )

        st.rerun()

else:
    st.info("No contacts available")

st.divider()

# ==========================
# Export Contacts
# ==========================

st.subheader("⬇ Export Contacts")

csv = df.to_csv(index=False)

st.download_button(
    label="Download Contacts CSV",
    data=csv,
    file_name="contacts.csv",
    mime="text/csv"
)
