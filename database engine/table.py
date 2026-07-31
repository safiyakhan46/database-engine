from __future__ import annotations

from typing import Any

import index
from exceptions import TypeMismatchError


class Table:
    """
    Represents a database table.
    """

    TYPE_MAP = {
        "INT": int,
        "TEXT": str,
        "FLOAT": float,
    }

    def __init__(
        self,
        name: str,
        columns: list[tuple[str, str]],
    ) -> None:

        self.name = name
        self.columns = columns
        self.rows: list[dict[str, Any]] = []

        # Dictionary of indexes
        self.indexes: dict[str, index.HashIndex] = {}

    def create_index(self, column: str) -> None:
        """
        Create a hash index on a column.
        """

        if column not in [name for name, _ in self.columns]:
            raise ValueError(f"Column '{column}' does not exist.")

        idx = index.HashIndex(column)

        for row in self.rows:
            idx.add(row)

        self.indexes[column] = idx

    def insert(self, values: list[Any]) -> None:

        if len(values) != len(self.columns):
            raise ValueError("Incorrect number of values.")

        row = {}

        for (column_name, column_type), value in zip(
            self.columns,
            values,
        ):

            expected_type = self.TYPE_MAP[column_type]

            if not isinstance(value, expected_type):
                raise TypeMismatchError(
                    f"{column_name} expects {column_type}"
                )

            row[column_name] = value

        self.rows.append(row)

        # Update indexes
        for idx in self.indexes.values():
            idx.add(row)

    def select(
        self,
        where: tuple[str, Any] | None = None,
    ) -> list[dict[str, Any]]:

        if where is None:
            return self.rows.copy()

        column, value = where

        # Use index if available
        if column in self.indexes:
            return self.indexes[column].find(value)

        return [
            row
            for row in self.rows
            if row[column] == value
        ]

    def delete(
        self,
        column: str | None = None,
        value: Any = None,
    ) -> int:

        before = len(self.rows)

        if column is None:
            self.rows = []
        else:
            self.rows = [
                row
                for row in self.rows
                if row[column] != value
            ]

        # Rebuild indexes
        for idx in self.indexes.values():
            idx.mapping.clear()

            for row in self.rows:
                idx.add(row)

        return before - len(self.rows)