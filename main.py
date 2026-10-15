from datetime import datetime
from models import Workout
from storage import load_workouts, save_Workout
from db import get_connection, get_all_sets

workouts = load_workouts()

#  HEADER / UI FORMATTING
def print_Header(title):
    width = 56
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


# FUNCTION TO LOG EACH WORKOUT
def log_Workout():

    session_Timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")

    try:
        num_Of_Exercises = int(input("Enter number of exercises done: "))

    except ValueError:
        print("Please enter a valid number.")
        return

    for i in range(num_Of_Exercises):

        while True:
            try:
                exercise = input("Enter exercise: ").strip()
                sets = int(input("Enter number of sets: "))
                reps = int(input("Enter number of reps: "))
                weight = float(input("Enter weight: "))

            except ValueError:
                print("Invalid input — numbers only. Try again.\n")
                continue

            if not exercise:
                print("Exercise name cant be empty.\n")
                continue

            workout = Workout(exercise, sets, reps, weight, session_Timestamp)
            workouts.append(workout)
            save_Workout(workout)
            break

    print_Header("Workout successfully logged!")

#FUNCTION TO DISPLAY ALL WORKOUTS LOGGED
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
            print(f"[{date}]")
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



#MENU FUNCTION TO DISPLAY USER MENU
def menu():
    while True:
        print_Header("WELCOME TO THE GYM TRACKER")

        print("1) Log workout")
        print("2) View workouts")
        print("3) Search workouts")
        print("4) Exit")

        choice = input("\nEnter choice --> ").strip()

        if choice == "1":
            log_Workout()
            
        elif choice == "2":
            view_Workouts()
        
        elif choice == "3":
            search_Workouts()
        
        elif choice == "4":
            print_Header("Application closing...")
            break

        else:
            print("\nInvalid choice, please try again.\n")


menu()
