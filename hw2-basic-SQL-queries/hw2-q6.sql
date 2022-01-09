/*3 rows*/
SELECT c.name AS carrier, MAX(f.price) AS max_price
	FROM Carriers AS c, Flights AS f
	WHERE c.cid = f.carrier_id AND
	(
	(f.origin_city = 'Seattle WA' AND f.dest_city = 'New York NY') OR
	(f.origin_city = 'New York NY' AND f.dest_city = 'Seattle WA')
	)
	GROUP BY c.name;

