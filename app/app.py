from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Create flask app
app = Flask(__name__)
# This should be secret, not hard coded. Using name for learning purposes
app.secret_key = 'george'
# Create an api for flask_restful
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


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
		# Filter takes two things: (filtering function, list to filter)
		item = next(filter(lambda x: x['name'] == name, items), None)  # Next gives us the first item in the filter object
		return {'item': item}, 200 if item else 404  # Ternary if statement

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


# Add resource to api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# Start app
app.run(port=5000, debug=True)
