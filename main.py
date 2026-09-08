from datetime import datetime
import os
from models import Workout

workouts = []

if os.path.exists("workouts.csv"):
    with open("workouts.csv","r") as f:
        for line in f:
            if line.strip():
                exercise, sets, reps, weight, timestamp = line.strip().split(",")
                workout = Workout(exercise, sets, reps, weight, timestamp)
                workouts.append(workout)



#  HEADER / UI FORMATTING
def print_Header(title):
    width = 56
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width + "\n")


# FUNCTION TO SAVE WORKOUTS TO CSV
def save_Workout(workout):
    with open("workouts.csv", "a") as f:
            f.write(f"{workout.exercise},{workout.sets},{workout.reps},{workout.weight},{workout.timestamp}\n")


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
    if not workouts:
        print("No workouts logged, get to work!\n")
        return

    print_Header("WORKOUT HISTORY")

    current_Timestamp = None

    for w in workouts:
        if w.timestamp != current_Timestamp:
            if current_Timestamp is not None:
                print()
                
            current_Timestamp = w.timestamp
            print(f"[{current_Timestamp}]")
            print("-" * 56)

        print(f"{w.exercise:<25} - {w.sets}x{w.reps} @ {w.weight}kg")
    
    print()



def search_Workouts():
    print_Header("Search Workouts")
    query = input("Search exercise name: ").strip().lower()

    if not query:
        print("Search cant be empty\n")
        return
    
    matches = [w for w in workouts if query in w.exercise.lower()]

    if not matches:
        print("No results.\n")
        return
    
    print_Header("Search Results")

    current_Timestamp = None

    for w in matches:
        if w.timestamp != current_Timestamp:
            print(f"{w.timestamp}")
            current_Timestamp = w.timestamp
        
        print(f"{w.exercise} - {w.sets}x{w.reps} @ {w.weight}kg")
    
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
