CREATE DATABASE IF NOT EXISTS realtorsite; 
USE realtorsite; 

DROP TABLE IF EXISTS ZipCodes; 
DROP TABLE IF EXISTS Homes;  
DROP TABLE IF EXISTS Cities; 
DROP TABLE IF EXISTS Schools;
DROP TABLE IF EXISTS StatisticsOf; 
DROP TABLE IF EXISTS Counties; 
DROP TABLE IF EXISTS CrimeStatistics;

CREATE TABLE Counties( 
	DistrictNumber INT PRIMARY KEY, 
	DistrictName VARCHAR(64), 
	Grade2022 VARCHAR(1) NOT NULL
) ENGINE = InnoDB; 

CREATE TABLE Schools(
	SchoolID INT PRIMARY KEY, 
    DistrictNumber INT, 
	SchoolName VARCHAR(255) NOT NULL, 
    Grade2022 CHAR(1), 
	FOREIGN KEY (DistrictNumber) REFERENCES Counties(DistrictNumber) 
    on update cascade
    on delete no action 
) ENGINE = InnoDB; 

CREATE TABLE CrimeStatistics( 
	statisticsID VARCHAR(64) PRIMARY KEY, 
    CountyName TEXT, 
	totalCrimeIndex INT NOT NULL, 
    Total_Arrests DECIMAL(10,2),
    Population TEXT, 
	Burglary DECIMAL(10,2),
    Larceny DECIMAL(10,2),
    Motor_Vehicle_Theft DECIMAL(10,2),
    Manslaughter DECIMAL(10,2),
    Kidnap_Abduction DECIMAL(10,2),
    Arson DECIMAL(10,2),
    Simple_Assault DECIMAL(10,2),
    Drug_Arrest DECIMAL(10,2),
    Bribery DECIMAL(10,2),
    Embezzlement DECIMAL(10,2),
    Fraud DECIMAL(10,2),
    Counterfeit_Forgery DECIMAL(10,2),
    Extortion_Blackmail DECIMAL(10,2),
    Intimidation DECIMAL(10,2),
    Prostitution DECIMAL(10,2),
    NonForcible_Sex_Offenses DECIMAL(10,2),
    Stolen_Property DECIMAL(10,2),
    DUI DECIMAL(10,2),
    Destruction_Vandalism DECIMAL(10,2),
    Gambling DECIMAL(10,2),
    Weapons_Violations DECIMAL(10,2),
    Liquor_Law_Violations DECIMAL(10,2),
    Misc DECIMAL(10,2)
)ENGINE = InnoDB;  

CREATE TABLE StatisticsOf( #lookup table to find a county's crime statistic id
	DistrictNumber INT, 
    statisticsID VARCHAR(64), 
    PRIMARY KEY(DistrictNumber, statisticsID), 
	FOREIGN KEY(DistrictNumber) REFERENCES Counties(DistrictNumber),  
	FOREIGN KEY(statisticsID) REFERENCES CrimeStatistics(statisticsID)
	on update cascade
    on delete no action 
)ENGINE = InnoDB; 

-- Lookup Table
CREATE TABLE ZipCodes (
    ZipCode INT PRIMARY KEY,
    City TEXT,
    County TEXT 
)Engine = InnoDB;

CREATE TABLE Homes( 
	listingID VARCHAR(64) PRIMARY KEY, 
	ZipCode INT NOT NULL, 
    property_url TEXT,
    style TEXT,
    street TEXT, 
    unit TEXT, 
    city VARCHAR(64),
    zip_code TEXT, 
    beds INT, 
    full_baths INT, 
    half_baths INT, 
    sqft INT, 
    year_built INT, 
	price float NOT NULL, 
	photo BLOB, 
    FOREIGN KEY (ZipCode) REFERENCES ZipCodes(ZipCode)
    on update cascade
    on delete no action 
)Engine = InnoDB; 
