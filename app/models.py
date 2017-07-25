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
