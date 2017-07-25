import unittest
from app.app import create_app, db


class BucketitemsTestCases(unittest.TestCase):
    """
    Test cases for the items
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        #set up test client
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go for skydiving '} 
        self.item = {'name': 'hawai  skies yeeey'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()    


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()            