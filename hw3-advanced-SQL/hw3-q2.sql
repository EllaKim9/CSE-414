--Q2

WITH CityMax AS
	(SELECT fl.origin_city, MAX(fl.actual_time) AS max_time 
	FROM Flights AS fl
	GROUP BY fl.origin_city)
SELECT DISTINCT f.origin_city AS city
FROM Flights AS f, CityMax AS cm
WHERE f.origin_city = cm.origin_city AND cm.max_time < 180 AND f.canceled = 0
ORDER BY f.origin_city ASC;


/*# of rows returned: 109
Run-time: 48
First 20 rows of result:
Aberdeen SD
Abilene TX
Alpena MI
Ashland WV
Augusta GA
Barrow AK
Beaumont/Port Arthur TX
Bemidji MN
Bethel AK
Binghamton NY
Brainerd MN
Bristol/Johnson City/Kingsport TN
Butte MT
Carlsbad CA
Casper WY
Cedar City UT
Chico CA
College Station/Bryan TX
Columbia MO
Columbus GA  
*/