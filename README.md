# Workout Tracker API

A Flask REST API for a workout tracking application used by personal trainers. It tracks workouts and the exercises performed in them, with the sets, reps or duration recorded for each exercise. Exercises are reusable, so the same exercise can be added to many workouts.

Built with Flask, Flask-SQLAlchemy, Flask-Migrate, Marshmallow and SQLite.

## Data Model

- **Exercise**: `id`, `name` (unique), `category`, `equipment_needed`
- **Workout**: `id`, `date`, `duration_minutes`, `notes`
- **WorkoutExercise** (join table): `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds`

A workout has many exercises through WorkoutExercises, and an exercise has many workouts through WorkoutExercises.

## Validations

| Type | Examples |
| --- | --- |
| Table constraints | unique exercise name; `duration_minutes > 0`; reps, sets and duration must be positive; an exercise can only be added once to a workout; at least one of `reps` or `duration_seconds` is required |
| Model validations | exercise name and category cannot be blank; `duration_minutes` must be a positive integer; notes limited to 500 characters; reps, sets and duration must be positive integers |
| Schema validations | required fields; length limits; `duration_minutes` between 1 and 600; valid date format; reps, sets and duration at least 1; reps or duration required |

## Installation

Requires Python 3.8 to 3.13 (Flask 2.2.2 does not work on Python 3.14 or newer) and [Pipenv](https://pipenv.pypa.io/).

```bash
git clone https://github.com/masuuddev/workout-api.git
cd workout-api
pipenv install
pipenv shell
cd server
flask db upgrade head
python seed.py
```

`flask db upgrade head` creates the database tables from the included migrations. `python seed.py` clears the tables and adds example data. It can be run again at any time to reset the data.

## Running the App

From the `server` folder:

```bash
flask run --port 5555
```

The API is available at `http://localhost:5555`.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show one workout with its exercises, including reps, sets and duration |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its associated WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show one exercise and the workouts it appears in |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its associated WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps, sets and duration |

### Example request bodies

Create a workout (`POST /workouts`):

```json
{ "date": "2026-11-02", "duration_minutes": 45, "notes": "Leg day" }
```

Create an exercise (`POST /exercises`):

```json
{ "name": "Lunges", "category": "Strength", "equipment_needed": false }
```

Add an exercise to a workout (`POST /workouts/1/exercises/2/workout_exercises`):

```json
{ "reps": 12, "sets": 3 }
```

For a timed exercise, send `duration_seconds` instead of `reps`, for example `{ "duration_seconds": 60, "sets": 3 }`.

### Response status codes

- `200` success, `201` created, `204` deleted with no content
- `404` workout or exercise not found
- `409` duplicate exercise name, or exercise already in that workout
- `422` invalid data (the response lists which fields are wrong)

## Project Structure

```
server/
  app.py       routes
  models.py    database models, constraints and validations
  schemas.py   Marshmallow schemas and schema validations
  seed.py      example data
  migrations/  database migrations
Pipfile
README.md
```
