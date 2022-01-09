--1.
CREATE TABLE Sales (
	name VARCHAR(10), 
	discount VARCHAR(4),
	month VARCHAR(3), 
	price INT);

--.read hw4.sql (to read in data from .txt)

--2. FD: if know column1 value, then know exact value for column2

/* (name->price) Result would be tuples for 1 or more unique prices for that given name. 
The result is nothing, so all tuples have exactly one price for every name 
(know that price is never null). Shows the FD between name & price */

SELECT *
	FROM Sales AS s1, Sales AS s2
	WHERE s1.name = s2.name AND
	s1.price != s2.price;
	

/* (month->discount) same as above but for month and discount FD */

SELECT *
	FROM Sales AS s1, Sales as s2
	WHERE s1.month = s2.month AND 
	s2.price != s2.price;

/* (name, discount->price, month) same execpt unique Price and Month for that given 
name and discount instance) */

SELECT * 
	FROM Sales AS s1, Sales as s2
	WHERE (s1.name = s2.name AND s1.discount = s2.discount) AND 
	(s1.price != s2.price AND s1.month != s2.month);

/* (month, price->discount, name) same FD as directly above execpt unique discount
and and name for that given month and price instance */

SELECT * 
	FROM Sales AS s1, Sales as s2
	WHERE (s1.month = s2.month and s1.price = s2.price) AND
 	(s1.discount != s2.discount and s1.name != s2.name);

--3. 
/* R(month, discount, name, price) as FD, where month = M, discount = D, name = N, & price = P
M -> D, N -> P
	1. M -> D violates BCNF, so split to
	(D, M), (M, N, P)

	2. N -> P violates BCNF, so split to
	(N, P), (M, N)

-ans: (D, M), (N, P) and (M, N) */

CREATE TABLE MerchPrice (
	name VARCHAR(10) PRIMARY KEY, 
	price INT);

CREATE TABLE DiscountMonth (
	month VARCHAR(3) PRIMARY KEY, 
	discount VARCHAR(4));

CREATE TABLE MonthMerch (
	name VARCHAR(10),
	month VARCHAR(3),
	FOREIGN KEY(name) REFERENCES MerchPrice(name), 
	FOREIGN KEY(month) REFERENCES DiscountMonth(month));

--4

/* Count = 37 rows (Total - Header = 36 rows) */
INSERT INTO MerchPrice 
	SELECT DISTINCT name, price 
	FROM Sales;

-- DISTINCT is kinda like the FD above 

SELECT COUNT(*) 
	FROM MerchPrice;

/* Count = 13 rows (Total - Header = 12 rows) */
INSERT INTO DiscountMonth
	SELECT DISTINCT month, discount 
	FROM Sales;

SELECT COUNT(*) 
	FROM DiscountMonth;

/* Count = 427 rows (Total - Header = 426 rows) */
INSERT INTO MonthMerch
	SELECT DISTINCT name, month 
	FROM Sales;

SELECT COUNT(*) 
	FROM MonthMerch;