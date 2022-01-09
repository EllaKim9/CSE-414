--a. 
CREATE TABLE InsuranceCo (
	name VARCHAR(256) PRIMARY KEY, 
	phone INT);

CREATE TABLE Driver (
	ssn INT PRIMARY KEY REFERENCES Person(ssn),
	driverID INT);

CREATE TABLE Vehicle (
	licensePlate VARCHAR(8) PRIMARY KEY, 
	year INT,
	maxLiability REAL,
	name VARCHAR(256) FOREIGN KEY REFERENCES InsuranceCo(name),
	ssn INT FOREIGN KEY REFERENCES Person(ssn));

CREATE TABLE Car (
	licensePlate VARCHAR(8) PRIMARY KEY REFERENCES Vehicle(licensePlate), 
	make VARCHAR(256));

CREATE TABLE Truck (
	licensePlate VARCHAR(8) PRIMARY KEY REFERENCES Vehicle(licensePlate),
	capacity INT
	ssn INT FOREIGN KEY REFERENCES ProfessionalDriver(ssn));

CREATE TABLE Person (
	ssn INT PRIMARY KEY, 
	name VARCHAR(256));

CREATE TABLE NonProfessionalDriver (
	ssn INT PRIMARY KEY REFERENCES Driver(ssn));

CREATE TABLE Drives (
	ssn INT REFERENCES NonProfessionalDriver(ssn)
	licensePlate VARCHAR(8) REFERENCES Car(licensePlate)
	PRIMARY KEY(ssn, licensePlate));

CREATE TABLE ProfessionalDriver	(
	ssn INT PRIMARY KEY REFERENCES Driver(ssn),
	medicalHistory VARCHAR(256));


--b.
The table Vehicle represents the the realtionship "insures," as it is a N to "at most 1"
relationship, so I can represent the relationship with InsuranceCo's primary key and 
the table for maxLiability in Vehicle. 



--c.
Whereas Operates goes from Truck to ProfessionalDriver from "no constraint" to "at most 1" 
relationship, the relationship from Car to NonProfessionalDiver is "no constraint" to 
"no constraint," so I created a new table for this relationship. (i.e, each Truck can 
only be driven by one ProfessionalDriver, but each Car can be driven by more than one 
NonProfessionalDriver).


