"""
tests/test_basic.py — basic tests for CREATE TABLE, INSERT, SELECT, DELETE.

Run with: python -m pytest tests/ -v
(or: python -m unittest tests.test_basic -v)
"""

import os
import shutil
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database import Database


class TestDatabaseEngine(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        self.db = Database(data_dir=self.test_dir)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_table(self):
        result = self.db.execute("CREATE TABLE users (id INT, name TEXT, age INT)")
        self.assertIn("created", result)
        self.assertIn("users", self.db.tables)

    def test_create_duplicate_table_fails(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT)")
        with self.assertRaises(ValueError):
            self.db.execute("CREATE TABLE users (id INT, name TEXT)")

    def test_insert_and_select(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT, age INT)")
        self.db.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
        self.db.execute("INSERT INTO users VALUES (2, 'Bob', 25)")

        rows = self.db.execute("SELECT * FROM users")
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["name"], "Alice")
        self.assertEqual(rows[1]["age"], 25)

    def test_select_with_where(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT, age INT)")
        self.db.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
        self.db.execute("INSERT INTO users VALUES (2, 'Bob', 25)")

        rows = self.db.execute("SELECT * FROM users WHERE id = 1")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Alice")

    def test_delete_with_where(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT, age INT)")
        self.db.execute("INSERT INTO users VALUES (1, 'Alice', 30)")
        self.db.execute("INSERT INTO users VALUES (2, 'Bob', 25)")

        result = self.db.execute("DELETE FROM users WHERE id = 1")
        self.assertIn("1 row(s) deleted", result)

        rows = self.db.execute("SELECT * FROM users")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Bob")

    def test_delete_all(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT)")
        self.db.execute("INSERT INTO users VALUES (1, 'Alice')")
        self.db.execute("INSERT INTO users VALUES (2, 'Bob')")

        result = self.db.execute("DELETE FROM users")
        self.assertIn("2 row(s) deleted", result)
        self.assertEqual(self.db.execute("SELECT * FROM users"), [])

    def test_insert_wrong_column_count_fails(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT)")
        with self.assertRaises(ValueError):
            self.db.execute("INSERT INTO users VALUES (1)")

    def test_data_persists_across_database_instances(self):
        self.db.execute("CREATE TABLE users (id INT, name TEXT)")
        self.db.execute("INSERT INTO users VALUES (1, 'Alice')")

        # simulate restarting the program
        db2 = Database(data_dir=self.test_dir)
        rows = db2.execute("SELECT * FROM users")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["name"], "Alice")


if __name__ == "__main__":
    unittest.main()