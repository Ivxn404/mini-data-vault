from datetime import datetime
from enum import Enum

class User:
    def __init__(self, user_id, username, email):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.workouts = []
        self.nutrition_logs = []
        self.sleep_logs = []
        self.mood_logs = []

class WorkoutType(Enum):
    CARDIO = "Cardio"
    STRENGTH = "Strength"
    FLEXIBILITY = "Flexibility"
    BALANCE = "Balance"

class Workout:
    def __init__(self, workout_id, workout_type, duration_minutes, calories_burned, date=None):
        self.workout_id = workout_id
        self.workout_type = workout_type
        self.duration_minutes = duration_minutes
        self.calories_burned = calories_burned
        self.date = date or datetime.now()

class NutritionLog:
    def __init__(self, log_id, calories, protein_grams, carbs_grams, fats_grams, date=None):
        self.log_id = log_id
        self.calories = calories
        self.protein_grams = protein_grams
        self.carbs_grams = carbs_grams
        self.fats_grams = fats_grams
        self.date = date or datetime.now()

class SleepLog:
    def __init__(self, log_id, hours_slept, sleep_quality, date=None):
        self.log_id = log_id
        self.hours_slept = hours_slept
        self.sleep_quality = sleep_quality  # scale 1-10
        self.date = date or datetime.now()

class MoodLog:
    def __init__(self, log_id, mood_level, notes, date=None):
        self.log_id = log_id
        self.mood_level = mood_level  # scale 1-10
        self.notes = notes
        self.date = date or datetime.now()
