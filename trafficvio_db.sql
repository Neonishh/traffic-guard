-- Create and use the database
CREATE DATABASE IF NOT EXISTS TrafficVioDB;
USE TrafficVioDB;

-- 1. Driver Table
CREATE TABLE Driver (
    Driver_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Address VARCHAR(255),
    Contact_no VARCHAR(15),
    License_no VARCHAR(50) UNIQUE NOT NULL
);

-- 2. Vehicle Table
CREATE TABLE Vehicle (
    Vehicle_ID INT PRIMARY KEY AUTO_INCREMENT,
    Registration_year INT,
    Model VARCHAR(50),
    Color VARCHAR(30),
    License_plate VARCHAR(20) UNIQUE NOT NULL,
    Driver_ID INT,
    FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
);

-- 3. Officer Table
CREATE TABLE Officer (
    Officer_ID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(100) NOT NULL,
    Officer_Rank VARCHAR(50),
    Badge_no VARCHAR(30) UNIQUE NOT NULL,
    Contact_no VARCHAR(15)
);

-- 4. Violation Table
CREATE TABLE Violation (
    Violation_ID INT PRIMARY KEY AUTO_INCREMENT,
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
    Penalty_ID INT PRIMARY KEY AUTO_INCREMENT,
    Amount DECIMAL(10,2) NOT NULL,
    Duedate DATE,
    Status VARCHAR(20) CHECK (Status IN ('Unpaid','Paid','Appealed')),
    Violation_ID INT UNIQUE,
    FOREIGN KEY (Violation_ID) REFERENCES Violation(Violation_ID)
);

-- 6. Payment Table
CREATE TABLE Payment (
    Payment_ID INT PRIMARY KEY AUTO_INCREMENT,
    Date DATE NOT NULL,
    Amount DECIMAL(10,2) NOT NULL,
    ModeofPayment VARCHAR(20) CHECK (ModeofPayment IN ('Cash','Card','Online','UPI')),
    Penalty_ID INT UNIQUE,
    FOREIGN KEY (Penalty_ID) REFERENCES Penalty(Penalty_ID)
);

-- 7. Appeal Table
CREATE TABLE Appeal (
    Appeal_ID INT PRIMARY KEY AUTO_INCREMENT,
    Datefiled DATE NOT NULL,
    Status VARCHAR(20) CHECK (Status IN ('Pending','Accepted','Rejected')),
    Reason VARCHAR(255),
    Violation_ID INT UNIQUE,
    Driver_ID INT,
    FOREIGN KEY (Violation_ID) REFERENCES Violation(Violation_ID),
    FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
);

-- 8. Violation Type Table
CREATE TABLE IF NOT EXISTS Violation_Type (
    ViolationType_ID INT PRIMARY KEY AUTO_INCREMENT,
    Type_Name VARCHAR(50) UNIQUE NOT NULL,
    Default_Amount DECIMAL(10,2) NOT NULL,
    Default_Demerit_Points INT DEFAULT 0,
    Default_Duedays INT DEFAULT 30,
    Description VARCHAR(255)
);

-- 9. Audit Log Table
CREATE TABLE IF NOT EXISTS Audit_Log (
    Audit_ID INT PRIMARY KEY AUTO_INCREMENT,
    Action VARCHAR(20),
    Table_Name VARCHAR(50),
    Record_ID INT,
    Action_By VARCHAR(100),
    Action_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Details TEXT
);

-- -----------------------------
-- INSERT STATEMENTS
-- -----------------------------

-- Driver Table Inserts
INSERT INTO Driver (Name, Address, Contact_no, License_no) VALUES
('Arun Kumar', 'Bangalore', '9876543210', 'KA05AB1234'),
('Meera Nair', 'Mysore', '9988776655', 'KA09CD5678'),
('Rohit Sharma', 'Mangalore', '9123456780', 'KA19EF9101'),
('Sneha Patil', 'Hubli', '9345678910', 'KA25GH1122');

-- Vehicle Table Inserts
INSERT INTO Vehicle (Registration_year, Model, Color, License_plate, Driver_ID) VALUES
(2020, 'Hyundai i20', 'White', 'KA01XY9999', 1),
(2018, 'Honda City', 'Black', 'KA05AB4321', 2),
(2019, 'Suzuki Baleno', 'Blue', 'KA09MN8765', 3),
(2021, 'Toyota Innova', 'Silver', 'KA19PQ1122', 4);

