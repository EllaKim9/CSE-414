/*22 row*/
SELECT c.name AS name, SUM(f.departure_delay) AS delay
	FROM Carriers AS c, Flights AS f
	WHERE c.cid = f.carrier_id
	GROUP BY c.name;


