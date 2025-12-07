"""
SuperMaids Cleaning Company Database
CSC 423 - Database Systems - Part 3
Embedded SQL Implementation in Python
Andrea A. Venti Fuentes, Jeremiah Moise
University of Miami
December 07, 2025
"""

import oracledb

# ============================================================
# DATABASE CONNECTION
# ============================================================
# IMPORTANT: Update these credentials for an Oracle database
# Format: username/password@hostname:port/service_name

# Example connection strings:
# Local Oracle XE: "username/password@localhost:1521/XEPDB1"
# Oracle Cloud: "username/password@hostname:1521/service_name"

try:
    # Credentials
    username = "your_username"
    password = "your_password"
    dsn = "localhost:1521/XEPDB1"

    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    print("Successfully connected to Oracle Database\n")

except oracledb.Error as error:
    print(f"Error connecting to Oracle: {error}")
    exit(1)

# ============================================================
# PART 3(c): EMBEDDED SQL QUERIES
# These correspond to the 5 transactions validated in Part 2c
# ============================================================

print("=" * 70)
print("PART 3(c): EMBEDDED SQL TRANSACTIONS")
print("=" * 70)

# ------------------------------------------------------------
# Transaction 1: List all clients and their requirements
# ------------------------------------------------------------
print("\nTransaction 1: List all clients and their requirements")
print("-" * 70)

cursor.execute(
    """
    SELECT 
        C.fName, 
        C.lName, 
        R.requirementNo, 
        R.sDate, 
        TO_CHAR(R.sTime, 'HH24:MI') AS sTime
    FROM CLIENT C
    JOIN REQUIREMENT R ON C.clientNo = R.clientNo
    ORDER BY C.lName, R.sDate
"""
)

print(f"{'Client Name':<25} {'Req#':<8} {'Date':<12} {'Time':<8}")
print("-" * 70)
for row in cursor.fetchall():
    fname, lname, req_no, s_date, s_time = row
    print(
        f"{fname} {lname:<20} {req_no:<8} {s_date.strftime('%Y-%m-%d'):<12} {s_time:<8}"
    )

# ------------------------------------------------------------
# Transaction 2: Equipment needed for requirement #1
# ------------------------------------------------------------
print("\n\nTransaction 2: Equipment needed for requirement #1")
print("-" * 70)

cursor.execute(
    """
    SELECT 
        E.description, 
        REQ.quantity
    FROM REQUIRES REQ
    JOIN EQUIPMENT E ON REQ.equipmentNo = E.equipmentNo
    WHERE REQ.requirementNo = 1
"""
)

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

cursor.execute(
    """
    SELECT 
        EM.fName, 
        EM.lName
    FROM ASSIGNED_TO A
    JOIN EMPLOYEE EM ON A.employeeNo = EM.employeeNo
    WHERE A.requirementNo = 1
"""
)

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

cursor.execute(
    """
    SELECT 
        requirementNo, 
        sDate, 
        TO_CHAR(sTime, 'HH24:MI') AS sTime, 
        duration
    FROM REQUIREMENT
    WHERE clientNo = 4
    ORDER BY sDate, sTime
"""
)

print(f"{'Req#':<8} {'Date':<12} {'Time':<8} {'Duration (min)':<15}")
print("-" * 70)
for row in cursor.fetchall():
    req_no, s_date, s_time, duration = row
    print(f"{req_no:<8} {s_date.strftime('%Y-%m-%d'):<12} {s_time:<8} {duration:<15}")

# ------------------------------------------------------------
# Transaction 5: Employees AND equipment for requirement #1
# ------------------------------------------------------------
print("\n\nTransaction 5: Employees AND equipment for requirement #1")
print("-" * 70)

cursor.execute(
    """
    SELECT 'EMPLOYEE' AS Type, fName AS Name, lName AS Detail
    FROM ASSIGNED_TO
    JOIN EMPLOYEE USING(employeeNo)
    WHERE requirementNo = 1
    UNION ALL
    SELECT 'EQUIPMENT' AS Type, description AS Name, TO_CHAR(quantity) AS Detail
    FROM REQUIRES
    JOIN EQUIPMENT USING(equipmentNo)
    WHERE requirementNo = 1
"""
)

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
