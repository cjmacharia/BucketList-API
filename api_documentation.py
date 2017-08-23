import os
from flasgger import Swagger
from app.app import create_app
from app.decorator import auth_token

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
def create_bucketlists_getapi(user_id, *args, **kwargs):
    """endpoint returning get  details.
    ---
    parameters:
      - name: name
        in: raw 
        type: string
        required: true 
    
    """ 
@app.route("/api/bucketlists/", methods=["POST"])
@auth_token
def create_bucketlists_postapi(user_id, *args, **kwargs):
    """endpoint returning post bucketlist details.
    ---
    parameters:
      - name: name
        in: raw 
        type: string
        required: true 
    
    """     

app.run()