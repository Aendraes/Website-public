
with sub as (SELECT e.exercise_name, we.repetitions, we.weight, 
we.weight * (1 + 0.0333 * we.repetitions ) AS onerm from workoutexercises we
join exercise e on e.exercise_id = we.exercise_id
group by e.exercise_name, we.repetitions, we.weight),
sub2 as (select exercise_name, max(onerm) from sub
group by exercise_name)
SELECT e.exercise_name, sub.repetitions, sub.weight from exercise e
 JOIN sub2 ON sub2.exercise_name = e.exercise_name
left JOIN sub on sub2.max = sub.onerm;

Create TAble session_backup AS session;