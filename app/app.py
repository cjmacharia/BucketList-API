import json
from functools import wraps

from flask import abort, g, jsonify, make_response, request
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

# initialize db
db = SQLAlchemy()

def create_app(config_name):
    """function wraps the creation of a new Flask object, 
    and returns it after it's loaded up with 
    configuration settings using"""

    from models import BucketList, Item, User
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    def auth_token(func):
        @wraps(func)    
        def wrapper(*args, **kwargs):
            # Check for the authentication token
            token = request.headers.get("Authorization")
            if not token:
                # If there's no token provided
                response = {
                    "message": "Register or log in to access this resource"
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
    @app.route("/api/bucketlists/", methods=["POST", "GET"])
    def create_bucketlists():
        if request.method == "POST":
            name = str(request.data.get('name', ''))
            if name:
                bucketlist = BucketList(name=name)
                bucketlist.save()
                response = jsonify({
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                })
                response.status_code = 201
                return response
            else:
                response = jsonify({
                    'you need to fill the name field'
                })
                response.status_code = 403
        else:
            # GET
            allbucketlists = BucketList.get_all()
            # Return the bucket lists
            content = []
            for bucketlist in allbucketlists:
                bucket = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                content.append(bucket)
            response = jsonify(content)
            response.status_code = 200
            return response