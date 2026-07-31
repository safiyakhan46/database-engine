# Database Engine

A lightweight relational database engine built from scratch in Python to explore the internal design of relational database systems.

This project implements a simplified SQL engine supporting table creation, data manipulation, persistence, and query execution without relying on external database libraries.

Implemented a hash-based indexing system to accelerate equality lookups by maintaining per-column indexes that reduce average query time from linear scans to constant-time dictionary lookups.
---

## Features

- CREATE TABLE
- INSERT
- SELECT
- DELETE
- WHERE filtering
- Persistent JSON storage
- Automatic table loading
- Schema validation
- Type checking
- Interactive SQL shell
- Unit tests

---

## Architecture

```
                SQL Commands
                      │
                      ▼
                SQL Parser
                      │
                      ▼
                 Database
                /         \
             Table     Storage Engine
```

---

## Example

```sql
CREATE TABLE students (
    id INT,
    name TEXT,
    gpa FLOAT
);

INSERT INTO students VALUES (1, "Alice", 3.9);

SELECT * FROM students;

DELETE FROM students WHERE id = 1;
```

---

## Running

```bash
python main.py
```

---

## Running Tests

```bash
python -m unittest discover tests
```

---

## Project Structure

```
database-engine/
├── database.py
├── parser.py
├── storage.py
├── table.py
├── exceptions.py
├── main.py
├── data/
└── tests/
```

---

## Future Improvements

- UPDATE
- DROP TABLE
- ORDER BY
- LIMIT
- SQL Lexer
- Abstract Syntax Tree (AST)
- Hash indexes
- B-Tree indexes
- Transactions
- Query optimisation

---

## Learning Outcomes

Through this project I gained practical experience with:

- Object-Oriented Programming
- Database architecture
- SQL parsing
- File persistence
- Data validation
- Software design
- Unit testing

## Future Improvements

- UPDATE statements
- ORDER BY
- LIMIT
- Hash indexing
- B-Tree indexing
- Transactions
- Query optimization
