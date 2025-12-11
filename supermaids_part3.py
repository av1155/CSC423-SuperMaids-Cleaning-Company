"""
SuperMaids Cleaning Company Database
CSC 423 - Database Systems - Part 3
Embedded SQL Implementation in Python (SQLite)
Andrea A. Venti Fuentes, Jeremiah Moise
University of Miami
December 07, 2025
"""

import sqlite3
import os

# ============================================================
# DATABASE CONNECTION
# ============================================================
# SQLite creates the database file automatically if it doesn't exist

DB_FILE = "supermaids.db"

# Remove existing database to start fresh
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

try:
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()
    
    # Enable foreign key support (off by default in SQLite)
    cursor.execute("PRAGMA foreign_keys = ON")
    
    print("Successfully connected to SQLite Database")
    print(f"Database file: {DB_FILE}\n")

except sqlite3.Error as error:
    print(f"Error connecting to SQLite: {error}")
    exit(1)

# ============================================================
# CREATE TABLES
# ============================================================

print("=" * 70)
print("CREATING DATABASE SCHEMA")
print("=" * 70)

# Drop tables if they exist (in correct order due to foreign keys)
cursor.execute("DROP TABLE IF EXISTS ASSIGNED_TO")
cursor.execute("DROP TABLE IF EXISTS REQUIRES")
cursor.execute("DROP TABLE IF EXISTS REQUIREMENT")
cursor.execute("DROP TABLE IF EXISTS EQUIPMENT")
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
cursor.execute("DROP TABLE IF EXISTS CLIENT")

# Create CLIENT table
cursor.execute("""
    CREATE TABLE CLIENT (
        clientNo        INTEGER PRIMARY KEY,
        fName           TEXT NOT NULL,
        lName           TEXT NOT NULL,
        address         TEXT NOT NULL,
        telephoneNo     TEXT NOT NULL
    )
""")
print("Table CLIENT created.")

# Create EMPLOYEE table
cursor.execute("""
    CREATE TABLE EMPLOYEE (
        employeeNo      INTEGER PRIMARY KEY,
        fName           TEXT NOT NULL,
        lName           TEXT NOT NULL,
        address         TEXT NOT NULL,
        salary          REAL NOT NULL CHECK (salary >= 0),
        telephoneNo     TEXT NOT NULL
    )
""")
print("Table EMPLOYEE created.")

# Create EQUIPMENT table
cursor.execute("""
    CREATE TABLE EQUIPMENT (
        equipmentNo     INTEGER PRIMARY KEY,
        description     TEXT NOT NULL,
        usage           TEXT,
        cost            REAL NOT NULL CHECK (cost >= 0)
    )
""")
print("Table EQUIPMENT created.")

# Create REQUIREMENT table
cursor.execute("""
    CREATE TABLE REQUIREMENT (
        requirementNo   INTEGER PRIMARY KEY,
        clientNo        INTEGER NOT NULL,
        sDate           TEXT NOT NULL,
        sTime           TEXT NOT NULL,
        duration        INTEGER NOT NULL CHECK (duration > 0),
        comments        TEXT,
        FOREIGN KEY (clientNo) REFERENCES CLIENT(clientNo)
    )
""")
print("Table REQUIREMENT created.")

# Create REQUIRES table
cursor.execute("""
    CREATE TABLE REQUIRES (
        requirementNo   INTEGER NOT NULL,
        equipmentNo     INTEGER NOT NULL,
        quantity        INTEGER NOT NULL CHECK (quantity > 0),
        PRIMARY KEY (requirementNo, equipmentNo),
        FOREIGN KEY (requirementNo) REFERENCES REQUIREMENT(requirementNo),
        FOREIGN KEY (equipmentNo) REFERENCES EQUIPMENT(equipmentNo)
    )
""")
print("Table REQUIRES created.")

