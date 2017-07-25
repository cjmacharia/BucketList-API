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

    def test_create_bucket_without_name(self):
        """
        Test the creation of an empty bucketlist 
        """
        res = self.client().post("/api/bucketlists/", data={
            'name':''
        })        
        self.assertEqual(res.status_code, 403)
        self.assertIn('you need to fill the name field', res.data.decode('utf-8'))

    def test_bucketlist_creation(self):
        """
        Test the creation of a bucketlist through the API via POST
        """
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)     
        self.assertIn('Go for skydiving', result.data.decode('utf-8'))

    def test_get_all_bucketlists(self):
        """Test API to get  bucketlists (GET request)."""
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go for skydiving', result.data.decode('utf-8'))    

    def test_get_bucketlist_by_id(self):
        """Test API to get  bucketlist with its id (GET request)."""
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/1/')
        self.assertEqual(result.status_code, 200)

    def test_get_bucket_with_empty_database(self):
        """Test API to get from and empty database"""
        response = self.client().post('/api/bucketlists/')
        self.assertEqual(response.data, 404)   

    def test_get_bucketlist_with_invalid_id(self):
        """Test API to get a non existing bucketlist """
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/29/')
        self.assertEqual(result.status_code, 404)    

    def test_edit_bucketlist(self):
        """Test API to edit an existing bucketlist (PUT request)"""
        result = self.client().post('/api/bucketlists/', data={
            'name' :'play the guitar'
        })   
        self.assertEqual(result.status_code, 201)

        result = self.client().put('/api/bucketlists/1/', data={
            'name' :'play the guitar and the piano'
        })
        self.assertEqual(result.status_code, 200)
        endresult = self.client().get('/api/bucketlists/1/')
        self.assertIn('play the guitar and the piano', endresult.data.decode('utf-8'))

    def test_edit_buckettlist_with_invalid_id(self):
        """Test API to edit a non existing bucketlist """
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().put('/api/bucketlists/29/')
        self.assertEqual(result.status_code, 404)                 

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

        