-- Officer Table Inserts
INSERT INTO Officer (Name, Officer_Rank, Badge_no, Contact_no) VALUES
('Ravi Shankar', 'Inspector', 'B123', '9123456789'),
('Lakshmi Rao', 'Sub-Inspector', 'B124', '9876501234'),
('Manoj Kumar', 'Head Constable', 'B125', '9765432109');

-- Violation Table Inserts
INSERT INTO Violation (Date_Time, Type, Location, Vehicle_ID, Officer_ID) VALUES
('2025-09-15 10:30:00', 'Speeding', 'MG Road, Bangalore', 1, 1),
('2025-09-16 11:00:00', 'Signal Jump', 'Brigade Road, Bangalore', 1, 2),
('2025-09-17 09:15:00', 'Parking Violation', 'Mysore Palace Road', 2, 2),
('2025-09-18 14:45:00', 'Drunk Driving', 'Mangalore Port Road', 3, 3),
('2025-09-19 19:00:00', 'Overspeeding', 'Hubli NH Road', 4, 1);

-- Penalty Table Inserts
INSERT INTO Penalty (Amount, Duedate, Status, Violation_ID) VALUES
(1500, '2025-09-20', 'Unpaid', 1),
(500, '2025-09-25', 'Paid', 2),
(1000, '2025-09-22', 'Unpaid', 3),
(750, '2025-09-20', 'Appealed', 4),
(1200, '2025-09-18', 'Unpaid', 5);

-- Payment Table Inserts
INSERT INTO Payment (Date, Amount, ModeofPayment, Penalty_ID) VALUES
('2025-09-25', 500, 'Online', 2),
('2025-09-21', 1500, 'Cash', 1);

-- Appeal Table Inserts
INSERT INTO Appeal (Datefiled, Status, Reason, Violation_ID, Driver_ID) VALUES
('2025-09-15', 'Pending', 'Emergency situation', 4, 3),
('2025-09-19', 'Rejected', 'Wrong parking sign', 3, 2);

-- Violation Type Inserts
INSERT INTO Violation_Type (Type_Name, Default_Amount, Default_Demerit_Points, Default_Duedays, Description)
VALUES
('Speeding', 1000, 2, 30, 'Exceeding speed limit'),
('Signal Jump', 1500, 3, 30, 'Jumping red traffic signal'),
('Parking Violation', 500, 1, 30, 'Illegal parking or wrong parking'),
('Drunk Driving', 2500, 6, 30, 'Driving under the influence of alcohol'),
('Overspeeding', 1200, 2, 30, 'Driving above permitted speed');

-- -----------------------------
-- VIOLATION TYPE UPDATES
-- -----------------------------
ALTER TABLE Violation ADD COLUMN ViolationType_ID INT;

SET SQL_SAFE_UPDATES = 0;

UPDATE Violation v
JOIN Violation_Type vt ON v.Type = vt.Type_Name
SET v.ViolationType_ID = vt.ViolationType_ID;

UPDATE Violation
SET Type = 'Underage Driving'
WHERE Type = 'Overspeeding';

INSERT INTO Violation_Type 
(Type_Name, Default_Amount, Default_Demerit_Points, Default_Duedays, Description)
VALUES ('Underage Driving', 2000, 8, 30, 'Operating a vehicle below the legal driving age');

DELETE FROM Violation_Type
WHERE Type_Name = 'Overspeeding';

UPDATE Violation
JOIN Violation_Type vt ON Violation.Type = vt.Type_Name
SET Violation.ViolationType_ID = vt.ViolationType_ID
WHERE Violation.Type = 'Underage Driving';

SET SQL_SAFE_UPDATES = 1;  -- turn it back on (optional)

-- -----------------------------
-- TRIGGER
-- -----------------------------
DELIMITER $$

CREATE TRIGGER trg_auto_create_penalty
AFTER INSERT ON Violation
FOR EACH ROW
BEGIN
    DECLARE violation_amount DECIMAL(10,2);

    SET violation_amount = CASE NEW.Type
        WHEN 'Speeding' THEN 1000.00
        WHEN 'Signal Jump' THEN 1500.00
        WHEN 'Parking Violation' THEN 500.00
        WHEN 'Drunk Driving' THEN 2500.00
        WHEN 'Underage Driving' THEN 2000.00
        WHEN 'Seatbelt Violation' THEN 500.00
        WHEN 'Mobile Usage' THEN 1000.00
        WHEN 'No Insurance' THEN 2300.00
        ELSE 500.00
    END;

    INSERT INTO Penalty (Amount, Duedate, Status, Violation_ID)
    VALUES (violation_amount, DATE_ADD(CURRENT_DATE, INTERVAL 30 DAY), 'Unpaid', NEW.Violation_ID);
