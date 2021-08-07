import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


# Api works with resources, every resource has to be a class
class Item(Resource):

	# Parser object to parse request
	parser = reqparse.RequestParser()
	# Parser definition
	parser.add_argument(
		'price',
		type=float,
		required=True,
		help="This field cannot be left blank!"
	)

	@jwt_required()
	def get(self, name):
		item = self.find_by_name(name)

		if item:
			return item
		return {'message': 'Item not found'}, 404

	@classmethod
	def find_by_name(cls, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))  # Value must be a tuple, even if it is a single item
		row = result.fetchone()

		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}

	def post(self, name):
		data = self.parser.parse_args()

		if self.find_by_name(name):
			return {'message': f'An item with name {name} already exists.'}, 400

		item = {'name': name, 'price': data['price']}

		# Calls the insert function
		try:
			self.insert(item)
		except Exception as e:
			exception_message = e
			return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error

		return item, 201

	@classmethod
	def insert(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "INSERT INTO items VALUES (?, ?)"
		cursor.execute(query, (item['name'], item['price']))

		connection.commit()
		connection.close()

	def delete(self, name):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "DELETE FROM items WHERE name=?"
		cursor.execute(query, (name,))

		connection.commit()
		connection.close()

		return {'message': 'Item deleted'}

	@jwt_required()
	def put(self, name):
		# This uses the json payload and only uses the arguments defined in the parser argument
		data = self.parser.parse_args()

		item = self.find_by_name(name)

		updated_item = {'name': name, 'price': data['price']}

		if item is None:
			try:
				self.insert(updated_item)
			except Exception as e:
				exception_message = e
				return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error
		else:
			try:
				self.update(updated_item)
			except Exception as e:
				exception_message = e
				return {'message': 'An error occurred updating the item.'}, 500  # Internal server error

		return updated_item

	@classmethod
	def update(cls, item):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "UPDATE items SET price=? WHERE name=?"  # Updates column of item where name matches
		cursor.execute(query, (item['price'], item['name']))

		connection.commit()
		connection.close()


class ItemList(Resource):

	def get(self):
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items"  # Updates column of item where name matches
		result = cursor.execute(query)

		items = []

		for row in result:
			items.append({'name': row[0], 'price': row[1]})

		connection.close()

		return {'items': items}
