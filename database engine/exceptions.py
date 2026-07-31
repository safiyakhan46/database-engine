"""
Custom exceptions for the database engine.
"""


class DatabaseError(Exception):
    """Base class for all database exceptions."""
    pass


class DuplicateTableError(DatabaseError):
    """Raised when creating a table that already exists."""
    pass


class TableNotFoundError(DatabaseError):
    """Raised when a requested table does not exist."""
    pass


class SchemaError(DatabaseError):
    """Raised when a schema is invalid."""
    pass


class TypeMismatchError(DatabaseError):
    """Raised when a value doesn't match its column type."""
    pass


class SQLSyntaxError(DatabaseError):
    """Raised when SQL cannot be parsed."""
    pass