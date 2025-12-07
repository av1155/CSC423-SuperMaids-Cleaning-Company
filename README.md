# SuperMaids Cleaning Company Database

**CSC 423 - Database Systems**  
**University of Miami**  
**Authors:** Andrea A. Venti Fuentes, Jeremiah Moise  
**Date:** December 07, 2025

---

## Project Overview

This project implements a relational database for SuperMaids Cleaning Company using **Oracle Enterprise DBMS**. The database manages clients, employees, cleaning requirements, equipment, and their relationships.

---

## Database Schema

### Entities

- **CLIENT** - Customer information
- **EMPLOYEE** - Staff information
- **EQUIPMENT** - Cleaning equipment details
- **REQUIREMENT** - Cleaning service schedules
- **REQUIRES** - Junction table linking requirements to equipment
- **ASSIGNED_TO** - Junction table linking employees to requirements

---

## Files in this Repository

### Part 3 Implementation

1. **`supermaids_part3.sql`**
    - Complete Oracle SQL script
    - Creates all tables with constraints (Part 3a)
    - Inserts 5 tuples per table (Part 3b)
    - Contains all 5 transaction queries (Part 3c)

2. **`supermaids_part3.py`**
    - Python implementation with embedded SQL
    - Demonstrates the 5 transaction queries using oracledb driver
    - Requires Oracle database connection

3. **`requirements.txt`**
    - Python dependencies

4. **`script_output.txt`**
    - Execution output demonstrating successful implementation

---

## Usage

### Oracle SQL Script

1. Open [Oracle Live SQL](https://livesql.oracle.com/)
2. Sign in (create free account)
3. Click "SQL Worksheet"
4. Paste entire `supermaids_part3.sql`
5. Click "Run Script"

### Python Script

```bash
# Install dependencies
pip install -r requirements.txt

# Update connection credentials in supermaids_part3.py
# Then run:
python supermaids_part3.py
```

**Note:** Python script requires Oracle database connection credentials (username, password, DSN).

---

## Database Schema Details

### Primary Keys

- CLIENT(clientNo)
- EMPLOYEE(employeeNo)
- EQUIPMENT(equipmentNo)
- REQUIREMENT(requirementNo)
- REQUIRES(requirementNo, equipmentNo)
- ASSIGNED_TO(requirementNo, employeeNo)

### Foreign Keys

- REQUIREMENT.clientNo → CLIENT.clientNo
- REQUIRES.requirementNo → REQUIREMENT.requirementNo
- REQUIRES.equipmentNo → EQUIPMENT.equipmentNo
- ASSIGNED_TO.requirementNo → REQUIREMENT.requirementNo
- ASSIGNED_TO.employeeNo → EMPLOYEE.employeeNo

### Constraints

- All primary keys are NOT NULL by default
- CHECK constraints on salary ≥ 0, cost ≥ 0, duration > 0, quantity > 0
- Required fields marked NOT NULL
- Referential integrity enforced via foreign keys

---

## Transaction Queries

The following 5 queries validate the database design (Part 2c → Part 3c):

1. **Transaction 1:** List all clients and their requirements
2. **Transaction 2:** Equipment needed for a specific requirement
3. **Transaction 3:** Employees assigned to a specific requirement
4. **Transaction 4:** All requirements for a specific client
5. **Transaction 5:** Combined view of employees AND equipment for a requirement

---

## Sample Data

The database includes 5 sample records for each table:

- **5 Clients:** John Smith, Paul Nuttall, Linda Park, Cardboard BoxCo, Maria Lopez
- **5 Employees:** Sarah Johnson, Mike Brown, Emily Clark, George Hill, Olivia Cruz
- **5 Equipment Items:** Industrial Floor Cleaner, Vacuum, Pressure Washer, Scrubber, Steam Cleaner
- **5 Requirements:** Various cleaning schedules for different clients
- **5 Equipment Requirements:** Linking requirements to needed equipment
- **5 Employee Assignments:** Assigning staff to requirements

---

## Normalization

All tables are normalized to **3rd Normal Form (3NF)**:

- 1NF: All attributes are atomic
- 2NF: No partial dependencies (all non-key attributes depend on the entire primary key)
- 3NF: No transitive dependencies

---
