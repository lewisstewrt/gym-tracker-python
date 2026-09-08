import os
from models import Workout

def load_workouts():
    workouts = []
    if os.path.exists("workouts.csv"):
        with open("workouts.csv","r") as f:
            for line in f:
                if line.strip():
                    exercise, sets, reps, weight, timestamp = line.strip().split(",")
                    workout = Workout(exercise, sets, reps, weight, timestamp)
                    workouts.append(workout)
    return workouts

# FUNCTION TO SAVE WORKOUTS TO CSV
def save_Workout(workout):
    with open("workouts.csv", "a") as f:
            f.write(f"{workout.exercise},{workout.sets},{workout.reps},{workout.weight},{workout.timestamp}\n")
