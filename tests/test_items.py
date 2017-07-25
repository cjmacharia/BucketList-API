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

    def test_create_item(self):
        """
        Test the creation of an item through the API via POST
        """
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        self.assertIn('hawai  skies yeeey', res.data.decode('utf-8'))
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()            