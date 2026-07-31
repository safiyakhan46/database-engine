"""
Very small SQL parser.
Supports:
CREATE TABLE
CREATE INDEX
INSERT
SELECT
DELETE
"""

from __future__ import annotations

import ast
import re

from exceptions import SQLSyntaxError


class SQLParser:

    CREATE_PATTERN = re.compile(
        r"CREATE TABLE (\w+)\s*\((.+)\)",
        re.IGNORECASE,
    )

    CREATE_INDEX_PATTERN = re.compile(
        r"CREATE INDEX \w+ ON (\w+)\((\w+)\)",
        re.IGNORECASE,
    )

    INSERT_PATTERN = re.compile(
        r"INSERT INTO (\w+)\s*VALUES\s*\((.+)\)",
        re.IGNORECASE,
    )

    SELECT_PATTERN = re.compile(
        r"SELECT \* FROM (\w+)(?: WHERE (\w+)\s*=\s*(.+))?",
        re.IGNORECASE,
    )

    DELETE_PATTERN = re.compile(
        r"DELETE FROM (\w+)(?:\s*WHERE (\w+)\s*=\s*(.+))?",
        re.IGNORECASE,
    )

    def parse(self, sql: str) -> dict:

        sql = sql.strip().rstrip(";")

        # CREATE TABLE
        if match := self.CREATE_PATTERN.fullmatch(sql):

            table = match.group(1)
            column_text = match.group(2)

            columns = []

            for definition in column_text.split(","):

                name, datatype = definition.strip().split()

                columns.append(
                    (name, datatype.upper())
                )

            return {
                "action": "CREATE",
                "table": table,
                "columns": columns,
            }

        # CREATE INDEX
        if match := self.CREATE_INDEX_PATTERN.fullmatch(sql):

            return {
                "action": "CREATE_INDEX",
                "table": match.group(1),
                "column": match.group(2),
            }

        # INSERT
        if match := self.INSERT_PATTERN.fullmatch(sql):

            table = match.group(1)

            values = ast.literal_eval(
                "(" + match.group(2) + ",)"
            )

            return {
                "action": "INSERT",
                "table": table,
                "values": list(values),
            }

        # SELECT
        if match := self.SELECT_PATTERN.fullmatch(sql):

            table = match.group(1)

            if match.group(2):

                return {
                    "action": "SELECT",
                    "table": table,
                    "where": (
                        match.group(2),
                        ast.literal_eval(match.group(3)),
                    ),
                }

            return {
                "action": "SELECT",
                "table": table,
                "where": None,
            }

        # DELETE
        if match := self.DELETE_PATTERN.fullmatch(sql):

            column = match.group(2)

            value = (
                ast.literal_eval(match.group(3))
                if match.group(3) is not None
                else None
            )

            return {
                "action": "DELETE",
                "table": match.group(1),
                "column": column,
                "value": value,
            }

        raise SQLSyntaxError("Invalid SQL.")