END$$

DELIMITER ;

DELIMITER $$

DROP TRIGGER IF EXISTS trg_update_penalty_status$$

CREATE TRIGGER trg_update_penalty_status
AFTER INSERT ON Payment
FOR EACH ROW
BEGIN
    -- Update the penalty status to 'Paid' when payment is made
    UPDATE Penalty
    SET Status = 'Paid'
    WHERE Penalty_ID = NEW.Penalty_ID;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_appeal_filed
AFTER INSERT ON Appeal
FOR EACH ROW
BEGIN
    -- As soon as appeal is filed, mark penalty as 'Appealed' (pending review)
    UPDATE Penalty
    SET Status = 'Appealed'
    WHERE Violation_ID = NEW.Violation_ID;
    
    -- Log it
    INSERT INTO Audit_Log (Action, Table_Name, Record_ID, Action_By, Details)
    VALUES ('INSERT', 'Appeal', NEW.Appeal_ID, USER(),
            CONCAT('Appeal filed for Violation #', NEW.Violation_ID, ' - Penalty status → Appealed'));
END$$
DELIMITER ;

DELIMITER $$

CREATE TRIGGER trg_update_penalty_on_appeal
AFTER UPDATE ON Appeal
FOR EACH ROW
BEGIN
    -- Only act if status changed
    IF OLD.Status != NEW.Status THEN
        
        -- If appeal is ACCEPTED, mark penalty as 'Paid' (waived/forgiven)
        IF NEW.Status = 'Accepted' THEN
            UPDATE Penalty
            SET Status = 'Paid'
            WHERE Violation_ID = NEW.Violation_ID;
            
            INSERT INTO Audit_Log (Action, Table_Name, Record_ID, Action_By, Details)
            VALUES ('UPDATE', 'Penalty', NEW.Violation_ID, USER(),
                    CONCAT('Appeal #', NEW.Appeal_ID, ' ACCEPTED - Penalty waived (Status → Paid)'));
        
        -- If appeal is REJECTED, mark penalty as 'Unpaid' (must pay)
        ELSEIF NEW.Status = 'Rejected' THEN
            UPDATE Penalty
            SET Status = 'Unpaid'
            WHERE Violation_ID = NEW.Violation_ID;
            
            INSERT INTO Audit_Log (Action, Table_Name, Record_ID, Action_By, Details)
            VALUES ('UPDATE', 'Penalty', NEW.Violation_ID, USER(),
                    CONCAT('Appeal #', NEW.Appeal_ID, ' REJECTED - Penalty must be paid (Status → Unpaid)'));
        
        -- If changed back to PENDING (rare case)
        ELSEIF NEW.Status = 'Pending' THEN
            UPDATE Penalty
            SET Status = 'Appealed'
            WHERE Violation_ID = NEW.Violation_ID;
        END IF;
        
    END IF;
END$$
DELIMITER ;

-- Insert new Drivers
INSERT INTO Driver (Name, Address, Contact_no, License_no) VALUES
('Vishal Singh', 'Delhi', '9845123456', 'DL01AK5123'),
('Sara Fernandes', 'Goa', '9938123076', 'GA08XY1547'),
('Ankit Bhatt', 'Ahmedabad', '9823032133', 'GJ05RT7721'),
('Priya Menon', 'Kochi', '9891123567', 'KL07ZE9982');

-- Insert new Vehicles
INSERT INTO Vehicle (Registration_year, Model, Color, License_plate, Driver_ID) VALUES
(2017, 'Ford Figo', 'Red', 'DL02CL4321', 5),
(2023, 'Volkswagen Polo', 'White', 'GA09NM7654', 6),
(2022, 'Honda Amaze', 'Silver', 'GJ06AB9912', 7),
(2020, 'Hyundai Creta', 'Black', 'KL09ZZ9876', 8);

-- Insert new Officers
INSERT INTO Officer (Name, Officer_Rank, Badge_no, Contact_no) VALUES
('Sahil Gupta', 'Inspector', 'B126', '9678123456'),
('Fatima Noor', 'Sub-Inspector', 'B134', '9182736451');

-- Insert additional Violation Types
INSERT INTO Violation_Type (Type_Name, Default_Amount, Default_Demerit_Points, Default_Duedays, Description) VALUES
('Seatbelt Violation', 500, 1, 30, 'Driver or passenger not wearing seatbelt'),
('Red Light Jump', 1200, 3, 30, 'Did not stop at red traffic signal'),
('Mobile Usage', 1000, 2, 30, 'Using mobile phone while driving'),
('No Insurance', 2300, 5, 15, 'Vehicle does not have valid insurance');

