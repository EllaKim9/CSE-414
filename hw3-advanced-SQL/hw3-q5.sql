--Q5

SELECT DISTINCT fin.dest_city AS city
FROM Flights as fin
WHERE fin.dest_city NOT IN 
	(SELECT DISTINCT f2.dest_city
	FROM Flights AS f1, Flights AS f2
	WHERE f1.origin_city = 'Seattle WA' AND
	f1.dest_city = f2.origin_city AND 
	f2.dest_city != 'Seattle WA' AND
	f1.dest_city != 'Seattle WA' AND
	f2.dest_city NOT IN 
		(SELECT DISTINCT f3.dest_city 
		FROM Flights AS f3
		WHERE f3.origin_city = 'Seattle WA')
	) AND
	fin.dest_city NOT IN 
		(SELECT DISTINCT f3.dest_city 
		FROM Flights AS f3
		WHERE f3.origin_city = 'Seattle WA')
ORDER BY city ASC;


/*# of rows returned: 4
Run-time: 34 seconds
The 4 rows of result:  
Devils Lake ND
Hattiesburg/Laurel MS
Seattle WA
St. Augustine FL
*/