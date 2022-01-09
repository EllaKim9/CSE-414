--Q3

SELECT cr.city AS origin_city, ISNULL(100.0*cl.coun/cr.more_three,0) AS perc
FROM 
	(SELECT fli.origin_city AS city, COUNT(fli.actual_time) as more_three
	FROM Flights AS fli
	WHERE fli.canceled = 0
	GROUP BY fli.origin_city) cr
	LEFT OUTER JOIN
	(SELECT fl.origin_city, COUNT(fl.actual_time) as coun
	FROM Flights as fl 
	WHERE fl.actual_time < 180
	GROUP BY fl.origin_city) cl
ON cr.city = cl.origin_city
ORDER BY perc, origin_city ASC;

/*# of rows returned: 327
Run-time: 12 seconds
First 20 rows of result:  
Guam TT    0.000000000000
Pago Pago TT    0.000000000000
Aguadilla PR    29.657794676806
Anchorage AK    32.304250559284
San Juan PR    34.008179959100
Charlotte Amalie VI    40.294117647058
Ponce PR    42.622950819672
Fairbanks AK    51.282051282051
Kahului HI    53.839338452451
Honolulu HI    55.115554401454
San Francisco CA    56.924691070179
Los Angeles CA    57.286573659285
Seattle WA    57.955062312380
Long Beach CA    62.916006339144
Kona HI    63.491189427312
New York NY    65.410530240485
Las Vegas NV    65.617081532270
Christiansted VI    65.771812080536
Worcester MA    68.852459016393
San Diego CA    69.178128599498
*/