-- Insert Violations (auto-increment Violation_ID)
INSERT INTO Violation (Date_Time, Type, Location, Vehicle_ID, Officer_ID) VALUES
('2025-10-01 08:15:00', 'Seatbelt Violation', 'NH8, Delhi', 5, 1),
('2025-10-01 09:00:00', 'Red Light Jump', 'Ashram Chowk, Delhi', 5, 2),
('2025-10-01 15:20:00', 'Mobile Usage', 'Calangute Beach Road, Goa', 6, 1),
('2025-10-02 17:50:00', 'Seatbelt Violation', 'Riverfront Road, Ahmedabad', 7, 3),
('2025-10-02 19:15:00', 'No Insurance', 'Marine Drive, Kochi', 8, 5),
('2025-10-03 11:40:00', 'Underage Driving', 'NH66, Kochi', 1, 2);

-- Insert Payments
INSERT INTO Payment (Date, Amount, ModeofPayment, Penalty_ID) VALUES
('2025-10-10', 500, 'Card', 6),
('2025-10-18', 500, 'UPI', 9);

-- Insert Appeals
INSERT INTO Appeal (Datefiled, Status, Reason, Violation_ID, Driver_ID) VALUES
('2025-10-18', 'Pending', 'Insurance in process', 10, 8),
('2025-10-21', 'Accepted', 'Age incorrect in records', 11, 8);

DELIMITER $$
CREATE FUNCTION GetMostFrequentViolationType()
RETURNS VARCHAR(50)
DETERMINISTIC
BEGIN
    DECLARE mostFrequentType VARCHAR(50);

    SELECT vi.Type
    INTO mostFrequentType
    FROM Violation vi
    GROUP BY vi.Type
    ORDER BY COUNT(*) DESC
    LIMIT 1;

    RETURN mostFrequentType;
END $$

DELIMITER ;
SELECT GetMostFrequentViolationType() AS MostCommonViolation;

-- Stored Procedure — Calculate Total Unpaid Fines for a Driver
DELIMITER $$

CREATE PROCEDURE CalculateTotalUnpaidFines(IN p_DriverID INT)
BEGIN
    SELECT 
        d.Driver_ID,
        d.Name,
        SUM(p.Amount) AS Total_Unpaid_Fines
    FROM Driver d
    JOIN Vehicle v ON d.Driver_ID = v.Driver_ID
    JOIN Violation vi ON v.Vehicle_ID = vi.Vehicle_ID
    JOIN Penalty p ON vi.Violation_ID = p.Violation_ID
    WHERE d.Driver_ID = p_DriverID
      AND p.Status = 'Unpaid'
    GROUP BY d.Driver_ID, d.Name;
END $$

DELIMITER ;
CALL CalculateTotalUnpaidFines(1);

-- Stored Procedure — Get Driver Violation History
DELIMITER $$

CREATE PROCEDURE GetDriverViolationHistory(IN p_DriverID INT)
BEGIN
    SELECT 
        d.Driver_ID,
        d.Name,
        v.Vehicle_ID,
        vi.Violation_ID,
        vi.Type AS Violation_Type,
        vi.Date_Time,
        vi.Location,
        p.Amount AS Penalty_Amount,
        p.Status AS Penalty_Status
    FROM Driver d
    JOIN Vehicle v ON d.Driver_ID = v.Driver_ID
    JOIN Violation vi ON v.Vehicle_ID = vi.Vehicle_ID
    LEFT JOIN Penalty p ON vi.Violation_ID = p.Violation_ID
    WHERE d.Driver_ID = p_DriverID
    ORDER BY vi.Date_Time DESC;
END $$

DELIMITER ;
CALL GetDriverViolationHistory(2);

-- Create an admin user (full privileges)
CREATE USER IF NOT EXISTS 'admin_user'@'localhost' IDENTIFIED BY 'admin123';
GRANT ALL PRIVILEGES ON TrafficVioDB.* TO 'admin_user'@'localhost' WITH GRANT OPTION;

-- Create a data entry operator (limited privileges)
CREATE USER IF NOT EXISTS 'data_entry'@'localhost' IDENTIFIED BY 'entry123';
GRANT SELECT, INSERT, UPDATE ON TrafficVioDB.* TO 'data_entry'@'localhost';

-- Create a viewer user (read-only)
CREATE USER IF NOT EXISTS 'viewer'@'localhost' IDENTIFIED BY 'view123';
GRANT SELECT ON TrafficVioDB.* TO 'viewer'@'localhost';

