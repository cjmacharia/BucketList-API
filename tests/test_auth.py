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