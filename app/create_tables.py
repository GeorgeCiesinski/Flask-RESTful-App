import sqlite3

connection = sqlite3.connect('data.db')  # Database connection
cursor = connection.cursor()  # Interacts with db

# SQL Query: Create users table if doesn't exist
# INTEGER PRIMARY KEY tells the db to auto increment. Normally we can use int for this data type.
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

# real is a decimal type in SQL
create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

connection.commit()

connection.close()