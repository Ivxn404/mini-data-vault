from flask import Flask, jsonify, request
from flask_cors import CORS

from models import User, Workout, WorkoutType, NutritionLog, SleepLog, MoodLog
from ai_insights import generate_insights
import uuid

app = Flask(__name__)
CORS(app)

# In-memory store for demo; replace with DB in real app
users = {}

# Helper to fetch user or create dummy user for demo
def get_or_create_user(user_id="demo_user"):
    if user_id not in users:
        users[user_id] = User(user_id=user_id, username="Demo User", email="demo@example.com")
    return users[user_id]

@app.route("/api/user", methods=["GET"])
def get_user():
    user = get_or_create_user()
    return jsonify({
        "userId": user.user_id,
        "username": user.username,
        "email": user.email,
    })

@app.route("/api/workouts", methods=["GET", "POST"])
def workouts():
    user = get_or_create_user()
    if request.method == "GET":
        workouts_data = [
            {
                "workoutId": w.workout_id,
                "type": w.workout_type.value,
                "durationMinutes": w.duration_minutes,
                "caloriesBurned": w.calories_burned,
                "date": w.date.isoformat(),
            } for w in user.workouts
        ]
        return jsonify(workouts_data)
    else:
        data = request.get_json()
        workout = Workout(
            workout_id=str(uuid.uuid4()),
            workout_type=WorkoutType[data.get("type")],
            duration_minutes=data.get("durationMinutes", 0),
            calories_burned=data.get("caloriesBurned", 0),
        )
        user.workouts.append(workout)
        return jsonify({"message": "Workout added", "workoutId": workout.workout_id})

@app.route("/api/nutrition", methods=["GET", "POST"])
def nutrition():
    user = get_or_create_user()
    if request.method == "GET":
        nutrition_data = [
            {
                "logId": n.log_id,
                "calories": n.calories,
                "proteinGrams": n.protein_grams,
                "carbsGrams": n.carbs_grams,
                "fatsGrams": n.fats_grams,
                "date": n.date.isoformat(),
            } for n in user.nutrition_logs
        ]
        return jsonify(nutrition_data)
    else:
        data = request.get_json()
        nutrition_log = NutritionLog(
            log_id=str(uuid.uuid4()),
            calories=data.get("calories", 0),
            protein_grams=data.get("proteinGrams", 0),
            carbs_grams=data.get("carbsGrams", 0),
            fats_grams=data.get("fatsGrams", 0),
        )
        user.nutrition_logs.append(nutrition_log)
        return jsonify({"message": "Nutrition log added", "logId": nutrition_log.log_id})

@app.route("/api/sleep", methods=["GET", "POST"])
def sleep():
    user = get_or_create_user()
    if request.method == "GET":
        sleep_data = [
            {
                "logId": s.log_id,
                "hoursSlept": s.hours_slept,
                "sleepQuality": s.sleep_quality,
                "date": s.date.isoformat(),
            } for s in user.sleep_logs
        ]
        return jsonify(sleep_data)
    else:
        data = request.get_json()
        sleep_log = SleepLog(
            log_id=str(uuid.uuid4()),
            hours_slept=data.get("hoursSlept", 0),
            sleep_quality=data.get("sleepQuality", 0),
        )
        user.sleep_logs.append(sleep_log)
        return jsonify({"message": "Sleep log added", "logId": sleep_log.log_id})

@app.route("/api/mood", methods=["GET", "POST"])
def mood():
    user = get_or_create_user()
    if request.method == "GET":
        mood_data = [
            {
                "logId": m.log_id,
                "moodLevel": m.mood_level,
                "notes": m.notes,
                "date": m.date.isoformat(),
            } for m in user.mood_logs
        ]
        return jsonify(mood_data)
    else:
        data = request.get_json()
        mood_log = MoodLog(
            log_id=str(uuid.uuid4()),
            mood_level=data.get("moodLevel", 0),
            notes=data.get("notes", ""),
        )
        user.mood_logs.append(mood_log)
        return jsonify({"message": "Mood log added", "logId": mood_log.log_id})

@app.route("/api/insights", methods=["GET"])
def insights():
    user = get_or_create_user()
    # Generate insights based on user data
    ai_result = generate_insights(user)
    return jsonify(ai_result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
