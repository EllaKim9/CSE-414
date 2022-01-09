--Q7

SELECT DISTINCT c.name AS carrier
FROM Flights as f, Carriers as c 
WHERE c.cid = f.carrier_id AND 
f.origin_city = 'Seattle WA' AND 
f.dest_city = 'San Francisco CA'
ORDER BY carrier ASC;


/*# of rows returned: 4
Run-time: 1 second (faster than nested query like lectures state)
The 4 rows of result:  
Alaska Airlines Inc.
SkyWest Airlines Inc.
United Air Lines Inc.
Virgin America
*/