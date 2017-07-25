import unittest
from app.app import create_app, db


class BucketlistTestCases(unittest.TestCase):
    """
    Test cases for the bucketlist
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        #set up test client
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go for skydiving '} 

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()    



    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        