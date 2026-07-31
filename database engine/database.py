"""
Main database engine.
"""

from __future__ import annotations

from exceptions import (
    DuplicateTableError,
    TableNotFoundError,
)
from parser import SQLParser
from storage import StorageEngine
from table import Table


class Database:
    """
    Main database engine.
    """

    def __init__(self, data_dir: str = "data") -> None:

        self.tables: dict[str, Table] = {}

        self.storage = StorageEngine(data_dir)

        self.parser = SQLParser()

        self._load_existing_tables()

    def _load_existing_tables(self) -> None:
        """
        Load all tables from disk.
        """

        for table_name in self.storage.list_tables():

            table = self.storage.load_table(table_name)

            if table is not None:
                self.tables[table_name] = table

    def create_table(
        self,
        name: str,
        columns: list[tuple[str, str]],
    ) -> str:

        if name in self.tables:
            raise DuplicateTableError(
                f"Table '{name}' already exists."
            )

        table = Table(name, columns)

        self.tables[name] = table

        self.storage.save_table(table)

        return f"Table '{name}' created."

    def create_index(
        self,
        table_name: str,
        column: str,
    ) -> str:

        table = self._get_table(table_name)

        table.create_index(column)

        # Save the updated table (including its indexes)
        self.storage.save_table(table)

        return (
            f"Index created on "
            f"{table_name}({column})."
        )

    def insert(
        self,
        table_name: str,
        values: list,
    ) -> str:

        table = self._get_table(table_name)

        table.insert(values)

        self.storage.save_table(table)

        return "1 row(s) inserted."

    def select(
        self,
        table_name: str,
        where=None,
    ) -> list:

        table = self._get_table(table_name)

        return table.select(where)

    def delete(
        self,
        table_name: str,
        column: str | None = None,
        value=None,
    ) -> str:

        table = self._get_table(table_name)

        deleted = table.delete(column, value)

        self.storage.save_table(table)

        return f"{deleted} row(s) deleted."

    def execute(self, sql: str):

        command = self.parser.parse(sql)

        action = command["action"]

        if action == "CREATE":

            return self.create_table(
                command["table"],
                command["columns"],
            )

        if action == "CREATE_INDEX":

            return self.create_index(
                command["table"],
                command["column"],
            )

        if action == "INSERT":

            return self.insert(
                command["table"],
                command["values"],
            )

        if action == "SELECT":

            return self.select(
                command["table"],
                command["where"],
            )

        if action == "DELETE":

            return self.delete(
                command["table"],
                command["column"],
                command["value"],
            )

        raise ValueError("Unknown SQL command.")

    def list_tables(self) -> list[str]:

        return sorted(self.tables.keys())

    def _get_table(self, table_name: str) -> Table:

        if table_name not in self.tables:
            raise TableNotFoundError(
                f"Table '{table_name}' not found."
            )

        return self.tables[table_name]