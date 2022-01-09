/*1 row*/
SELECT SUM(f.capacity) AS capacity
	FROM Months AS m, Flights AS f 
	WHERE m.mid = f.month_id AND
	m.month = 'July' AND
	f.day_of_month = 10 AND 
	(
	(f.origin_city = 'Seattle WA' AND 
	f.dest_city = 'San Francisco CA') OR
	(f.origin_city = 'San Francisco CA' AND 
	f.dest_city = 'Seattle WA')
	);

