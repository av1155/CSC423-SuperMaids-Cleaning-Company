-- ============================================================
-- SuperMaids Cleaning Company Database
-- CSC 423 - Database Systems - Part 3
-- Oracle Enterprise DBMS Implementation
-- Andrea A. Venti Fuentes, Jeremiah Moise
-- University of Miami
-- December 07, 2025
-- ============================================================

-- ------------------------------------------------------------
-- CLEAN RESET: Drop existing objects
-- ------------------------------------------------------------
DROP TABLE ASSIGNED_TO CASCADE CONSTRAINTS;
DROP TABLE REQUIRES CASCADE CONSTRAINTS;
DROP TABLE REQUIREMENT CASCADE CONSTRAINTS;
DROP TABLE EQUIPMENT CASCADE CONSTRAINTS;
DROP TABLE EMPLOYEE CASCADE CONSTRAINTS;
DROP TABLE CLIENT CASCADE CONSTRAINTS;

-- ------------------------------------------------------------
-- PART 3(a): CREATE DATABASE SCHEMA WITH CONSTRAINTS
-- ------------------------------------------------------------

CREATE TABLE CLIENT (
    clientNo        NUMBER PRIMARY KEY,
    fName           VARCHAR2(50) NOT NULL,
    lName           VARCHAR2(50) NOT NULL,
    address         VARCHAR2(255) NOT NULL,
    telephoneNo     VARCHAR2(15) NOT NULL
);

CREATE TABLE EMPLOYEE (
    employeeNo      NUMBER PRIMARY KEY,
    fName           VARCHAR2(50) NOT NULL,
    lName           VARCHAR2(50) NOT NULL,
    address         VARCHAR2(255) NOT NULL,
    salary          NUMBER(10,2) NOT NULL CHECK (salary >= 0),
    telephoneNo     VARCHAR2(15) NOT NULL
);

CREATE TABLE EQUIPMENT (
    equipmentNo     NUMBER PRIMARY KEY,
    description     VARCHAR2(100) NOT NULL,
    usage           VARCHAR2(100),
    cost            NUMBER(10,2) NOT NULL CHECK (cost >= 0)
);

CREATE TABLE REQUIREMENT (
    requirementNo   NUMBER PRIMARY KEY,
    clientNo        NUMBER NOT NULL,
    sDate           DATE NOT NULL,
    sTime           TIMESTAMP NOT NULL,
    duration        NUMBER NOT NULL CHECK (duration > 0),
    comments        VARCHAR2(255),
    CONSTRAINT fk_req_client FOREIGN KEY (clientNo) 
        REFERENCES CLIENT(clientNo)
);

CREATE TABLE REQUIRES (
    requirementNo   NUMBER NOT NULL,
    equipmentNo     NUMBER NOT NULL,
    quantity        NUMBER NOT NULL CHECK (quantity > 0),
    CONSTRAINT pk_requires PRIMARY KEY (requirementNo, equipmentNo),
    CONSTRAINT fk_requires_req FOREIGN KEY (requirementNo) 
        REFERENCES REQUIREMENT(requirementNo),
    CONSTRAINT fk_requires_equip FOREIGN KEY (equipmentNo) 
        REFERENCES EQUIPMENT(equipmentNo)
);

CREATE TABLE ASSIGNED_TO (
    requirementNo   NUMBER NOT NULL,
    employeeNo      NUMBER NOT NULL,
    CONSTRAINT pk_assigned_to PRIMARY KEY (requirementNo, employeeNo),
    CONSTRAINT fk_assigned_req FOREIGN KEY (requirementNo) 
        REFERENCES REQUIREMENT(requirementNo),
    CONSTRAINT fk_assigned_emp FOREIGN KEY (employeeNo) 
        REFERENCES EMPLOYEE(employeeNo)
);

-- ------------------------------------------------------------
-- PART 3(b): INSERT SAMPLE DATA (5 tuples per table)
-- ------------------------------------------------------------

-- CLIENT data
INSERT INTO CLIENT VALUES (1, 'John', 'Smith', '100 Main St', '305-111-1111');
INSERT INTO CLIENT VALUES (2, 'Paul', 'Nuttall', '22 Orange Ave', '305-222-2222');
INSERT INTO CLIENT VALUES (3, 'Linda', 'Park', '77 Sunset Blvd', '305-333-3333');
INSERT INTO CLIENT VALUES (4, 'Cardboard', 'BoxCo', '88 Industrial Rd', '305-444-4444');
INSERT INTO CLIENT VALUES (5, 'Maria', 'Lopez', '55 Coral Way', '305-555-5555');

-- EMPLOYEE data
INSERT INTO EMPLOYEE VALUES (1, 'Sarah', 'Johnson', '12 Pine St', 42000, '305-999-1111');
INSERT INTO EMPLOYEE VALUES (2, 'Mike', 'Brown', '8 Oak St', 41000, '305-999-2222');
INSERT INTO EMPLOYEE VALUES (3, 'Emily', 'Clark', '20 Palm Dr', 45000, '305-999-3333');
INSERT INTO EMPLOYEE VALUES (4, 'George', 'Hill', '9 Birch Rd', 39000, '305-999-4444');
INSERT INTO EMPLOYEE VALUES (5, 'Olivia', 'Cruz', '3 Maple Ave', 47000, '305-999-5555');

