import pandas as pd
import pywhatkit as kit
import time
from datetime import datetime
from pathlib import Path

scheduled_file = Path("data/scheduled.csv")

print("Scheduler Started...")

while True:

    try:

        if scheduled_file.exists():

            scheduled = pd.read_csv(
                scheduled_file,
                dtype={"Phone": str}
            )

            if not scheduled.empty:

                current_date = datetime.now().strftime("%Y-%m-%d")
                current_time = datetime.now().strftime("%H:%M")

                rows_to_remove = []

                for index, row in scheduled.iterrows():

                    schedule_date = str(row["Date"])
                    schedule_time = str(row["Time"])[:5]

                    if (
                        schedule_date == current_date
                        and schedule_time == current_time
                    ):

                        phone = str(
                            row["Phone"]
                        ).split(".")[0].strip()

                        if not phone.startswith("+91"):
                            phone = "+91" + phone

                        message = row["Message"]

                        print(
                            f"Sending to {phone}"
                        )

                        kit.sendwhatmsg_instantly(
                            phone,
                            message,
                            wait_time=10,
                            tab_close=True,
                            close_time=5
                        )

                        rows_to_remove.append(
                            index
                        )

                if rows_to_remove:

                    scheduled = scheduled.drop(
                        rows_to_remove
                    )

                    scheduled.to_csv(
                        scheduled_file,
                        index=False
                    )

        time.sleep(30)

    except Exception as e:

        print(
            "Error:",
            e
        )

        time.sleep(30)
