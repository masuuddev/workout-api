#!/usr/bin/env python3

from datetime import date, timedelta

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing existing data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    exercises = [
        Exercise(name='Push-ups', category='Strength', equipment_needed=False),
        Exercise(name='Squats', category='Strength', equipment_needed=False),
        Exercise(name='Deadlift', category='Strength', equipment_needed=True),
        Exercise(name='Plank', category='Core', equipment_needed=False),
        Exercise(name='Running', category='Cardio', equipment_needed=False),
        Exercise(name='Rowing Machine', category='Cardio', equipment_needed=True),
    ]
    db.session.add_all(exercises)
    db.session.commit()
    pushups, squats, deadlift, plank, running, rowing = exercises

    print('Seeding workouts...')
    today = date.today()
    workouts = [
        Workout(date=today - timedelta(days=4), duration_minutes=45,
                notes='Upper and lower body strength.'),
        Workout(date=today - timedelta(days=2), duration_minutes=30,
                notes='Cardio and core.'),
        Workout(date=today, duration_minutes=60, notes=None),
    ]
    db.session.add_all(workouts)
    db.session.commit()
    strength, cardio, full_body = workouts

    print('Seeding workout exercises...')
    db.session.add_all([
        WorkoutExercise(workout=strength, exercise=pushups, reps=15, sets=3),
        WorkoutExercise(workout=strength, exercise=squats, reps=12, sets=4),
        WorkoutExercise(workout=strength, exercise=deadlift, reps=5, sets=5),
        WorkoutExercise(workout=cardio, exercise=running, duration_seconds=1200),
        WorkoutExercise(workout=cardio, exercise=plank, sets=3, duration_seconds=60),
        WorkoutExercise(workout=full_body, exercise=squats, reps=10, sets=3),
        WorkoutExercise(workout=full_body, exercise=rowing, duration_seconds=900),
        WorkoutExercise(workout=full_body, exercise=plank, sets=3, duration_seconds=45),
    ])
    db.session.commit()

    print('Done seeding!')
