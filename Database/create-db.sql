CREATE DATABASE IF NOT EXISTS realtorsite; 
USE realtorsite; 


DROP TABLE IF EXISTS Homes;
DROP TABLE IF EXISTS ZipCodes;
DROP TABLE IF EXISTS Cities; 
DROP TABLE IF EXISTS Schools;
DROP TABLE IF EXISTS StatisticsOf; 
DROP TABLE IF EXISTS CrimeStatistics;
DROP TABLE IF EXISTS Counties; 

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
	totalCrimeIndex INT NOT NULL, 
    Total_Arrests DECIMAL(10,2),
    Population INT, 
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
    Misc DECIMAL(10,2), 
    
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
    City VARCHAR(200),
    County VARCHAR(200) 
)Engine = InnoDB;

CREATE TABLE Homes(
    listingID INT AUTO_INCREMENT PRIMARY KEY,
    ZipCode INT NOT NULL,
    property_url VARCHAR(250) DEFAULT 'www.google.com',
    style VARCHAR(200),
    street VARCHAR(250),
    unit VARCHAR(200),
    city VARCHAR(64),
    beds INT DEFAULT 0,
    full_baths INT DEFAULT 0,
    half_baths INT DEFAULT 0,
    sqft INT DEFAULT 2000,
    year_built INT DEFAULT 2010,
    price FLOAT DEFAULT 0,
    photo VARCHAR(250),
    type VARCHAR(100),  -- New type attribute
    latitude DECIMAL(10, 8),  -- New latitude attribute
    longitude DECIMAL(11, 8),  -- New longitude attribute
    FOREIGN KEY (ZipCode) REFERENCES ZipCodes(ZipCode)
        ON UPDATE CASCADE
        ON DELETE NO ACTION
) ENGINE = InnoDB;


