--Q4

SELECT DISTINCT f2.dest_city AS city
FROM Flights AS f1, Flights AS f2
WHERE f1.origin_city = 'Seattle WA' AND
f1.dest_city = f2.origin_city AND 
f2.dest_city != 'Seattle WA' AND
f1.dest_city != 'Seattle WA' AND
f2.dest_city NOT IN 
	(SELECT DISTINCT f3.dest_city 
	FROM Flights AS f3
	WHERE f3.origin_city = 'Seattle WA')
ORDER BY city ASC;


/*# of rows returned: 256
Run-time: 10 seconds
First 20 rows of result:  
Aberdeen SD
Abilene TX
Adak Island AK
Aguadilla PR
Akron OH
Albany GA
Albany NY
Alexandria LA
Allentown/Bethlehem/Easton PA
Alpena MI
Amarillo TX
Appleton WI
Arcata/Eureka CA
Asheville NC
Ashland WV
Aspen CO
Atlantic City NJ
Augusta GA
Bakersfield CA
Bangor ME
*/