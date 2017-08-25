from functools import wraps
from flask import abort, jsonify, make_response, request
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
import re
# local import
from instance.config import app_config

#pylint: disable=C0103
# initialize db
db = SQLAlchemy()


def create_app(config_name):
    """function wraps the creation of a new Flask object,
    and returns it after it's loaded up with
    configuration settings """

    from .models import BucketList, Item, User
    from .decorator import auth_token

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #pylint: disable=unused-argument
    #pylint: disable=unused-variable
    @app.route('/api/bucketlists/auth/register/', methods=["POST"])
    def register_user():
        '''
        This endpoint uses the post request method to add users in your database.
        It acceps data in json format with username and password as keys.
        '''
        username = str(request.data.get('username'))
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if email == "":
            response = jsonify({'error': 'email field cannot be blank'})
            response.status_code = 400
            return response
        elif not re.match(regex, email):
            response = jsonify({
                'error':'the email need to be a valid email'
            })
            response.status_code = 403
            return response

        elif username == "":
            response = jsonify({'error': 'username field cannot be blank'})
            response.status_code = 400
            return response
        elif not re.match("^[a-zA-Z0-9_]*$", username):
            response = jsonify({'error':
                                'Username cannot contain special characters'})
            response.status_code = 403
            return response
        elif password == "":
            response = jsonify({'error': 'password field has to be field'})
            response.status_code = 400
            return response
        elif len(password) < 5:
            response = jsonify({'error':
                                'Password should be more than 5 characters'})
            response.status_code = 403
            return response
        elif User.query.filter_by(email=email).first() is not None:
            response = jsonify({'error': 'user already exists'})
            # return conflict error
            response.status_code = 409
            return response
        else:
            user = User(username=username, password=password, email=email)
            user.save()
            response = jsonify({'message': 'welcome loggen in user'})
            #users created successfully
            response.status_code = 201
            return response

    @app.route('/api/bucketlists/auth/login/', methods=['POST'])
    def login():
        '''
        Accepts user crendtials and generates a jwt token for each user.
        The token expires after an hour. This can be adjusted by setting
        the 'exp'private Claim to whatever timeout you prefer.
        '''
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))
        user = User.query.filter_by(email=email).first()
        if user and user.password_is_valid(password):
            token = user.token_generate(user.id)
            if token:
                response = jsonify({
                    "message": "You logged in successfully.",
                    "access_token": token.decode()})
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
    def create_bucketlists(user_id, *args, **kwargs):
        '''
        This endpoint creates a new bucketlist for the user.
        '''
        if request.method == "POST":
            name = request.data.get('name')
            if name == "":
                response = jsonify({
                    'message':'you need to fill the name field'
                })
                response.status_code = 403
                return response

            elif name:
                stripped_name = name.strip()
                name = stripped_name
                if len(stripped_name) == 0:
                    response = jsonify({'error':
                    'Your first value  must NOT !! be a space'})
                    response.status_code = 403
                    return response
                else:
                    if BucketList.query.filter_by(created_by=user_id).filter_by(name=name).first() is not None:
                        response = jsonify({
                            'message':"the bucket list already exists"
                        })
                        response.status_code = 403
                        return response
                    else:
                        bucketlist = BucketList(name=name, created_by=user_id)
                        bucketlist.save()
                        response = jsonify({
                            'message': "bucketlist successfully added"
                        })
                        response.status_code = 201
                        return response
        else:
            url = "/api/bucketlists/"
            search_query = request.args.get('q')
            if not search_query:
                content = []
                allbucketlists = BucketList.get_all(user_id)
                for bucketlist in allbucketlists:
                    bucket = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        "created_by": bucketlist.created_by
                    }
                    content.append(bucket)
                if  len(content) == 0:
                    response = jsonify({
                        "error":"No bucketlists"
                    })
                    response.status_code = 403
                    return response
                else:
                    if request.args.get("page"):
                        # Get the page requested
                        page = int(request.args.get("page"))
                    else:
                        # If no page number request, start at the first one
                        page = 1
                    limit = request.args.get("limit")
                    if limit and int(limit) < 10:
                        # Use the limit value from user if it exists
                        limit = int(request.args.get("limit"))
                    else:
                        # Set the default limit value if none was received
                        limit = 10
                    result = BucketList.query.filter_by(
                        created_by=user_id).paginate(page, limit, False)
                    if not result:
                        response = jsonify({
                            'error':'Ooops! You have not created any bucketlist yet!'})
                        response.status_code = 404
                        return response
                    if result.has_next:
                        next_page = request.url + '?page=' + str(
                            page + 1) + '&limit=' + str(limit)
                    else:
                        next_page = ""

                    if result.has_prev:
                        previous_page = request.url + '?page=' + str(
                            page - 1) + '&limit=' + str(limit)
                    else:
                        previous_page = ""
                    paginated_bucketlists = result.items
                    # Return the bucket lists
                    results = []
                    for bucketlist in paginated_bucketlists:
                        # Get the items in the paginated bucketlists
                        bucketlist = {
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "date_created": bucketlist.date_created,
                            "date_modified": bucketlist.date_modified,
                            "created_by": bucketlist.created_by
                        }
                        results.append(bucketlist)
                    response = jsonify({
                        "next_page": next_page,
                        "previous_page": previous_page,
                        "bucketlists": results
                        })

                    response.status_code = 200
                    return response
            elif search_query:
                # If it was a search request
                search = BucketList.query.filter_by(created_by=user_id).filter(
                    BucketList.name.ilike('%' + search_query + '%')).all()
                # If the search has returned any results
                if search:
                    search_results = []
                    for bucketlist in search:
                        bucketlist_searched = {
                            "id": bucketlist.id,
                            "name": bucketlist.name,
                            "date_created": bucketlist.date_created,
                            "date_modified": bucketlist.date_modified,
                            "created_by": bucketlist.created_by
                        }
                        search_results.append(bucketlist_searched)
                        response = jsonify(search_results)
                        response.status_code = 200
                        return response
                # If there are no results after the search
                else:
                    response = jsonify({
                        "message": "Bucketlist not found"
                    })
                    response.status_code = 404
                    return response


            else:
                content = []
                allbucketlists = BucketList.get_all(user_id)
                for bucketlist in allbucketlists:
                    bucket = {
                        'id': bucketlist.id,
                        'name': bucketlist.name,
                        'date_created': bucketlist.date_created,
                        'date_modified': bucketlist.date_modified,
                        "created_by": bucketlist.created_by
                    }
                    content.append(bucket)
                if  len(content) == 0:
                    response = jsonify({
                        "error":"No bucketlists"
                    })
                    response.status_code = 403
                    return response
                else:
                    # Return the bucket lists
                    response = jsonify(content)
                    response.status_code = 200
                    return response


    @app.route('/api/bucketlists/<int:bid>/', methods=['GET', 'PUT', 'DELETE'])
    @auth_token
    def bucketlist_manipulation(bid, user_id):
        """function that tests endpoints to get delete and update a bucket list"""
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
            return {"message": "bucketlist {} deleted successfully".format(bucketlist.id)}, 200
        elif request.method == 'PUT':
            name = request.data.get('name')
            bucket = BucketList.query.filter_by(id=bid, created_by=user_id).first()
            if bucket.name != name:
                if BucketList.exists(name, user_id):
                    return make_response(jsonify(dict(message="Bucket exists"), 409))

            bucketlist.name = name
            bucketlist.save()
            response = jsonify({"message":"Successfully updated"})
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
    def create_items(id, user_id, *args, **kwargs):
        '''
        This endpoint creates a new items in a bucket list.
        '''
        if request.method == "POST":
            name = str(request.data.get("name"))
            if not BucketList.exists(name, user_id):
                    return make_response(jsonify(dict(message="item herre"), 409))
            if name == "":
                response = jsonify({
                    'message': 'oops! you need to fill the name field'
                })
                response.status_code = 403
                return response
            elif name:
                stripped_name = name.split()
                name = str(stripped_name)
                if len(name) == 0:
                    response = jsonify({'error':'Your first value  must NOT !! be a space'})
                    response.status_code = 403
                    return response
                if  Item.query.filter_by(bucketlist_id=id).filter_by(name=name).first() is not None:
                    response = jsonify({'name':'The item already exist'})
                    response.status_code = 403
                    return response
                else:
                    item = Item(name=str(name), bucketlist_id=id)
                    item.save()
                    response = jsonify({
                        "message":"item successfully addded to this bucketlist"})
                    response.status_code = 201
                    return response



        elif request.method == "GET":
            items = Item.get_all_items(id)
            results = []
            for item in items:
                obj = {
                    "id": item.id,
                    "name": item.get_name(),
                    "date_created": item.date_created,
                    "date_modified": item.date_modified,
                    "bucketlist_id": item.bucketlist_id,
                }
                results.append(obj)
            if  len(results) == 0:
                response = jsonify({
                    "error":"No items in this bucket"
                })
                response.status_code = 403
                return response
            else:
                response = jsonify(results)
                response.status_code = 200
                return response


    @app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["PUT"])
    @auth_token
    def update_item(bid, item_id, user_id, *args, **kwargs):
        '''
        This endpoint update items in a bucket list.
        '''
        item = Item.query.filter_by(bucketlist_id=bid).filter_by(
            id=item_id).first()

        if not item:
            abort(404)

        if request.method == "PUT":
            name = str(request.data.get('name'))
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
    def delete_item(bid, item_id, user_id, *args, **kwargs):
        '''
        This endpoint deletes items from a bucketlist.
        '''
        item = Item.query.filter_by(bucketlist_id=bid).filter_by(id=item_id).first()
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
    def get_item(bid, item_id, user_id, *args, **kwargs):
        '''
        This endpoint gets items of a bucket list.
        '''
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
