from flask import Flask
from flask_restful import Resource, Api


# Create flask app
app = Flask(__name__)

# Create an api for flask_restful
api = Api(app)


# Api works with resources, every resource has to be a class
class Student(Resource):

	def get(self, name):
		return {'student': name}

# Add resource to api
api.add_resource(Student, '/student/<string:name>')  # http://127.0.0.1:5000/student/Bob

# Start app
app.run(port=5000)
