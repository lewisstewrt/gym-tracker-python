from datetime import datetime

# WORKOUT CLASS TO HOLD ALL VALUES IN ONE OBJECT
class Workout:
    def __init__(self, exercise, sets, reps, weight, timestamp=None):
        self.exercise = exercise
        self.sets = int(sets)
        self.reps = int(reps)
        self.weight = float(weight)
        self.timestamp = timestamp or datetime.now().strftime("%d/%m/%Y %H:%M")

    def __str__(self):
        return f"{self.exercise} - {self.sets}x{self.reps} @ {self.weight}kg - {self.timestamp}"