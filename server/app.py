from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import (
    exercise_schema,
    exercises_schema,
    workout_schema,
    workouts_schema,
    workout_exercise_schema,
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404
    return jsonify(workout_schema.dump(workout)), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
        workout = Workout(**data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 422
    except ValueError as err:
        return jsonify({'errors': str(err)}), 422

    db.session.add(workout)
    db.session.commit()
    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if workout is None:
        return jsonify({'error': 'Workout not found'}), 404

    db.session.delete(workout)
    db.session.commit()
    return '', 204


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404
    return jsonify(exercise_schema.dump(exercise)), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
        exercise = Exercise(**data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 422
    except ValueError as err:
        return jsonify({'errors': str(err)}), 422

    try:
        db.session.add(exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'An exercise with that name already exists'}), 409
    return jsonify(exercise_schema.dump(exercise)), 201


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    db.session.delete(exercise)
    db.session.commit()
    return '', 204


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if workout is None or exercise is None:
        return jsonify({'error': 'Workout or exercise not found'}), 404

    try:
        data = workout_exercise_schema.load(request.get_json())
        workout_exercise = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
    except ValidationError as err:
        return jsonify({'errors': err.messages}), 422
    except ValueError as err:
        return jsonify({'errors': str(err)}), 422

    try:
        db.session.add(workout_exercise)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'This exercise is already in this workout'}), 409
    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201


if __name__ == '__main__':
    app.run(port=5555, debug=True)
