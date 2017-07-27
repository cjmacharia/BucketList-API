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

    def test_create_item_with_invalid_bucket(self):    
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/30/items/', data=self.item)
        self.assertEqual(res.status_code, 404)   

    def test_get_bucket_item_by_id(self):
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        the_item = self.client().get('/api/bucketlists/1/items/1/')
        self.assertEqual(the_item.status_code, 200)
        self.assertIn('hawai  skies yeeey', the_item.data.decode('utf-8'))  

    def test_get_bucket_item_with_invalid_id(self):
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        the_item = self.client().get('/api/bucketlists/1/items/20/')
        self.assertEqual(the_item.status_code, 404)   

    def test_edit_item(self):
        result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/1/items/', data={
            'name':'go to the bermuda'})
        self.assertEqual(res.status_code, 201)
        res = self.client().put('/api/bucketlists/1/items/1/', data={
            'name':'go to the bermuda with my family'
        })
        self.assertEqual(res.status_code, 200)    

    def test_item_exist(self):
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertIn('The item already exist', res.data.decode('utf-8'))   

    def test_edit_item_that_doesnot_exist(self):
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201)  
        res = self.client().put('/api/bucketlists/1/items/19/', data={
            'name':'go to the bermuda with my family'
        })
        self.assertEqual(res.status_code, 404)  

    def test_delete_items(self):
        # result = self.client().post("/api/bucketlists/", data=self.bucketlist)
        # self.assertEqual(result.status_code, 201) 
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/bucketlists/1/items/1/', data=self.item)
        self.assertEqual(res.status_code, 200)

    def test_delete_invalid_item_id(self):
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201) 
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/bucketlists/1/items/18/', data=self.item)
        self.assertEqual(res.status_code, 404)  

    def test_delete_items_with_invalid_bucket_id(self):
        result = self.client().post('/api/bucketlists/', data=self.bucketlist)
        self.assertEqual(result.status_code, 201) 
        res = self.client().post('/api/bucketlists/1/items/', data=self.item)
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/bucketlists/19/items/1/', data=self.item)
        self.assertEqual(res.status_code, 404)       
            

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()            