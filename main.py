from datetime import datetime
from models import Workout
from storage import load_workouts, save_Workout
from db import get_connection, get_all_sets, create_session, get_or_create_exercise, add_set

workouts = load_workouts()

#  HEADER / UI FORMATTING
def print_Header(title):
    width = 56
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


# FUNCTION TO LOG EACH WORKOUT
def log_Workout():
    print_Header("Log Workout")
    new_Exercises = []
    # 1. Ask how many exercises (or ask until they type 'done')
    
    try:
        num_Of_Exercises = int(input("Enter number of exercises: "))
    except ValueError:
        print("Input must be integer.\n")
        return 
    # 2. For each exercise: ask the name, then sets, reps and weight
    #    (collect these into a list first; don't save yet)
    for i in range(num_Of_Exercises):
        while True:
            try:
                exercise_Name = input("Enter exercise name: ").strip()
                num_of_Sets = int(input("Enter number of sets: "))
                num_of_reps = int(input("Enter number of reps: "))
                weight = float(input("Enter weight (Kg): "))
            except ValueError:
                print("Invalid entry.")
                continue
            break

        new_Exercises.append((exercise_Name, num_of_Sets, num_of_reps, weight))

    if not new_Exercises:
         print("No exercises entered.\n")
         return

  

    # 4. Open the database connection
    with get_connection() as conn:
    # 5. Create ONE session with the current time and keep its id
            started_at = datetime.now().isoformat(timespec="minutes")
            session_id = create_session(conn, started_at)

            for name, sets, reps, weight in new_Exercises:
                exercise_id = get_or_create_exercise(conn, name)
                for set_number in range(1, sets+1):
                    add_set(conn, session_id, exercise_id, set_number, reps, weight)

    print_Header("Workout successfuly logged.")    
    # 6. For each exercise in your list:
    #       get its exercise id
    #       add a row for every set
    # 7. Print the success header

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
