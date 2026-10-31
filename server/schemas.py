from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    workouts = fields.List(
        fields.Nested('WorkoutSchema', only=('id', 'date', 'duration_minutes', 'notes')),
        dump_only=True,
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=600))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))

    workout_exercises = fields.List(
        fields.Nested('WorkoutExerciseSchema', exclude=('workout_id',)),
        dump_only=True,
    )


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    exercise = fields.Nested(
        ExerciseSchema, only=('id', 'name', 'category', 'equipment_needed'), dump_only=True
    )

    @validates_schema
    def require_reps_or_duration(self, data, **kwargs):
        if data.get('reps') is None and data.get('duration_seconds') is None:
            raise ValidationError('Provide at least one of reps or duration_seconds.', field_name='reps')


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workouts',))
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
workout_exercise_schema = WorkoutExerciseSchema()