# Create ASSIGNED_TO table
cursor.execute("""
    CREATE TABLE ASSIGNED_TO (
        requirementNo   INTEGER NOT NULL,
        employeeNo      INTEGER NOT NULL,
        PRIMARY KEY (requirementNo, employeeNo),
        FOREIGN KEY (requirementNo) REFERENCES REQUIREMENT(requirementNo),
        FOREIGN KEY (employeeNo) REFERENCES EMPLOYEE(employeeNo)
    )
""")
print("Table ASSIGNED_TO created.")

# ============================================================
# INSERT SAMPLE DATA
# ============================================================

print("\n" + "=" * 70)
print("INSERTING SAMPLE DATA")
print("=" * 70)

# CLIENT data
clients = [
    (1, 'John', 'Smith', '100 Main St', '305-111-1111'),
    (2, 'Paul', 'Nuttall', '22 Orange Ave', '305-222-2222'),
    (3, 'Linda', 'Park', '77 Sunset Blvd', '305-333-3333'),
    (4, 'Cardboard', 'BoxCo', '88 Industrial Rd', '305-444-4444'),
    (5, 'Maria', 'Lopez', '55 Coral Way', '305-555-5555')
]
cursor.executemany("INSERT INTO CLIENT VALUES (?, ?, ?, ?, ?)", clients)
print(f"Inserted {len(clients)} rows into CLIENT.")

# EMPLOYEE data
employees = [
    (1, 'Sarah', 'Johnson', '12 Pine St', 42000, '305-999-1111'),
    (2, 'Mike', 'Brown', '8 Oak St', 41000, '305-999-2222'),
    (3, 'Emily', 'Clark', '20 Palm Dr', 45000, '305-999-3333'),
    (4, 'George', 'Hill', '9 Birch Rd', 39000, '305-999-4444'),
    (5, 'Olivia', 'Cruz', '3 Maple Ave', 47000, '305-999-5555')
]
cursor.executemany("INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?, ?, ?)", employees)
print(f"Inserted {len(employees)} rows into EMPLOYEE.")

# EQUIPMENT data
equipment = [
    (1, 'Industrial Floor Cleaner', 'Floor deep clean', 200),
    (2, 'Vacuum', 'Standard vacuum cleaning', 50),
    (3, 'Pressure Washer', 'Outdoor cleaning', 150),
    (4, 'Scrubber', 'Tile scrubbing', 120),
    (5, 'Steam Cleaner', 'Carpet steaming', 180)
]
cursor.executemany("INSERT INTO EQUIPMENT VALUES (?, ?, ?, ?)", equipment)
print(f"Inserted {len(equipment)} rows into EQUIPMENT.")

# REQUIREMENT data
requirements = [
    (1, 4, '2025-01-02', '07:00', 120, 'Morning shift'),
    (2, 4, '2025-01-02', '17:00', 120, 'Evening shift'),
    (3, 2, '2025-01-05', '10:00', 180, 'Weekly clean'),
    (4, 1, '2025-01-08', '09:00', 90, 'Deep clean'),
    (5, 3, '2025-01-11', '14:00', 120, 'General clean')
]
cursor.executemany("INSERT INTO REQUIREMENT VALUES (?, ?, ?, ?, ?, ?)", requirements)
print(f"Inserted {len(requirements)} rows into REQUIREMENT.")

# REQUIRES data
requires = [
    (1, 1, 3),
    (1, 2, 2),
    (2, 1, 1),
    (3, 5, 1),
    (4, 4, 1)
]
cursor.executemany("INSERT INTO REQUIRES VALUES (?, ?, ?)", requires)
print(f"Inserted {len(requires)} rows into REQUIRES.")

# ASSIGNED_TO data
assigned = [
    (1, 1),
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5)
]
cursor.executemany("INSERT INTO ASSIGNED_TO VALUES (?, ?)", assigned)
print(f"Inserted {len(assigned)} rows into ASSIGNED_TO.")

connection.commit()
print("\nAll data committed to database.")

# ============================================================
# PART 3(c): EMBEDDED SQL QUERIES
# These correspond to the 5 transactions validated in Part 2c
# ============================================================

print("\n" + "=" * 70)
print("PART 3(c): EMBEDDED SQL TRANSACTIONS")
print("=" * 70)

