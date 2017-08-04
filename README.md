[![Code Health](https://landscape.io/github/cjmash/BucketList-API/restful-api/landscape.svg?style=flat-square)](https://landscape.io/github/cjmash/BucketList-API/restful-api)    [![Codacy Badge](https://api.codacy.com/project/badge/Grade/5998ad5777634cb591392198de69ad3c)](https://www.codacy.com/app/cjmash/BucketList-API?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=cjmash/BucketList-API&amp;utm_campaign=Badge_Grade)  [![Build Status](https://travis-ci.org/cjmash/BucketList-API.svg?branch=restful-api)](https://travis-ci.org/cjmash/BucketList-API)

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
/api/bucketlists/<bucket_id>/            |  	GET	    | Retrieve a bucketlist by ID | private
/api/bucketlists/<bucket_id>/	          |      PUT	|     Update a bucketlist |private
/api/bucketlists/<bucket_id>/	          |      DELETE	| Delete a bucketlist |private
/api/bucketlists/<bucket_id>/items/      |     POST	| Create items in a bucketlist |private
/api/bucketlists/<bucket_id>/items/<item_id>/|	DELETE	| Delete an item in a bucketlist |prvate
/api/bucketlists/<bucket_id>/items/<item_id>|/	PUT   	|update a bucketlist item details |private

Run the APIs on postman to ensure they are fully functioning.
