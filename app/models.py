from app import db

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

    def __init__(self, name):
        self.name = name
    
    def save(self):
        """
        save a bucketlist
        """
        db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_all():
        """
        get all buckets
        """
        return BucketList.query.all()

    def delete(self):
        """
        Delete a bucketlist
        """
        db.session.delete(self)
        db.session.commit()

class Item(db.Model):
    """Model for my items"""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(BucketList.id))  
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())                  
    def __init__(self, name,bucketlist_id):
        self.name = name
        self.bucketlist_id = bucketlist_id
    
    def save(self):
        """
        save an item
        """
        db.session.add(self)
        db.session.commit()
    @staticmethod
    def get_all_items(self):
        """
        get all items
        """
        return Item.query.filter_by(bucketlist_id=BucketList_id)

    def delete(self):
        """
        Delete an item
        """
        db.session.delete(self)
        db.session.commit()                        
        