# ------------------------------------------------------------
# Transaction 1: List all clients and their requirements
# ------------------------------------------------------------
print("\nTransaction 1: List all clients and their requirements")
print("-" * 70)

cursor.execute("""
    SELECT 
        C.fName, 
        C.lName, 
        R.requirementNo, 
        R.sDate, 
        R.sTime
    FROM CLIENT C
    JOIN REQUIREMENT R ON C.clientNo = R.clientNo
    ORDER BY C.lName, R.sDate
""")

print(f"{'Client Name':<25} {'Req#':<8} {'Date':<12} {'Time':<8}")
print("-" * 70)
for row in cursor.fetchall():
    fname, lname, req_no, s_date, s_time = row
    print(f"{fname} {lname:<20} {req_no:<8} {s_date:<12} {s_time:<8}")

# ------------------------------------------------------------
# Transaction 2: Equipment needed for requirement #1
# ------------------------------------------------------------
print("\n\nTransaction 2: Equipment needed for requirement #1")
print("-" * 70)

cursor.execute("""
    SELECT 
        E.description, 
        REQ.quantity
    FROM REQUIRES REQ
    JOIN EQUIPMENT E ON REQ.equipmentNo = E.equipmentNo
    WHERE REQ.requirementNo = 1
""")

print(f"{'Equipment':<35} {'Quantity':<10}")
print("-" * 70)
for row in cursor.fetchall():
    description, quantity = row
    print(f"{description:<35} {quantity:<10}")

# ------------------------------------------------------------
# Transaction 3: Employees assigned to requirement #1
# ------------------------------------------------------------
print("\n\nTransaction 3: Employees assigned to requirement #1")
print("-" * 70)

cursor.execute("""
    SELECT 
        EM.fName, 
        EM.lName
    FROM ASSIGNED_TO A
    JOIN EMPLOYEE EM ON A.employeeNo = EM.employeeNo
    WHERE A.requirementNo = 1
""")

print(f"{'Employee Name':<30}")
print("-" * 70)
for row in cursor.fetchall():
    fname, lname = row
    print(f"{fname} {lname:<25}")

# ------------------------------------------------------------
# Transaction 4: All requirements for client #4
# ------------------------------------------------------------
print("\n\nTransaction 4: All requirements for client #4")
print("-" * 70)

cursor.execute("""
    SELECT 
        requirementNo, 
        sDate, 
        sTime, 
        duration
    FROM REQUIREMENT
    WHERE clientNo = 4
    ORDER BY sDate, sTime
""")

print(f"{'Req#':<8} {'Date':<12} {'Time':<8} {'Duration (min)':<15}")
print("-" * 70)
for row in cursor.fetchall():
    req_no, s_date, s_time, duration = row
    print(f"{req_no:<8} {s_date:<12} {s_time:<8} {duration:<15}")

# ------------------------------------------------------------
# Transaction 5: Employees AND equipment for requirement #1
# ------------------------------------------------------------
print("\n\nTransaction 5: Employees AND equipment for requirement #1")
print("-" * 70)

cursor.execute("""
    SELECT 'EMPLOYEE' AS Type, fName AS Name, lName AS Detail
    FROM ASSIGNED_TO
    JOIN EMPLOYEE USING(employeeNo)
    WHERE requirementNo = 1
    UNION ALL
    SELECT 'EQUIPMENT' AS Type, description AS Name, CAST(quantity AS TEXT) AS Detail
    FROM REQUIRES
    JOIN EQUIPMENT USING(equipmentNo)
    WHERE requirementNo = 1
""")

print(f"{'Type':<12} {'Name':<30} {'Detail':<20}")
print("-" * 70)
for row in cursor.fetchall():
    type_val, name, detail = row
    print(f"{type_val:<12} {name:<30} {detail:<20}")

# ============================================================
# CLEANUP
# ============================================================
cursor.close()
connection.close()
print("\n" + "=" * 70)
print("Database connection closed successfully")
print("=" * 70)
