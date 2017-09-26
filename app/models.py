from datetime import datetime, timedelta
import jwt
from .app import db
from flask_bcrypt import Bcrypt
SECRET_KEY = 'this is a very long string'

class User(db.Model):
    """
    The model for a User
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), nullable=False, unique=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship('BucketList', order_by="BucketList.id",
                                  cascade="all,delete-orphan") #relationship

    def __init__(self, username, password, email):
        """
        Initialize the User with a username, email and password
        """
        self.username = username
        self.password = Bcrypt().generate_password_hash(password).decode()

        self.email = email

    def password_is_valid(self, password):
        """
        Checks the password against it's hash to validates the user's password
        """
        return Bcrypt().check_password_hash(self.password, password)

    def token_generate(self, user_id):
        """function to generate a token """
        try:
            """we set up a payload with the expiry time issued date and the subject """
            payload = {
                'iat':datetime.utcnow(),
                'exp':datetime.utcnow()+timedelta(hours=1245),
                'sub':user_id
                }
            return jwt.encode(
                payload,
                SECRET_KEY,
                algorithm='HS256')

        except Exception as e:
            return 'error ocurred'

    @staticmethod
    def decode_token(token):
        """
        Decodes access token from Authorization Header
        """
        try:
            # decode the token if provided and returns the user id
            payload = jwt.decode(token, SECRET_KEY)
            return payload["sub"]

        except jwt.ExpiredSignatureError:
            # checks whether the token has expired
            return "please re login in your token has expired"

        except jwt.InvalidTokenError:
            # checks if the token is valid
            return "the token is invalid"

    def save(self):
        """
        Save a user to the database
        """
        db.session.add(self)
        db.session.commit()

class BucketList(db.Model):
    """
    The model for the bucketlist
    """

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    bucketlists = db.relationship('Item', order_by="Item.id",
                                  cascade="all,delete-orphan")
    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by


    def save(self):
        """
        save a bucketlist
        """
        db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_all(user_id):
        """
        get all buckets
        """
        return BucketList.query.filter_by(created_by=user_id)

    def delete(self):
        """
        Delete a bucketlist
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_items(bucketlist_id):
        """
        Returns all the items in a bucketlist
        """
        return Item.query.filter_by(bucketlist_id=bucketlist_id)

    @staticmethod
    def exists(bucket_name, created_by):
        """
        Returns if a bucket exists with that name
        """
        bucket = BucketList.query.filter_by(name=bucket_name, created_by=created_by).first()
        return True if bucket else False


class Item(db.Model):
    """Model for my items"""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


    def __init__(self, name, bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        """
        save an item
        """
        db.session.add(self)
        db.session.commit()

    def get_name(self):
        return self.name.strip('[]')

    @staticmethod
    def get_all_items(bucketlist_id):
        """
        get all items
        """
        return Item.query.filter_by(bucketlist_id=bucketlist_id).all()

    def delete(self):
        """
        Delete an item
        """
        db.session.delete(self)
        db.session.commit()
