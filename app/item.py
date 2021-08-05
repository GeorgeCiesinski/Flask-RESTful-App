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
		connection = sqlite3.connect('data.db')
		cursor = connection.cursor()

		query = "SELECT * FROM items WHERE name=?"
		result = cursor.execute(query, (name,))  # Value must be a tuple, even if it is a single item
		row = result.fetchone()

		connection.close()

		if row:
			return {'item': {'name': row[0], 'price': row[1]}}
		return {'message': 'Item not found'}, 404

	def post(self, name):

		if next(filter(lambda x: x['name'] == name, items), None):
			return {'message': f'An item with name {name} already exists.'}, 400

		data = Item.parser.parse_args()

		item = {'name': name, 'price': data['price']}
		items.append(item)
		return items, 201

	def delete(self, name):
		global items
		items = list(filter(lambda x: x['name'] != name, items))
		return {'message': 'Item deleted'}

	@jwt_required()
	def put(self, name):

		item = next(filter(lambda x: x['name'] == name, items), None)

		# This uses the json payload and only uses the arguments defined in the parser argument
		data = Item.parser.parse_args()

		# If Item doesn't exist, create a new item from the data payload
		if item is None:
			item = {'name': name, 'price': data['price']}
			items.append(item)
		# If Item exists, update from data payload
		else:
			item.update(data)  # Dicts have an update method
		return item


class ItemList(Resource):

	def get(self):
		return {'items': items}
