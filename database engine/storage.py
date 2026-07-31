"""
Handles saving and loading tables to disk.
"""

from __future__ import annotations

import json
from pathlib import Path

from table import Table


class StorageEngine:
    """
    Handles saving and loading database tables as JSON files.
    """

    def __init__(self, data_directory: str = "data") -> None:
        self.data_directory = Path(data_directory)
        self.data_directory.mkdir(exist_ok=True)

    def save_table(self, table: Table) -> None:
        """
        Save a table to disk.
        """

        filepath = self.data_directory / f"{table.name}.json"

        data = {
            "name": table.name,
            "columns": table.columns,
            "rows": table.rows,
        }

        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load_table(self, table_name: str) -> Table | None:
        """
        Load a table from disk.
        """

        filepath = self.data_directory / f"{table_name}.json"

        if not filepath.exists():
            return None

        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Support older save files that don't contain a "name" field
        table_name = data.get("name", table_name)

        table = Table(
            table_name,
            [tuple(column) for column in data["columns"]],
        )

        table.rows = data["rows"]

        return table

    def list_tables(self) -> list[str]:
        """
        Return all saved tables.
        """

        files = list(self.data_directory.glob("*.json"))

        return [file.stem for file in files]