import csv
from datetime import datetime

from db import create_tables, get_connection, create_session, get_or_create_exercise, add_set

CSV_PATH = "workouts.csv"

def convert_timestamp(old):
    return datetime.strptime(old, "%d/%m/%Y %H:%M").isoformat(timespec="minutes")


def migrate():
    create_tables()

    with get_connection() as conn:
        existing = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        if existing > 0:
            print("Database already has data, migration skipped.")
            return

        session_ids = {}
        rows_moved = 0

        with open(CSV_PATH, newline="") as f:
            for row in csv.reader(f):
                if not row:
                    continue
                exercise, sets, reps, weight_kg, timestamp = row

                if timestamp not in session_ids:
                    session_ids[timestamp] = create_session(conn, convert_timestamp(timestamp))
                session_id = session_ids[timestamp]

                exercise_id = get_or_create_exercise(conn, exercise)

                for set_number in range(1,int(sets)+1):
                    add_set(conn, session_id, exercise_id, set_number, int(reps),float(weight_kg))
                    


                rows_moved += 1
    print(f"Moved {rows_moved} rows into {len(session_ids)} sessions.")


if __name__ == "__main__":
    migrate()


