
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
    configuration settings """

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
              
        
    @app.route('/api/bucketlists/auth/register/', methods=["POST"])
    def register_user():
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if email is None:
            response = jsonify({'error': 'email field cannot be blank'})
            response.status_code = 401
            return response
        elif username is None:
            response = jsonify({'error': 'name field cannot be blank'})
            response.status_code = 401
            return response
        elif password is None:
            response = jsonify ({'error': 'password field has to be field'})
            response.status_code = 401
            return response
        elif User.query.filter_by(email = email).first() is not None:
            response = jsonify({'error': 'user already exists'})
            # return conflict error 
            response.status_code = 409 
            return response
        else:
            user = User(username=username, password=password,
                                    email=email)
            user.save()
            response = jsonify({'message': 'welcome loggen in user'
            })
            #users created successfully 
            response.status_code = 201 
            return response

    @app.route('/api/bucketlists/auth/login/', methods=['POST'])
    def login():
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.query.filter_by(email = email).first()
        if user and user.password_is_valid(password):
            token = user.token_generate(user.id)
            if token:
                    response = jsonify({
                        "message": "You logged in successfully.",
                        "access_token": token.decode()
                    })

                    response.status_code = 200
                    return response
            else:
                response = jsonify({
                    "message":"An authorization error occured please try again"
                })
                response.status_code = 401 
                return response 
        else:
            response = jsonify({
                "message":"wrong credentials "
            })
            response.status_code = 401 
            return response
    
    @app.route("/api/bucketlists/", methods=["POST", "GET"])
    @auth_token
    def create_bucketlists(user_id):
        if request.method == "POST":
            name = str(request.data.get('name'))
            if name:
                bucketlist = BucketList(name=name, created_by=user_id)
                bucketlist.save()
                response = jsonify({
                    'message': "bucketlist successfully added"
                    
                })
                response.status_code = 201
                return response
            else:
                response = jsonify({
                    'you need to fill the name field'
                })
                response.status_code = 403
        else:
            content = []
            allbucketlists = BucketList.get_all(user_id)
            for bucketlist in allbucketlists:
                bucket = {
                    'id': bucketlist.id,
                    'name': bucketlist.name,
                    'date_created': bucketlist.date_created,
                    'date_modified': bucketlist.date_modified
                }
                content.append(bucket)
            print(content)
            if  len(content) == 0:
                response = jsonify({
                "error":"No bucketlists"
                })        
                response.status_code = 404
                return response
            else:
                # Return the bucket lists                
                response = jsonify(content)
                response.status_code = 200
                return response
                

    @app.route('/api/bucketlists/<int:bid>/', methods=['GET', 'PUT', 'DELETE'])
    @auth_token
    def bucketlist_manipulation(bid, user_id):
     # retrieve a buckelist using it's ID
        bucketlist = BucketList.query.filter_by(id=bid, created_by=user_id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            response = jsonify({
                'message':'the bucketlist doesnot exist'
            })
            response.status_code = 404
            return response 

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
            "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
         }, 200

        elif request.method == 'PUT':
            name = request.data.get('name')
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                "message":"Successfully updated"
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response


    @app.route("/api/bucketlists/<int:id>/items/", methods=["POST", "GET"])
    @auth_token
    def create_items(id,user_id,*args, **kwargs):
        """create a bucket item """
        bucketlist = BucketList.query.filter_by(id=id).first()
        if not bucketlist:
            abort(404)

        if request.method == "POST":
            name = request.data.get("name")
           
            if  BucketList.query.filter_by(name = name).first() is not None:
                response = jsonify({'name':'The item already exist'})
                response.status_code = 403
                return response
                
            elif name != '':
                item = Item(name=name, bucketlist_id=id)
                item.save()
                response = jsonify({
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id,
                    })

                response.status_code = 201
                return response
            else:
                response = jsonify({
                    'message': 'oops! you need to fill the name field'
                })
                response.status_code = 403
                return response
                
        elif request.method == "GET":
            items = Item.query.filter_by(bucketlist_id=id)
            results = []

            for item in items:
                obj = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id,
                }
                results.append(obj)
            return make_response(jsonify(results)), 200
            

    @app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["PUT"])  
    @auth_token  
    def update_item(bid, item_id,user_id,*args, **kwargs):
        item = Item.query.filter_by(bucketlist_id=bid).filter_by(
                    id=item_id).first()
    
        if not item:
            abort(404)

        if request.method == "PUT":
            name = request.data.get('name')
            if name:
                item.name = name
                item.save()
                response = jsonify({
                    "message":"item successfuly updated"
                })
                response.status_code = 200
                return response
            else:
                response = jsonify({
                    'message': 'oops! you need to fill the name field'
                })
                response.status_code = 403
                return response 
        else:
            response = jsonify({
                'message':'an error ocuured try again'
            })
    @app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["DELETE"])  
    @auth_token  
    def delete_item(bid, item_id,user_id,*args, **kwargs):
        item = Item.query.filter_by(bucketlist_id=bid).filter_by(
                    id=item_id).first() 
        if not item:
            abort(404)
                   
        if request.method == "DELETE":
            item.delete()
            response = jsonify({
                "message": "Item {} has been successfully deleted"
                .format(item.name)})
            response.status_code = 200
            return response
                
    
    @app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["GET"])  
    @auth_token  
    def get_item(bid, item_id,user_id,*args, **kwargs):
        item = Item.query.filter_by(bucketlist_id=bid).filter_by(
                    id=item_id).first()   
        if not item:
            abort(404)
                  
        if request.method == "GET":
            all_items = Item.query.filter_by(id=item_id)
            results = []

            for item in all_items:
                obj = {
                    "id": item.id,
                    "name": item.name,
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id,
                }
                results.append(obj)
                return make_response(jsonify(results)), 200

                        


    return app
