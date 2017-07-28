# BucketList Application API


# Installation and Setup

Clone the repo

git clone https://github.com/cjmash/BucketList-API.git

use ssh 

    git@github.com:cjmash/BucketList-API.git

go to the root folder

cd bucketlist
Create the virtual environment

mkvirtualenv myenv
Activate the virtual environment

workon myenv
# Install the requirements

pip install -r requirements.txt
Set Up Environment


Run Database Migrations

# Initialize, migrate, upgrade the database

python manage.py db init
python manage.py db migrate
python manage.py db upgrade
Launch the Progam

# Run

python run.py development
Interact with the API, send http requests using Postman

# API Endpoints

URL Endpoint	                     HTTP Methods	Summary
/api/bucketlists/auth/register/         POST	    Register a new user
/api/bucketlists/auth/login/	            POST	Login and retrieve token
/api/bucketlists/	                    POST	Create a new Bucketlist
/api/bucketlists/	                    GET	     Retrieve all bucketlists for user
/api/bucketlists/<id>/              	GET	     Retrieve a bucketlist by ID
/api/bucketlists/<id>/	                PUT	     Update a bucketlist
/api/bucketlists/<id>/	                DELETE	 Delete a bucketlist
/api/bucketlists/<id>/items/            POST	 Create items in a bucketlist
/api/bucketlists/<id>/items/<item_id>	DELETE	 Delete an item in a bucketlist
/api/bucketlists/<id>/items/<item_id>	PUT   	update a bucketlist item details

Run the APIs on postman to ensure they are fully functioning.