FLUSH PRIVILEGES;

-- Grant INSERT privilege to the viewer user for Payment and Appeal tables
GRANT INSERT ON TrafficVioDB.Payment TO 'viewer'@'localhost';
GRANT INSERT ON TrafficVioDB.Appeal TO 'viewer'@'localhost';

FLUSH PRIVILEGES;
-- Get Summary Report for Violations by City (JOIN + AGGREGATE)
DELIMITER $$
CREATE PROCEDURE GetViolationSummary()
BEGIN
    SELECT 
        SUBSTRING_INDEX(v.Location, ',', -1) AS City,
        COUNT(v.Violation_ID) AS Total_Violations,
        SUM(p.Amount) AS Total_Penalties,
        SUM(CASE WHEN p.Status = 'Unpaid' THEN 1 ELSE 0 END) AS Unpaid_Count
    FROM Violation v
    JOIN Penalty p ON v.Violation_ID = p.Violation_ID
    GROUP BY City
    ORDER BY Total_Violations DESC;
END$$
DELIMITER ;

-- Nested Query Example: Drivers with more than one violation
DELIMITER $$
CREATE VIEW DriversWithMultipleViolations AS
SELECT d.Driver_ID, d.Name, COUNT(v.Violation_ID) AS Total_Violations
FROM Driver d
JOIN Vehicle ve ON d.Driver_ID = ve.Driver_ID
JOIN Violation v ON ve.Vehicle_ID = v.Vehicle_ID
GROUP BY d.Driver_ID, d.Name
HAVING COUNT(v.Violation_ID) > 1;
$$
DELIMITER ;

-- Drop existing foreign key
ALTER TABLE Vehicle DROP FOREIGN KEY Vehicle_ibfk_1;

-- Add new foreign key with CASCADE DELETE
ALTER TABLE Vehicle 
ADD CONSTRAINT fk_vehicle_driver 
FOREIGN KEY (Driver_ID) REFERENCES Driver(Driver_ID)
ON DELETE CASCADE;

DELIMITER $$

DROP TRIGGER IF EXISTS trg_set_violation_type_id$$

CREATE TRIGGER trg_set_violation_type_id
BEFORE INSERT ON Violation
FOR EACH ROW
BEGIN
    DECLARE type_id INT;
    
    -- Get ViolationType_ID from Violation_Type table
    SELECT ViolationType_ID INTO type_id
    FROM Violation_Type
    WHERE Type_Name = NEW.Type;
    
    -- Set the ViolationType_ID
    IF type_id IS NOT NULL THEN
        SET NEW.ViolationType_ID = type_id;
    END IF;
END$$

DELIMITER ;

-- JOIN Query: Get Violation Details with Driver and Vehicle Info
SELECT 
    v.Violation_ID,
    v.Date_Time,
    v.Type AS Violation_Type,
    v.Location,
    d.Name AS Driver_Name,
    d.License_no,
    ve.License_plate,
    ve.Model,
    o.Name AS Officer_Name,
    p.Amount AS Fine_Amount,
    p.Status AS Payment_Status
FROM Violation v
JOIN Vehicle ve ON v.Vehicle_ID = ve.Vehicle_ID
JOIN Driver d ON ve.Driver_ID = d.Driver_ID
JOIN Officer o ON v.Officer_ID = o.Officer_ID
LEFT JOIN Penalty p ON v.Violation_ID = p.Violation_ID
ORDER BY v.Date_Time DESC;

-- AGGREGATE Query: Revenue and Violation Statistics
SELECT 
    COUNT(DISTINCT d.Driver_ID) AS Total_Drivers,
    COUNT(v.Violation_ID) AS Total_Violations,
    SUM(p.Amount) AS Total_Revenue,
    AVG(p.Amount) AS Average_Fine,
    MAX(p.Amount) AS Highest_Fine,
    MIN(p.Amount) AS Lowest_Fine,
    SUM(CASE WHEN p.Status = 'Paid' THEN p.Amount ELSE 0 END) AS Revenue_Collected,
    SUM(CASE WHEN p.Status = 'Unpaid' THEN p.Amount ELSE 0 END) AS Revenue_Pending
FROM Driver d
JOIN Vehicle ve ON d.Driver_ID = ve.Driver_ID
JOIN Violation v ON ve.Vehicle_ID = v.Vehicle_ID
JOIN Penalty p ON v.Violation_ID = p.Violation_ID;

select * from Driver;
select * from Vehicle;
select * from payment;