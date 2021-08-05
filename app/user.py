import sqlite3
from flask_restful import Resource, reqparse


class User:
	def __init__(self, _id, username, password):
		self.id = _id
		self.username = username
		self.password = password

	@classmethod
	def find_by_username(cls, username):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE username=?"
		# To execute queries, execute requires a tuple. Single item tuple must have comma.
		result = cursor.execute(query, (username,))

		# Get first row out of result set
		row = result.fetchone()
		if row:
			# Pass row[0], row[1], row [2]. * extracts ordered fields.
			user = cls(*row)
		else:
			user = None

		# Close connection once done
		connection.close()

		return user

	@classmethod
	def find_by_id(cls, _id):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM users WHERE id=?"
		# To execute queries, execute requires a tuple. Single item tuple must have comma.
		result = cursor.execute(query, (_id,))

		# Get first row out of result set
		row = result.fetchone()
		if row:
			# Pass row[0], row[1], row [2]. * extracts ordered fields.
			user = cls(*row)
		else:
			user = None

		# Close connection once done
		connection.close()

		return user


class UserRegister(Resource):

	parser = reqparse.RequestParser()  # Parser object

	# Username Parser
	parser.add_argument(
		'username',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)

	# Password parser
	parser.add_argument(
		'password',
		type=str,
		required=True,
		help="This field cannot be left blank!"
	)

	def post(self):
		"""
		Registers a new user and posts the new User object to the database.

		:return: message, http status
		"""

		# Parse json
		data = UserRegister.parser.parse_args()

		# Checks if user already exists
		if User.find_by_username(data['username']):
			return {"message": "A user with that username already exists"}, 400

		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		# Query to insert users. First value is NULL because of autoincrement.
		query = "INSERT INTO users VALUES (NULL, ?, ?)"
		cursor.execute(query, (data['username'], data['password']))

		connection.commit()
		connection.close()

		return {"message": "User created successfully."}, 201
