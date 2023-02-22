drop table if exists workoutexercises;
drop table if exists workout;
Drop table IF exists Exercise;
Create Table if not Exists Exercise(
    exercise_id Serial primary key,
    exercise_name text
);
Create Table if not Exists Workout (
    workout_id Serial Primary Key,
    workout_date DATE
);
Commit;
Create Table if not Exists WorkoutExercises (
    id Serial Primary Key,
    workout_id INT References Workout(workout_id),
    Exercise_id INT References Exercise(Exercise_Id)
);

INSERT INTO exercise (exercise_name) VALUES ('Squat'),
('Leg Press'),
('Leg Extension'),
('Calf Press'),
('Incline press');

INSERT INTO workout (workout_date) VALUES ('22-12-10');
SELECT * FROM workout;
SELECT * FROM exercise;
INSERT INTO workoutexercises (workout_id, exercise_id) Values 
(1,2),
(1,3),
(1,4);

drop table if exists session;
drop table if exists session_name;
create table if not exists session_name (
    session_id SERIAL PRIMARY KEY,
    name VARCHAR(80)
);
CREATE TABLE IF NOT EXISTS session (
    session_id INT REFERENCES session_name(session_id),
    exercise_id INT REFERENCES exercise(exercise_id)
);
-- INSERT INTO exercise (exercise_name) VALUES
-- ('Pec Deck'),
-- ('Lat Pulldowns'),
-- ('Deadlift');
INSERT INTO session_name (name)
VALUES ('Chest and back day');
INSERT INTO session (session_id, exercise_id) VALUES
(1,6),
(1,5),
(1,7),
(1,8);