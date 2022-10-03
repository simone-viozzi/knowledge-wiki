import sqlite3
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class SQLiteType(Enum):
    """Enum matching SQLite data types to corresponding Python types.

    Supported SQLite types:
        https://docs.python.org/3/library/sqlite3.html#sqlite-and-python-types.

    This Enum is uses in the definition of a table schema to define
        the allowed data type of a column.

    Example: SQLiteType.INTEGER is the ENUM,
        SQLiteType.INTEGER.name is "INTEGER",
        SQLiteType.INTEGER.value is int.
    """

    NULL = None
    INTEGER = int
    REAL = float
    TEXT = str
    BLOB = bytes


class SchemaError(Exception):
    """Base Schema error class if a table schema is not respected."""

    pass


class DB:
    """SQLite Database class.

    Supports all major CRUD operations.
    This DB operates in memory only by default.

    Attributes:
        location (str): The location of the database.
            Either a .db file or the special :memory: value for an
            in-memory database connection.
        connection (sqlite3.Connection): Connection object used to interact with
            the SQLite database.
        cursor (sqlite3.Cursor): Cursor object used to send SQL statements
            to a SQLite database.
        table_schemas (dict): The table schemas of the database.
            The key is the table name and the value is a list of pairs of
            column name and column type.
    """

    def __init__(self, location: Optional[str] = ":memory:"):
        self.location: str = location

        self.connection: sqlite3.Connection = None
        self.cursor: sqlite3.Cursor = None
        self.table_schemas: Dict[str, List[Tuple[str, SQLiteType]]] = {}

    def __enter__(self):
        self.connection = sqlite3.connect(self.location)
        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.close()

    def create(
        self, table: str, schema: List[Tuple[str, SQLiteType]], primary_key: str
    ):
        """Creates a new table.

        Makes use of the SQLiteType enum class.
        Updates the table_schemas attribute.

        You can declare any column of the schema to serve as the primary key by adding
            'primary key' after the column name in the SQL statement.

        If the primary key is not part of the schema,
            a SchemaError should be raised with the message:
            "The provided primary key must be part of the schema."

        Args:
            table (str): The table's name.
            schema (list): A list of columns and their SQLite data types.
                Example: [("make", SQLiteType.TEXT), ("year": SQLiteType.INTEGER)].
            primary_key (str): The primary key column of the provided schema.

        Raises:
            SchemaError: If the given primary key is not part of the schema.
        """
        if primary_key not in (e[0] for e in schema):
            raise SchemaError("The provided primary key must be part of the schema.")

        self.table_schemas[table] = schema

        columns = []
        for name, type_ in schema:
            column = f"{name} {type_.name}"

            if name == primary_key:
                column = f"{column} primary key"

            columns.append(column)

        sql = f"CREATE TABLE {table} ({', '.join(columns)})"
        self._execute(sql)

    def delete(self, table: str, target: Tuple[str, Any]):
        """Deletes rows from the table.

        Args:
            table (str): The table's name.
            target (tuple): What to delete from the table. The tuple consists
                of the column name and the actual value. For example, if you
                wanted to remove the row(s) with the year 1999, you would pass it
                ("year", 1999). Only supports "=" operator in this bite.
        """
        sql = f"DELETE FROM {table} WHERE {target[0]}= ?"
        params = (target[1],)
        self._execute(sql, params)

    def insert(self, table: str, values: List[Tuple]):
        """Inserts one or multiple new records into the database.

        Before inserting a value, you should make sure
            that the schema for the table is respected.

        If there are more or less values than columns,
            a SchemaError should be raised with the message:
            "Table <table-name> expects items with <table-columns-count> values."

        If the type of a value does not respect the type of the column,
            a SchemaError should be raised with the message:
            "Column <column-name> expects values of type <column-type>."

        To add several values with a single command, you might want to look into
            [executemany](https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.executemany)

        Args:
            table (str): The table's name.
            values (list): A list of values to insert.
                Values must respect the table schema.
                The tuple consists of the values for each column in the table.
                Example: [("VW", 2001), ("Tesla", 2020)]

        Raises:
            SchemaError: If a value does not respect the table schema or
                if there are more values than columns for the given table.
        """
        table_schema = self.table_schemas[table]

        values_mismatch = any(
            x != y for x, y in zip(map(len, table_schema), map(len, values))
        )

        if values_mismatch:
            raise SchemaError(
                f"Table {table} expects items with {len(table_schema)} values."
            )

        for entry in values:
            for v, (name, type_) in zip(entry, table_schema):
                if not isinstance(v, type_.value):
                    raise SchemaError(
                        f"Column {name} expects values of type {type_.value.__name__}."
                    )

        placeholders = ", ".join("?" * len(table_schema))
        sql = f"INSERT INTO {table} VALUES ({placeholders})"
        self.cursor.executemany(sql, values)

    def select(
        self,
        table: str,
        columns: Optional[List[str]] = None,
        target: Optional[Tuple[str, Optional[str], Any]] = None,
    ) -> List[Tuple]:
        """Selects records from the database.

        If there are no columns given, select all available columns as default.

        If a target is given, but no operator (length of target < 3), assume equality check.

        Args:
            table (str): The table's name.
            columns (list, optional): List of the column names that you want to retrieve.
                Defaults to None.
            target (tuple, optional): If you want to narrow down the records returned,
                you can specify the column name, the operator and a value to look for.
                Defaults to None. Example: ("year", 1999) <-> ("year", "=", 1999).

        Returns:
            list: The output returned from the sql command
        """
        columns = ["*"] if columns is None else columns

        sql = "SELECT " + ", ".join(columns) + f" FROM {table}"
        params = tuple()

        if target:
            if len(target) == 2:
                target = (target[0], "=", target[1])

            sql += f" WHERE {target[0]} {target[1]} ?"
            params = (target[2],)

        return self._execute(sql, params)

    def update(self, table: str, new_value: Tuple[str, Any], target: Tuple[str, Any]):
        """Update a record in the database.

        Args:
            table (str): The table's name.
            new_value (tuple): The new value that you want to enter. For example,
                if you wanted to change "year" to 2001 you would pass it ("year", 2001).
            target (tuple): The row/record to modify. Example ("year", 1991)
        """
        sql = f"UPDATE {table} SET {new_value[0]}= ? WHERE {target[0]}= ?"
        params = (new_value[1], target[1])
        self._execute(sql, params)

    def _execute(self, sql: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """Executes a SQL command with optional parameters.

        Args:
            sql (str): SQL command to execute
            params (tuple, optional): It is common convention to pass variables into
                SQL commands in this fashion to prevent SQL injection attacks.
                Defaults to None.

        Returns:
            (List): Fetches all (remaining) rows of a query result, returning a list.
                An empty list is returned when no rows are available.
        """
        params = tuple() if params is None else params
        self.cursor.execute(sql, params)

        return self.cursor.fetchall()

    @property
    def num_transactions(self) -> int:
        """The total number of changes since the database connection was opened.

        Returns:
            int: Returns the total number of database rows that have been modified.
        """
        return self.connection.total_changes
