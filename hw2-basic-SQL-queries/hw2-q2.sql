/*1472 rows*/
SELECT c.name AS name, f1.flight_num AS f1_flight_num,
	f1.origin_city AS f1_origin_city, f1.dest_city AS f1_dest_city, 
	f1.actual_time AS f1_actual_time, f2.flight_num AS f2_flight_num, 
	f2.origin_city AS f2_origin_city, f2.dest_city AS f2_dest_city, 
	f2.actual_time AS f2_actual_time, (f1.actual_time + f2.actual_time) AS actual_time
	FROM Carriers AS c, Months AS m, Flights AS f1, Flights AS f2
	WHERE c.cid = f1.carrier_id AND
	c.cid = f2.carrier_id AND
	m.mid = f1.month_id AND
	m.mid = f2.month_id AND
	m.month = 'July' AND 
	f1.day_of_month = 15 AND
	f2.day_of_month = 15 AND
	f1.origin_city = 'Seattle WA' AND
	f2.dest_city = 'Boston MA' AND 
	f1.dest_city = f2.origin_city AND
	(f1.actual_time + f2.actual_time)/60.0 < 7.0;

