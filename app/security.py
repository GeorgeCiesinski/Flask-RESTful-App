import hmac
from user import User


# Authenticates user based on above dictionaries
def authenticate(username, password):
	user = User.find_by_username(username)
	# Compares two strings safely
	if user and hmac.compare_digest(user.password, password):
		return user


def identity(payload):
	user_id = payload['identity']
	return User.find_by_id(user_id)
