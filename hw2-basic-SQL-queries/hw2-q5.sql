/*6 rows*/
SELECT c.name AS name, (AVG(f.canceled)*100.0) AS percentage
	FROM Carriers AS c, Flights AS f
	WHERE c.cid = f.carrier_id AND 
	f.origin_city = 'Seattle WA'
	GROUP BY c.name
	HAVING (percentage > 0.5)
	ORDER BY percentage ASC;

