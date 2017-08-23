import os
from flasgger import Swagger
from app.app import create_app
from app.decorator import auth_token
#pylint: disable=C0103
config_name = os.getenv('APP_SETTINGS')
app = create_app(config_name)
swagger = Swagger(app)

@app.route('/api/bucketlists/auth/register/', methods=["POST"])
def register_user_api():
    """ endpoint returning register details.
    ---
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    """
@app.route('/api/bucketlists/auth/login/', methods=["POST"])
def login_user_api():
    """ endpoint returning login details.
    ---
    parameters:
      - name: email
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    """

@app.route("/api/bucketlists/", methods=["GET"])
@auth_token
def create_bucketlists_get():
    """endpoint returning get  details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true

    """
@app.route("/api/bucketlists/", methods=["POST"])
@auth_token
def create_bucketlists_post():
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true

    """
@app.route('/api/bucketlists/<int:bid>/', methods=['PUT'])
@auth_token
def bucketlist_manipulation_put():
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

@app.route('/api/bucketlists/<int:bid>/', methods=['GET'])
@auth_token
def bucketlist_manipulation_get():
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route('/api/bucketlists/<int:bid>/', methods=['DELETE'])
@auth_token
def bucketlist_manipulation_detete():
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

@app.route("/api/bucketlists/<int:id>/items/", methods=["GET"])
@auth_token
def create_items_get():
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: string
        required: true
    """
@app.route("/api/bucketlists/<int:id>/items/", methods=["POST"])
@auth_token
def create_items_post():
    """endpoint returning  bucketlist item details.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: id
        in: path
        type: string
        required: true
    """
@app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["PUT"])
@auth_token
def update_item_put():
    """endpoint returning  bucketlist item details.
    ---
    parameters:
      - name: name
        in: formData
        type: string
        required: true
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["DELETE"])
@auth_token
def update_item_delete():
    """endpoint returning  bucketlist item details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """
@app.route("/api/bucketlists/<int:bid>/items/<int:item_id>/", methods=["GET"])
@auth_token
def update_item_get():
    """endpoint returning  bucketlist item details.
    ---
    parameters:
      - name: Authorization
        in: header
        type: string
        required: true
      - name: item_id
        in: path
        type: string
        required: true
      - name: bid
        in: path
        type: string
        required: true
    """

app.run()
