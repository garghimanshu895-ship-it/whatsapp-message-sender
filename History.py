import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Message History",
    page_icon="📜",
    layout="wide"
)

st.title("📜 Message History")



history_file = Path("data/history.csv")

if not history_file.exists():

    pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Phone",
            "Message",
            "Status"
        ]
    ).to_csv(
        history_file,
        index=False
    )

history = pd.read_csv(history_file)



col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Messages",
        len(history)
    )

with col2:

    success_count = len(
        history[
            history["Status"] == "Success"
        ]
    ) if not history.empty else 0

    st.metric(
        "Successful",
        success_count
    )

with col3:

    failed_count = len(
        history[
            history["Status"] == "Failed"
        ]
    ) if not history.empty else 0

    st.metric(
        "Failed",
        failed_count
    )

st.divider()


search = st.text_input(
    "🔍 Search Phone Number"
)

status_filter = st.selectbox(
    "Filter by Status",
    [
        "All",
        "Success",
        "Failed"
    ]
)

filtered_df = history.copy()

# Search Filter

if search:

    filtered_df = filtered_df[
        filtered_df["Phone"]
        .astype(str)
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]


if status_filter != "All":

    filtered_df = filtered_df[
        filtered_df["Status"]
        == status_filter
    ]

st.divider()



st.subheader("📋 Message Records")

if filtered_df.empty:

    st.info(
        "No records found"
    )

else:

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()



csv = history.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download History Report",
    data=csv,
    file_name="history_report.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()


if st.button(
    "🗑 Clear Entire History",
    use_container_width=True
):

    pd.DataFrame(
        columns=[
            "Date",
            "Time",
            "Phone",
            "Message",
            "Status"
        ]
    ).to_csv(
        history_file,
        index=False
    )

    st.success(
        "History Cleared Successfully"
    )

    st.rerun()