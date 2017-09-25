import unittest
import json
from app.app import create_app, db



class BucketitemsTestCases(unittest.TestCase):
    """
    Test cases for the items in a bucket list
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        #set up test client
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go for skydiving'}
        self.item = {'name': 'hawai  skies yeah'}
        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

        # Register a that we will use to test
        self.user_data = json.dumps(dict({
            "username": "testuser",
            "email": "cj@test.com",
            "password": "testpassword"}))
        self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                           content_type="application/json")

        self.login_info = json.dumps(dict({
            "email": "cj@test.com",
            "password": "testpassword"
        }))
        # Log is as the test user and get a token
        self.login_result = self.client().post("/api/bucketlists/auth/login/",
                                               data=self.login_info,
                                               content_type="application/json")
        self.access_token = json.loads(
            self.login_result.data.decode())['access_token']
        self.headers = dict(Authorization="Bearer "+ self.access_token,
                            content_type="application/json")

    def test_create_item(self):
        """
        Test the creation of an item through the API via POST
        """
        result = self.client().post("/api/bucketlists/", headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/', headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 201)

    def test_create_item_nonexistence_bucketlist(self):
        """
        Test the creation of an item through the API via POST with an invalid bucketlist
        """
        result = self.client().post("/api/bucketlists/", headers=self.headers,
                                    data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/30/items/', headers=self.headers,
                                 data=self.item)
        self.assertEqual(res.status_code, 401)

    # def test_get_bucket_item_by_id(self):
    #     """
    #     Test get item by id
    #     """
    #     result = self.client().post("/api/bucketlists/", headers=self.headers, data=self.bucketlist)
    #     self.assertEqual(result.status_code, 201)
    #     res = self.client().post('/api/bucketlists/1/items/', headers=self.headers, data=self.item)
    #     self.assertEqual(res.status_code, 201)
    #     the_item = self.client().get('/api/bucketlists/1/items/1/', headers=self.headers, )
    #     self.assertEqual(the_item.status_code, 200)

    def test_get_bucket_item_invalid_id(self):
        """
        Test getting  an item through the API with an invalid id
        """
        result = self.client().post("/api/bucketlists/", headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/', headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 201)
        the_item = self.client().get('/api/bucketlists/1/items/20/', headers=self.headers, )
        self.assertEqual(the_item.status_code, 401)

    def test_edit_item(self):
        """
        Test editting   an item through the API
        """
        result = self.client().post("/api/bucketlists/", headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/', headers=self.headers, data={
            'name':'go to the bermuda'})
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/api/bucketlists/1/items/1/', headers=self.headers, data={
            'name':'go to the bermuda with my family'
        })
        self.assertEqual(res.status_code, 200)

    def test_edit_nonexistent_item(self):
        """
        Test edit  an item through the API with an invalid id
        """
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().put('/api/bucketlists/1/items/19/', headers=self.headers, data={
            'name':'go to the bermuda with my family'
        })
        self.assertEqual(res.status_code, 401)

    def test_delete_invalid_item_id(self):
        """
        Test delete  an item through the API with an invalid id
        """
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/',
                                 headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/bucketlists/1/items/18/',
                                   headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 401)

    def test_delete_items_nonexistent_bucketid(self):
        """
        Test delete  an item through the API with an invalid bucketlist
        """
        result = self.client().post('/api/bucketlists/', headers=self.headers, data=self.bucketlist)
        self.assertEqual(result.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/', headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/bucketlists/19/items/1/',
                                   headers=self.headers, data=self.item)
        self.assertEqual(res.status_code, 401)
    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

