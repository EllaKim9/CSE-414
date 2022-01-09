/*12 rows*/
SELECT DISTINCT c.name AS name
	FROM Carriers AS c, Flights AS f
	WHERE c.cid = f.carrier_id
	GROUP BY f.day_of_month, f.day_of_week_id, c.name
	HAVING COUNT(name)  >  1000;

