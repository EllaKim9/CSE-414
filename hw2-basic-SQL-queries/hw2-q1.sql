/*3 rows*/
SELECT DISTINCT f.flight_num AS flight_num
	FROM Carriers AS c, Weekdays AS w, Flights AS f
	WHERE c.cid = f.carrier_id AND
	w.did = f.day_of_week_id AND
	c.name = 'Alaska Airlines Inc.' AND
	w.day_of_week = 'Monday' AND
	f.origin_city = 'Seattle WA' AND
	f.dest_city = 'Boston MA';