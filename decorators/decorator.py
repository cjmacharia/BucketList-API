from functools import wraps
from flask import jsonify, make_response, request
from app.models import User

def auth_token(func):
        """function that wraps a wrapper function"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check for the authentication token
            token = request.headers.get("Authorization")
            if not token:
                # If there's no token provided
                response = {
                    "message": "Register or login to be able to view this page"
                }
                return make_response(jsonify(response)), 401

            else:
                # Attempt to decode the token and get the user id
                access_token = token.split(" ")[1]
                user_id = User.decode_token(access_token)

                if isinstance(user_id, str):
                    # User id does not exist so payload is an error message
                    message = user_id
                    response = jsonify({
                        "message": message
                    })

                    response.status_code = 401
                    return response

                else:
                    return func(user_id=user_id, *args, **kwargs)

        return wrapper
