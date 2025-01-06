import unittest
from app import app, db, User  # Assuming 'app' is your Flask app and 'User' is your model

class AppIntegrationTestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up the test client and create a temporary database."""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Using in-memory database for testing
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        # Ensure app context is available for db operations
        with self.app.app_context():
            db.create_all()  # Create all tables for the in-memory database

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()  # Remove the session
            db.drop_all()  # Drop all tables after each test

    def test_user_registration_login_and_profile_creation(self):
        """Test user registration, login, and profile creation."""

    # Step 1: Register a new user
        response = self.client.post('/register', data=dict(
            email='test@test.com',
            password='password'
        ), follow_redirects=True)

    # Assert registration was successful and redirected to login
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Check if login page is shown after redirect

    # Step 2: Login the user
        response = self.client.post('/login', data=dict(
            email='test@test.com',
            password='password'
        ), follow_redirects=True)

    # Assert login was successful and redirected to homepage
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Book Nest!', response.data)  # Check if homepage is shown

    # Step 3: Ensure profile setup is available after login
        response = self.client.get('/profile', follow_redirects=True)

    # Assert that profile setup page loads correctly
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Complete Your Profile', response.data)  # Check if profile setup form is available

    # Optionally, test profile form submission (skipping form validation for now)
        response = self.client.post('/profile', data=dict(
            genres=['1', '2'],  # Example genre IDs
            authors=['1', '2'],  # Example author IDs
            reading_history=['1', '2'],  # Example book IDs
            future_interests=['1', '2']  # Example future books IDs
        ), follow_redirects=True)

    # Assert profile was updated successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Book Nest!', response.data)  # Ensure profile update confirmation

    # Step 4: Check if the user was added to the database and profile updated
        with self.app.app_context():
            user_in_db = User.query.filter_by(email='test@test.com').first()
            self.assertIsNotNone(user_in_db)  # Ensure user exists in the database
            self.assertEqual(user_in_db.email, 'test@test.com')  # Ensure email matches


