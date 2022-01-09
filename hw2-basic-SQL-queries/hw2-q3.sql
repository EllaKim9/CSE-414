/*1 row: Friday,14.4725010477787*/
SELECT w.day_of_week AS day_of_week, AVG(f.arrival_delay) AS delay
	FROM Weekdays AS w, Flights AS f
	WHERE w.did = f.day_of_week_id
	GROUP BY w.day_of_week
	ORDER BY AVG(f.arrival_delay) DESC
	LIMIT 1;