-- EQUIPMENT data
INSERT INTO EQUIPMENT VALUES (1, 'Industrial Floor Cleaner', 'Floor deep clean', 200);
INSERT INTO EQUIPMENT VALUES (2, 'Vacuum', 'Standard vacuum cleaning', 50);
INSERT INTO EQUIPMENT VALUES (3, 'Pressure Washer', 'Outdoor cleaning', 150);
INSERT INTO EQUIPMENT VALUES (4, 'Scrubber', 'Tile scrubbing', 120);
INSERT INTO EQUIPMENT VALUES (5, 'Steam Cleaner', 'Carpet steaming', 180);

-- REQUIREMENT data
INSERT INTO REQUIREMENT VALUES (1, 4, TO_DATE('2025-01-02', 'YYYY-MM-DD'), 
    TO_TIMESTAMP('2025-01-02 07:00:00', 'YYYY-MM-DD HH24:MI:SS'), 120, 'Morning shift');
INSERT INTO REQUIREMENT VALUES (2, 4, TO_DATE('2025-01-02', 'YYYY-MM-DD'), 
    TO_TIMESTAMP('2025-01-02 17:00:00', 'YYYY-MM-DD HH24:MI:SS'), 120, 'Evening shift');
INSERT INTO REQUIREMENT VALUES (3, 2, TO_DATE('2025-01-05', 'YYYY-MM-DD'), 
    TO_TIMESTAMP('2025-01-05 10:00:00', 'YYYY-MM-DD HH24:MI:SS'), 180, 'Weekly clean');
INSERT INTO REQUIREMENT VALUES (4, 1, TO_DATE('2025-01-08', 'YYYY-MM-DD'), 
    TO_TIMESTAMP('2025-01-08 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 90, 'Deep clean');
INSERT INTO REQUIREMENT VALUES (5, 3, TO_DATE('2025-01-11', 'YYYY-MM-DD'), 
    TO_TIMESTAMP('2025-01-11 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 120, 'General clean');

-- REQUIRES data
INSERT INTO REQUIRES VALUES (1, 1, 3);
INSERT INTO REQUIRES VALUES (1, 2, 2);
INSERT INTO REQUIRES VALUES (2, 1, 1);
INSERT INTO REQUIRES VALUES (3, 5, 1);
INSERT INTO REQUIRES VALUES (4, 4, 1);

-- ASSIGNED_TO data
INSERT INTO ASSIGNED_TO VALUES (1, 1);
INSERT INTO ASSIGNED_TO VALUES (1, 2);
INSERT INTO ASSIGNED_TO VALUES (2, 3);
INSERT INTO ASSIGNED_TO VALUES (3, 4);
INSERT INTO ASSIGNED_TO VALUES (4, 5);

COMMIT;

-- ------------------------------------------------------------
-- VERIFICATION: Display all table contents
-- ------------------------------------------------------------
SELECT 'CLIENT TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM CLIENT;

SELECT 'EMPLOYEE TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM EMPLOYEE;

SELECT 'EQUIPMENT TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM EQUIPMENT;

SELECT 'REQUIREMENT TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM REQUIREMENT;

SELECT 'REQUIRES TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM REQUIRES;

SELECT 'ASSIGNED_TO TABLE' AS "Table Name" FROM DUAL;
SELECT * FROM ASSIGNED_TO;

-- ------------------------------------------------------------
-- PART 3(c): 5 SQL QUERIES (Embedded SQL Transactions)
-- These correspond to the transactions validated in Part 2c
-- ------------------------------------------------------------

-- Transaction 1: List all clients and their requirements
SELECT 'TRANSACTION 1: List all clients and their requirements' AS "Query" FROM DUAL;
SELECT 
    C.fName, 
    C.lName, 
    R.requirementNo, 
    R.sDate, 
    TO_CHAR(R.sTime, 'HH24:MI') AS sTime
FROM CLIENT C
JOIN REQUIREMENT R ON C.clientNo = R.clientNo
ORDER BY C.lName, R.sDate;

-- Transaction 2: Equipment needed for requirement #1
SELECT 'TRANSACTION 2: Equipment needed for requirement #1' AS "Query" FROM DUAL;
SELECT 
    E.description, 
    REQ.quantity
FROM REQUIRES REQ
JOIN EQUIPMENT E ON REQ.equipmentNo = E.equipmentNo
WHERE REQ.requirementNo = 1;

-- Transaction 3: Employees assigned to requirement #1
SELECT 'TRANSACTION 3: Employees assigned to requirement #1' AS "Query" FROM DUAL;
SELECT 
    EM.fName, 
    EM.lName
FROM ASSIGNED_TO A
JOIN EMPLOYEE EM ON A.employeeNo = EM.employeeNo
WHERE A.requirementNo = 1;

-- Transaction 4: All requirements for client #4
SELECT 'TRANSACTION 4: All requirements for client #4' AS "Query" FROM DUAL;
SELECT 
    requirementNo, 
    sDate, 
    TO_CHAR(sTime, 'HH24:MI') AS sTime, 
    duration
FROM REQUIREMENT
WHERE clientNo = 4
ORDER BY sDate, sTime;

-- Transaction 5: Employees AND equipment for requirement #1
SELECT 'TRANSACTION 5: Employees AND equipment for requirement #1' AS "Query" FROM DUAL;
SELECT 'EMPLOYEE' AS Type, fName AS Name, lName AS Detail
FROM ASSIGNED_TO
JOIN EMPLOYEE USING(employeeNo)
WHERE requirementNo = 1
UNION ALL
SELECT 'EQUIPMENT' AS Type, description AS Name, TO_CHAR(quantity) AS Detail
FROM REQUIRES
JOIN EQUIPMENT USING(equipmentNo)
WHERE requirementNo = 1;
