from datetime import datetime
from models import Workout
from storage import load_workouts, save_Workout
from db import get_connection, get_all_sets, create_session, get_or_create_exercise, add_set, deleteSession

workouts = load_workouts()


# HEADER / UI FORMATTING
def print_Header(title):
    width = 56
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


# FUNCTION TO LOG EACH WORKOUT
def log_Workout():
    print_Header("Log Workout")
    new_Exercises = []

    try:
        num_Of_Exercises = int(input("Enter number of exercises: "))
    except ValueError:
        print("Input must be a whole number.\n")
        return

    for i in range(num_Of_Exercises):
        exercise_Name = input("Enter exercise name: ").strip()

        while True:
            try:
                num_Of_Sets = int(input("Enter number of sets: "))
            except ValueError:
                print("Input must be a whole number.")
                continue
            break

        exercise_Sets = []
        for set_num in range(1, num_Of_Sets + 1):
            while True:
                try:
                    reps = int(input(f"  Set {set_num} reps: "))
                    weight = float(input(f"  Set {set_num} weight (kg): "))
                except ValueError:
                    print("Invalid input, try that set again.")
                    continue
                break
            exercise_Sets.append((reps, weight))

        new_Exercises.append((exercise_Name, exercise_Sets))

    if not new_Exercises:
        print("No exercises entered.\n")
        return

    with get_connection() as conn:
        started_at = datetime.now().isoformat(timespec="minutes")
        session_id = create_session(conn, started_at)

        for name, sets in new_Exercises:
            exercise_id = get_or_create_exercise(conn, name)
            for set_number, (reps, weight) in enumerate(sets, start=1):
                add_set(conn, session_id, exercise_id, set_number, reps, weight)

    print_Header("Workout successfully logged.")


# FUNCTION TO DISPLAY ALL WORKOUTS LOGGED
def view_Workouts():
    with get_connection() as conn:
        rows = get_all_sets(conn)

    if not rows:
        print("No workouts logged, get to work!\n")
        return

    print_Header("WORKOUT HISTORY")

    current_Session = None
    current_Exercise = None

    for row in rows:
        if row["session_id"] != current_Session:
            if current_Session is not None:
                print()

            current_Session = row["session_id"]
            current_Exercise = None
            date = datetime.fromisoformat(row["started_at"]).strftime("%d/%m/%Y %H:%M")
            print(f"Session ID:{row['session_id']}, [{date}]")
            print("-" * 56)

        if row["name"] != current_Exercise:
            current_Exercise = row["name"]
            print(current_Exercise)

        print(f"   Set {row['set_number']}: {row['reps']} reps @ {row['weight_kg']}kg")

    print()


def search_Workouts():
    print_Header("Search Workouts")
    query = input("Search exercise name: ").strip().lower()

    if not query:
        print("Search cant be empty\n")
        return

    with get_connection() as conn:
        rows = get_all_sets(conn, query)

    if not rows:
        print("No results.\n")
        return

    print_Header("Search Results")

    current_Session = None
    current_Exercise = None

    for row in rows:
        if row["session_id"] != current_Session:
            if current_Session is not None:
                print()

            current_Session = row["session_id"]
            current_Exercise = None
            date = datetime.fromisoformat(row["started_at"]).strftime("%d/%m/%Y %H:%M")
            print(f"[{date}]")
            print("-" * 56)

        if row["name"] != current_Exercise:
            current_Exercise = row["name"]
            print(current_Exercise)

        print(f"   Set {row['set_number']}: {row['reps']} reps @ {row['weight_kg']}kg")

    print()


# Delete a session
def delete_session_menu():
    with get_connection() as conn:
        rows = get_all_sets(conn)

    if not rows:
        print("Nothing to delete.")
        return

    view_Workouts()

    try:
        sessionId = int(input("Enter session id to delete: "))
    except ValueError:
        print("Session ID must be integer.")
        return

    print(f"Are you sure you want to delete session {sessionId}?\n")
    confirmation = input("(y) or (n)").strip().lower()

    if confirmation == "y":
        with get_connection() as conn:
            deleted_session = deleteSession(conn, sessionId)
    elif confirmation == "n":
        print("Cancelling deletion...")
        return
    else:
        print("Invalid entry, cancelling deletion...")
        return

    if deleted_session == True:
        print("Session deleted.")
    else:
        print("No session with that ID, please try again.")


# MENU FUNCTION TO DISPLAY USER MENU
def menu():
    while True:
        print_Header("WELCOME TO THE GYM TRACKER")

        print("1) Log workout")
        print("2) View workouts")
        print("3) Search workouts")
        print("4) Delete session")
        print("5) Exit")

        choice = input("\nEnter choice --> ").strip()

        if choice == "1":
            log_Workout()

        elif choice == "2":
            view_Workouts()

        elif choice == "3":
            search_Workouts()

        elif choice == "4":
            delete_session_menu()

        elif choice == "5":
            print_Header("Application closing...")
            break

        else:
            print("\nInvalid choice, please try again.\n")


menu()
