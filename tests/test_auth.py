import unittest
import json

from app.app import create_app, db


class AuthTestCases(unittest.TestCase):
    """
    Tests for  authentication 
    """
    def setUp(self):
        self.app = create_app(config_name="testing")
        # Set up the test client
        self.client = self.app.test_client
        self.user_data = json.dumps(dict({
            "username": "testuser",
            "email": "testuser@gmail.com",
            "password": "test_password"
        }))

        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """
        Test new user registration
        """
        result = self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                                    content_type="application/json")
        results = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 201)

    def test_double_registration(self):
        """
        Test that double registration
        """
        result = self.client().post("/api/bucketlists/auth/register/", data=self.user_data,
                                    content_type="application/json")
        self.assertEqual(result.status_code, 201)

        # Test double registration
        second_result = self.client().post("/api/bucketlists/auth/register/",
                                           data=self.user_data,
                                           content_type="application/json")
        self.assertEqual(second_result.status_code, 409)      

    def test_register_with_a_nonexistent_url(self):
        response = self.client().post('/bucketlist/api/auth/regist/', data=self.user_data)
        self.assertEqual(response.status_code, 404)    

    def test_registration_no_username(self):
        """
        Test missing username
        """
        res = json.dumps(dict({
            "username": "",
            "password": "test_password",
            "email": "testuser@gmail.com"
        }))

        result = self.client().post("/api/bucketlists/auth/register/", data=res,
                                    content_type="application/json")
        final_result = json.loads(result.data.decode())
        self.assertEqual(result.status_code, 400)     

    def test_registration_no_password(self):
        """
        Test that missing password throws an error
        """
        res = json.dumps(dict({
            "username": "testuser",
            "password": "",
            "email": "testuser@gmail.com"
        }))

        result = self.client().post("/api/bucketlists/auth/register/", data=res,
                                    content_type="application/json")
        result = json.loads(result.data)
        self.assertEqual(result.status_code, 400)  

    def test_login_non_registered_user(self):
        """
        Test that non registered users cannot log in
        """
        unregistered = json.dumps(dict({
            "username": "tiaroot",
            "email": "tiaroot@email.com",
            "password": "invalidpassword"
        }))

        result = self.client().post("/api/bucketlists/auth/login/", data=unregistered,
                                    content_type="application/json")
        final_result = json.loads(result.data.decode())

        self.assertEqual(result.status_code, 401)
           