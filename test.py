import sqlite3

# sqlite3 connection. This uses a file called data.db to store the database
connection = sqlite3.connect('data.db')

# Cursor to interact with db
cursor = connection.cursor()

# Creating and executing query
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# Manually create first user
user = (1, 'george', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?)"

# Executes SQL query on one item
cursor.execute(insert_query, user)

users = [
	(2, 'albert', '1234'),
	(3, 'alphonse', '1234')
]

# Executes SQL query on many items
cursor.executemany(insert_query, users)

# Retrieve items from database
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
	print(row)

# Commit changes
connection.commit()

# Close connection
connection.close()
