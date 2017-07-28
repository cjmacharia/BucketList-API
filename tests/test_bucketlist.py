import unittest
from app.app import create_app, db
from flask import json



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

        # Register a that we will use to test
        self.user_data = json.dumps(dict({
            "username": "tuser",
            "email": "cjuser@test.com",
            "password": "test"
                }))
        self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                           content_type="application/json")

        self.login_info = json.dumps(dict({
            "email": "cjuser@test.com",
            "password": "test"
        }))
        # Log is as the test user and get a token
        self.login_result = self.client().post("/api/bucketlists/auth/login/",
                                               data=self.login_info,
                                               content_type="application/json")
        self.access_token = json.loads(
            self.login_result.data.decode())['access_token']   
        print (self.access_token)      
        self.headers =dict(Authorization="Bearer "+ self.access_token, content_type = "application/json")                                  

    def test_bucketlist_creation(self):
        """
        Test the creation of a bucketlist through the API via POST
        """
        result = self.client().post("/api/bucketlists/", headers=self.headers,
        data=self.bucketlist)
        self.assertEqual(result.status_code, 201) 
         

    def test_get_all_bucketlists(self):
        """Test API to get  bucketlists (GET request)."""
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/', headers=self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertIn('Go for skydiving', result.data.decode('utf-8')) 

    def test_get_bucketlist_by_id(self):
        """Test API to get  bucketlist with its id (GET request)."""
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/1/',headers=self.headers)
        self.assertEqual(result.status_code, 200)
            
    def test_get_bucketlist_with_invalid_id(self):
        """Test API to get a non existing bucketlist """
        result = self.client().post('/api/bucketlists/', data=self.bucketlist, headers=self.headers)
        self.assertEqual(result.status_code, 201)
        result = self.client().get('/api/bucketlists/29/', headers=self.headers)
        self.assertEqual(result.status_code, 404)
    
    def test_edit_bucketlist(self):
        """Test API to edit an existing bucketlist (PUT request)"""
        result = self.client().post('/api/bucketlists/',  headers=self.headers, data={
            'name' :'play the guitar'
        })   
        self.assertEqual(result.status_code, 201)

        result = self.client().put('/api/bucketlists/1/', headers=self.headers, data={
            'name' :'play the guitar and the piano', 
        })
        self.assertEqual(result.status_code, 200)
        endresult = self.client().get('/api/bucketlists/1/', headers=self.headers)
        self.assertIn('play the guitar and the piano', endresult.data.decode('utf-8'))
    
    def test_edit_bucketlist_with_invalid_id(self):
        """Test API to edit a non existing bucketlist """
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().put('/api/bucketlists/29/', headers=self.headers)
        self.assertEqual(result.status_code, 404)

    def test_delete_bucketlist(self):
        """Test API to delete an existing bucketlist (DELETE request)"""
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().delete('/api/bucketlists/1/', headers=self.headers)
        self.assertEqual(res.status_code, 200)
        #test if the bucket has been deleted
        result = self.client().get('/api/bucketlists/1/', headers=self.headers)
        self.assertEqual(result.status_code, 404) 

    def test_delete_bucketlist_with_invalid_id(self):
        """Test API to delete a non existing bucketlist """
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        result = self.client().delete('/api/bucketlists/29/', headers=self.headers)
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


