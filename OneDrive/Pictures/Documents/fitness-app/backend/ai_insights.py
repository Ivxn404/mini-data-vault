import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def generate_insights(user):
    """Generate simple AI-driven insights based on historical user data."""

    insights = {}

    # Insight 1: Workout trend (duration over time)
    workouts = sorted(user.workouts, key=lambda w: w.date)
    if len(workouts) >= 2:
        dates = np.array([(w.date - workouts[0].date).days for w in workouts]).reshape(-1, 1)
        durations = np.array([w.duration_minutes for w in workouts])
        model = LinearRegression().fit(dates, durations)
        trend = model.coef_[0]
        if trend > 0:
            insights['workoutTrend'] = f"Your workout duration is increasing by {trend:.2f} minutes per day."
        elif trend < 0:
            insights['workoutTrend'] = f"Your workout duration is decreasing by {abs(trend):.2f} minutes per day."
        else:
            insights['workoutTrend'] = "Your workout duration is stable."

    else:
        insights['workoutTrend'] = "Not enough workout data to determine a trend."

    # Insight 2: Average sleep quality
    sleep_logs = user.sleep_logs
    if sleep_logs:
        avg_quality = np.mean([s.sleep_quality for s in sleep_logs])
        insights['averageSleepQuality'] = f"Your average sleep quality is {avg_quality:.1f} out of 10."
    else:
        insights['averageSleepQuality'] = "No sleep data available."

    # Insight 3: Nutrition balance (simple ratio of macros)
    nutrition_logs = user.nutrition_logs
    if nutrition_logs:
        avg_protein = np.mean([n.protein_grams for n in nutrition_logs])
        avg_carbs = np.mean([n.carbs_grams for n in nutrition_logs])
        avg_fats = np.mean([n.fats_grams for n in nutrition_logs])
        insights['nutritionBalance'] = f"Avg macros: Protein {avg_protein:.1f}g, Carbs {avg_carbs:.1f}g, Fats {avg_fats:.1f}g."
    else:
        insights['nutritionBalance'] = "No nutrition data available."

    # Insight 4: Mood pattern (average mood level)
    mood_logs = user.mood_logs
    if mood_logs:
        avg_mood = np.mean([m.mood_level for m in mood_logs])
        insights['averageMood'] = f"Your average mood level is {avg_mood:.1f} out of 10."
    else:
        insights['averageMood'] = "No mood data available."
    
    return insights
