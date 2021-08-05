from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

# Create flask app
app = Flask(__name__)
# This should be secret, not hard coded. Using name for learning purposes
app.secret_key = 'george'
# Create an api for flask_restful
api = Api(app)

jwt = JWT(app, authenticate, identity)

# Add resource to api
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# Start app
app.run(port=5000, debug=True)
