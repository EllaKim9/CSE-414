CREATE TABLE Caregivers (
    UsernameC varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (UsernameC)
);

CREATE TABLE Availabilities (
    Time date,
    UsernameC varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, UsernameC)
);

CREATE TABLE Patients (
    UsernameP varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (UsernameP)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointments (
    AppointmentID int,
    UsernameP varchar(255) REFERENCES Patients,
    UsernameC varchar(255) REFERENCES Caregivers,
    Name varchar(255) REFERENCES Vaccines,
    Time date,
    PRIMARY KEY (AppointmentID),
);

