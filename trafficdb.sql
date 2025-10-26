CREATE DATABASE TrafficViolationDB;
USE TrafficViolationDB;
-- 1. Driver Table
CREATE TABLE Driver (
    Driver_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    Contact_no VARCHAR(15),
    License_no VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Vehicle Table
CREATE TABLE Vehicle (
    Vehicle_ID INT PRIMARY KEY,
    Registration_year INT,
    Model VARCHAR(50),
    Color VARCHAR(30),
    License_plate VARCHAR(20) UNIQUE NOT NULL,
    Driver_ID INT,
    FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
);

-- 3. Officer Table
CREATE TABLE Officer (
    Officer_ID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
	Officer_Rank VARCHAR(50),
    Badge_no VARCHAR(30) UNIQUE NOT NULL,
    Contact_no VARCHAR(15)
);

-- 4. Violation Table
CREATE TABLE Violation (
    Violation_ID INT PRIMARY KEY,
    Date_Time TIMESTAMP NOT NULL,
    Type VARCHAR(50),
    Location VARCHAR(100),
    Vehicle_ID INT NOT NULL,
    Officer_ID INT,
    FOREIGN KEY (Vehicle_ID) REFERENCES Vehicle(Vehicle_ID),
    FOREIGN KEY (Officer_ID) REFERENCES Officer(Officer_ID)
);

-- 5. Penalty Table
CREATE TABLE Penalty (
    Penalty_ID INT PRIMARY KEY,
    Amount DECIMAL(10,2) NOT NULL,
    Duedate DATE,
    Status VARCHAR(20) CHECK (Status IN ('Unpaid','Paid','Appealed')),
    Violation_ID INT UNIQUE,
    FOREIGN KEY (Violation_ID) REFERENCES Violation(Violation_ID)
);

-- 6. Payment Table
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY,
    Date DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    ModeofPayment VARCHAR(20) CHECK (ModeofPayment IN ('Cash','Card','Online','UPI')),
    Penalty_ID INT UNIQUE,
    FOREIGN KEY (Penalty_ID) REFERENCES Penalty(Penalty_ID)
);

-- 7. Appeal Table
CREATE TABLE Appeal (
    Appeal_ID INT PRIMARY KEY,
    Datefiled DATE NOT NULL,
    Status VARCHAR(20) CHECK (Status IN ('Pending','Accepted','Rejected')),
    Reason VARCHAR(255),
    Violation_ID INT UNIQUE,
    Driver_ID INT,
    FOREIGN KEY (Violation_ID) REFERENCES Violation(Violation_ID),
    FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
);

CREATE TABLE IF NOT EXISTS Violation_Type (
    ViolationType_ID INT PRIMARY KEY AUTO_INCREMENT,
    Type_Name VARCHAR(50) UNIQUE NOT NULL,
    Default_Amount DECIMAL(10,2) NOT NULL,
    Default_Demerit_Points INT DEFAULT 0,
    Default_Duedays INT DEFAULT 30,
    Description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Audit_Log (
    Audit_ID INT PRIMARY KEY AUTO_INCREMENT,
    Action VARCHAR(20),
    Table_Name VARCHAR(50),
    Record_ID INT,
    Action_By VARCHAR(100),
    Action_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Details TEXT
);

--Driver Table Inserts
INSERT INTO Driver VALUES (1, 'Arun Kumar', 'Bangalore', '9876543210', 'KA05AB1234');
INSERT INTO Driver VALUES (2, 'Meera Nair', 'Mysore', '9988776655', 'KA09CD5678');
INSERT INTO Driver VALUES (3, 'Rohit Sharma', 'Mangalore', '9123456780', 'KA19EF9101');
INSERT INTO Driver VALUES (4, 'Sneha Patil', 'Hubli', '9345678910', 'KA25GH1122');
--Vehicle Table Inserts
INSERT INTO Vehicle VALUES (101, 2020, 'Hyundai i20', 'White', 'KA01XY9999', 1);
INSERT INTO Vehicle VALUES (102, 2018, 'Honda City', 'Black', 'KA05AB4321', 2);
INSERT INTO Vehicle VALUES (103, 2019, 'Suzuki Baleno', 'Blue', 'KA09MN8765', 3);
INSERT INTO Vehicle VALUES (104, 2021, 'Toyota Innova', 'Silver', 'KA19PQ1122', 4);
--Officer Table Inserts
INSERT INTO Officer VALUES (201, 'Ravi Shankar', 'Inspector', 'B123', '9123456789');
INSERT INTO Officer VALUES (202, 'Lakshmi Rao', 'Sub-Inspector', 'B124', '9876501234');
INSERT INTO Officer VALUES (203, 'Manoj Kumar', 'Head Constable', 'B125', '9765432109');
--Violation Table Inserts
INSERT INTO Violation VALUES (301, '2025-09-15 10:30:00', 'Speeding', 'MG Road, Bangalore', 101, 201);
INSERT INTO Violation VALUES (302, '2025-09-16 11:00:00', 'Signal Jump', 'Brigade Road, Bangalore', 101, 202);
INSERT INTO Violation VALUES (303, '2025-09-17 09:15:00', 'Parking Violation', 'Mysore Palace Road', 102, 202);
INSERT INTO Violation VALUES (304, '2025-09-18 14:45:00', 'Drunk Driving', 'Mangalore Port Road', 103, 203);
INSERT INTO Violation VALUES (305, '2025-09-19 19:00:00', 'Overspeeding', 'Hubli NH Road', 104, 201);
--Penalty Table Inserts
INSERT INTO Penalty VALUES (401, 1500, '2025-09-20', 'Unpaid', 301);
INSERT INTO Penalty VALUES (402, 500, '2025-09-25', 'Paid', 302);
INSERT INTO Penalty VALUES (403, 1000, '2025-09-22', 'Unpaid', 303);
INSERT INTO Penalty VALUES (404, 750, '2025-09-20', 'Appealed', 304);
INSERT INTO Penalty VALUES (405, 1200, '2025-09-18', 'Unpaid', 305);
--Payment Table Inserts
INSERT INTO Payment VALUES (501, '2025-09-25', 500, 'Online', 402);
INSERT INTO Payment VALUES (502, '2025-09-21', 1500, 'Cash', 401);
--Appeal Table Inserts
INSERT INTO Appeal VALUES (601, '2025-09-15', 'Pending', 'Emergency situation', 304, 3);
INSERT INTO Appeal VALUES (602, '2025-09-19', 'Rejected', 'Wrong parking sign', 303, 2);

