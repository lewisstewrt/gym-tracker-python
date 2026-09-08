# Gym Tracker (Python)

A command-line fitness tracking application for logging, storing, and analysing workout data over time.
Built as a personal portfolio project to practise Python fundamentals, object-oriented design, and data persistence, with the goal of evolving into a small predictive analytics tool.

---

## Features

- Log multi-exercise workout sessions in a single pass
- Automatic session timestamp grouping for cleaner history views
- Persistent storage via CSV, with plans to migrate to SQLite
- Search workouts by exercise name, with case-insensitive partial matching
- Input validation and error handling throughout
- Clean, formatted console interface

---

## Example Output
========================================================
WORKOUT HISTORY
[09/02/2026 12:02]

Bench Press — 3x12 @ 100.0kg
Pec Dec — 3x12 @ 50.0kg
Tricep Pushdown — 3x12 @ 45.0kg


---

## Technologies Used

- Python
- Object-Oriented Programming (OOP)
- File Handling (CSV, moving to SQLite)
- Console UI Formatting

---

## Project Purpose

This project exists to:

- Build real, applied Python skills beyond tutorials — structuring, persisting, and querying real data
- Practise software design decisions as the project grows (e.g. refactoring from a single script into modules)
- Serve as a foundation for a small machine learning feature: predicting future strength trends from logged workout history
- Produce a portfolio-ready application that reflects iterative, real-world development rather than a one-off exercise

---

## Planned Improvements

- [ ] Refactor into separate modules (models, storage, interface)
- [ ] Migrate from CSV to SQLite
- [ ] Edit and delete workout entries
- [ ] Session analytics and volume tracking
- [ ] Linear regression model to predict future strength/weight progression from logged history
- [ ] Progress visualisation (charts)
- [ ] (Stretch) Simple GUI or web interface

---

## Installation & Usage

1. Clone the repository:
