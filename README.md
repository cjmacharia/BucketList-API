[![Code Health](https://landscape.io/github/cjmash/BucketList-API/restful-api/landscape.svg?style=flat-square)](https://landscape.io/github/cjmash/BucketList-API/restful-api)

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


# Run Database Migrations

 Initialize, migrate, upgrade the database

python manage.py db init

python manage.py db migrate

python manage.py db upgrade

Launch the Progam

# Run

python run.py development
Interact with the API, send http requests using Postman

# API Endpoints

URL Endpoint	|               HTTP requests   | access| status|
----------------|-----------------|-------------|------------------
/api/bucketlists/auth/register/   |      POST	| Register a new user|publc
/api/bucketlists/auth/login/	  |     POST	| Login and retrieve token|public
/api/bucketlists/	              |      POST	|Create a new Bucketlist|private
/api/bucketlists/	              |      GET	|     Retrieve all bucketlists for user|private
/api/bucketlists/<id>/            |  	GET	    | Retrieve a bucketlist by ID | private
/api/bucketlists/<id>/	          |      PUT	|     Update a bucketlist |private
/api/bucketlists/<id>/	          |      DELETE	| Delete a bucketlist |private
/api/bucketlists/<id>/items/      |     POST	| Create items in a bucketlist |private
/api/bucketlists/<id>/items/<item_id>|	DELETE	| Delete an item in a bucketlist |prvate
/api/bucketlists/<id>/items/<item_id>|	PUT   	|update a bucketlist item details |private

Run the APIs on postman to ensure they are fully functioning.
