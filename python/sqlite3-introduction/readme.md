# SQLite3 introduction

In this Bite, you are going to get some practice playing around with some structured query language (SQL) that's used to work with databases.

If you are not familiar with SQL, a nice little introduction can be found at Digital Ocean.

To solve this Bite, you will use the sqlite3 module. SQLite is a C library that provides a lightweight disk-based database that doesn't require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language.

If you master this Bite, as well as being able to use sqlite3 in your own projects to store data outside the current session, you will be able to use what you have learned about SQL to work with databases like MySQL and PostgreSQL.
Task

Your task is to create a DB class that does some basic CRUD (Create, Read, Update, Delete) operations. You may find it helpful to follow the Digital Ocean tutorial when implementing this class.
DB Class

The class is initialized with just DB() to create an in-memory database but if a file name is given, then the database is saved to that location. You will also need to initialize the class variables connection, cursor and table_schemas.

As the names imply, connection holds the connection to the database, cursor holds the cursor that allows you to send SQL statements to a SQLite database and table_schemas holds the schema for each table (column names and allowed types).

Although you will be adding the option to create an on-file database, your class will be tested only with an in-memory one, so the actual database doesn't really get created on disk.

The class already implements a context manager behavior thanks to the __enter__ and __exit___methods. Thus, you can use the class as a context manager:

with DB() as db:
    db.create(table, schema, primary_key)
    db.insert(table, values)

Class Methods

The skeletons of the methods are supplied for you to flesh out.

- `create()` - Creates a new table
- `delete()` - Deletes a record
- `insert()` - Inserts one or multiple new records
- `select()` - Reads data from a table
- `update()` - Updates a record

As always, feel free to add any helper method that suits you.

Docstrings are provided with all of the above methods to explain their purpose in more detail.
Class Property

There is one property in the class that you will need to implement. It's used to report the total changes made during the connection to the database.

- `num_transactions()` - The total number of changes since the database connection was opened.
Database Schema

There is one addition that was made to this bite that goes beyond the mentioned Digital Ocean tutorial: Database schema.

In a real-world application it is essential to understand and know the database schema because it tells you, among many other things, what the data looks like.

In other words, the schema defines the allowed data types for each table and each column.

In this Bite a schema is passed as second argument to the create() method to tell the DB class the allowed column types for each column.

Therefore, a schema is a list of tuples of pairs of column name and column type. SQLite 3 supports certain types and each type has a corresponding type in Python 3. For example, the SQLite type INTEGER maps to the Python type int.

You are given an enumeration class SQLiteType that you can use to translate between the two worlds, SQLite and Python. The idea is that you have to limit the choice for a column type to the entries of this enumeration.

To use this class, you can access the items per dot notation, as demonstrated in the docstrings of the create() method:

```python
[("make", SQLiteType.TEXT), ("year": SQLiteType.INTEGER)]
```

To access the name of an enumeration, use the name property:  SQLiteType.INTEGER.name. This will return the string "INTEGER".

To access the value of an enumeration, use the value property: SQLiteType.INTEGER.value.

This will return the value, in this case the Python type int.

You need this information to finish the insert() method because you are expected to raise a SchemaError exception (also provided in the template) whenever someone calls the insert() method with the wrong number of values (less or more values than columns) or the wrong type as defined in the table schema.
Primary Key

Another common concept for dealing with databases is the concept of primary keys (you are not dealing with foreign keys in this Bite).

Simply put, a primary key is the column that serves as primary identification column for its table and each entry (row) must have a unique and valid value for this primary key. In most databases, if no primary key is specified, the database creates a unique ID column that serves this purpose. However, in this bite, the primary key is explicitly given as the third argument of the create() method.

For the create() method, you have to make sure that the primary key is part of the table schema, so there must be a column that matches the primary key.
Test Data

The tests rely on a small table with brave pybite ninjas:

|ninja | bitecoins|
|------|----------|
|taspotts | 906|
|Tomade | 896|
|tasoak | 894|
|clamytoe | 890|

The first column ninja is of type TEXT and the second column bitecoins is of type INTEGER.

The column ninja is the primary key for this table.

To create this table with the provided DB class, the following code will be used:

```python
NINJAS = [
    ("taspotts", 906),
    ("Tomade", 896),
    ("tasoak", 894),
    ("clamytoe", 890),
]
DB_SCHEMA = [("ninja", SQLiteType.TEXT), ("bitecoins", SQLiteType.INTEGER)]

with DB() as db:
    db.create("ninjas", DB_SCHEMA, "ninja")
    db.insert("ninjas", NINJAS)
```
