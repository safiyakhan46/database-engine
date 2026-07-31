"""
Simple hash-based index for accelerating equality lookups on a column.
"""

from __future__ import annotations

from typing import Any


class HashIndex:
    """
    Maps a column value to the list of rows that contain it,
    turning an O(n) linear scan into an O(1) average-case lookup.
    """

    def __init__(self, column: str) -> None:
        self.column = column
        self.mapping: dict[Any, list[dict[str, Any]]] = {}

    def add(self, row: dict[str, Any]) -> None:
        """
        Register a row under its value for the indexed column.
        """

        value = row[self.column]

        self.mapping.setdefault(value, []).append(row)

    def find(self, value: Any) -> list[dict[str, Any]]:
        """
        Return all rows whose indexed column equals value.
        """

        return list(self.mapping.get(value, []))