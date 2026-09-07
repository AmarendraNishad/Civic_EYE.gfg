import csv
import os
from datetime import datetime

LOG_FILE = "incidents/incident_log.csv"


def log_incident(vehicle_id, duration, image_path):

    os.makedirs("incidents", exist_ok=True)

    file_exists = os.path.exists(LOG_FILE)

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Vehicle ID",
                "Duration (seconds)",
                "Status",
                "Snapshot"
            ])

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            vehicle_id,
            round(duration, 2),
            "CRITICAL",
            image_path
        ])