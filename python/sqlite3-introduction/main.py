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
    This DB operates in-memory only by default.

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
        """Initializes the database.

        Args:
            location (str, optional): The location of the database.
                Either a .db file or the special :memory: value for an
                in-memory database connection. Defaults to ":memory:".
        """
        self.location = location
        self.table_schemas = {}
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.location)
        self.cursor = self.connection.cursor()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
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
        if not self.cursor:
            raise ValueError("You must use the database as a context manager.")

        if primary_key not in [column for column, _ in schema]:
            raise SchemaError("The provided primary key must be part of the schema.")

        self.table_schemas[table] = schema
        
        columns = ", ".join([f"{column} {sqlite_type.name}" for column, sqlite_type in schema])

        self.cursor.execute(
            f"CREATE TABLE {table} ({columns}, PRIMARY KEY ({primary_key}));"
        )

    def delete(self, table: str, target: Tuple[str, Any]):
        """Deletes rows from the table.

        Args:
            table (str): The table's name.
            target (tuple): What to delete from the table. The tuple consists
                of the column name and the actual value. For example, if you
                wanted to remove the row(s) with the year 1999, you would pass it
                ("year", 1999). Only supports "=" operator in this bite.
        """
        if not self.cursor:
            raise ValueError("You must use the database as a context manager.")

        self.cursor.execute(
            f"DELETE FROM {table} WHERE {target[0]} = ?;", (target[1],)
        )


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
        if not self.cursor:
            raise ValueError("You must use the database as a context manager.")


        schema = self.table_schemas[table]
        columns_count = len(schema)

        for value in values:
            if len(value) != columns_count:
                raise SchemaError(f"Table {table} expects items with {columns_count} values.")

            for (column, column_type), v in zip(schema, value):
                if not isinstance(v, column_type.value):
                    raise SchemaError(f"Column {column} expects values of type {column_type.value.__name__}.")
        
        self.cursor.executemany(
            f"INSERT INTO {table} VALUES ({','.join(['?'] * columns_count)});",
            values,
        )

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
        if not self.cursor:
            raise ValueError("You must use the database as a context manager.")

        if columns is None:
            columns = [column for column, _ in self.table_schemas[table]]

        if target is None:
            self.cursor.execute(f"SELECT {','.join(columns)} FROM {table};")
        else:
            if len(target) == 2:
                target = (target[0], "=", target[1])

            self.cursor.execute(
                f"SELECT {','.join(columns)} FROM {table} WHERE {target[0]} {target[1]} ?;",
                (target[2],),
            )

        return self.cursor.fetchall()

    def update(self, table: str, new_value: Tuple[str, Any], target: Tuple[str, Any]):
        """Update a record in the database.

        Args:
            table (str): The table's name.
            new_value (tuple): The new value that you want to enter. For example,
                if you wanted to change "year" to 2001 you would pass it ("year", 2001).
            target (tuple): The row/record to modify. Example ("year", 1991)
        """
        if not self.cursor:
            raise ValueError("You must use the database as a context manager.")

        self.cursor.execute(
            f"UPDATE {table} SET {new_value[0]} = ? WHERE {target[0]} = ?;",
            (new_value[1], target[1]),
        )

    @property
    def num_transactions(self) -> int:
        """The total number of changes since the database connection was opened.

        Returns:
            int: Returns the total number of database rows that have been modified.
        """
        return self.connection.total_changes if self.connection else 0


NINJAS = [
    ("taspotts", 906),
    ("Tomade", 896),
    ("tasoak", 894),
    ("clamytoe", 890),
]

DB_SCHEMA = [("ninja", SQLiteType.TEXT), ("bitecoins", SQLiteType.INTEGER)]


if __name__ == "__main__":
    db = DB()
    assert db.location == ":memory:"
    assert db.cursor is None
    assert db.connection is None
    assert db.table_schemas == {}

    with DB() as db:
        db.create("ninjas", DB_SCHEMA, "ninja")
        db.insert("ninjas", NINJAS)

    tables = "city", "ninjas"
    schemas = [("name", SQLiteType.TEXT), ("population", SQLiteType.REAL)], DB_SCHEMA
    pks = "name", "ninja"

    for table, schema, pk in zip(tables, schemas, pks):
        with DB() as db:
            assert db.num_transactions == 0
            db.create(table, schema, pk)
            query = f"SELECT name FROM sqlite_master WHERE type= 'table' AND name='{table}';"
            output = db.cursor.execute(query).fetchall()
            assert len(output) == 1
            assert db.num_transactions == 0
