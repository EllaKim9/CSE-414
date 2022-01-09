--Q6

SELECT DISTINCT c.name AS carrier
FROM Carriers as c 
WHERE c.cid IN 
	(SELECT f.carrier_id 
	FROM Flights as f
	WHERE f.origin_city = 'Seattle WA' AND 
	f.dest_city = 'San Francisco CA')
ORDER BY carrier ASC;

/*# of rows returned: 4
Run-time: 2 seconds
The 4 rows of result:  
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America
*/