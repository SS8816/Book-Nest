import unittest
from app import app, db
from app import User, Genre, Author, Book
from flask import Flask

class AppTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Runs once before all tests"""
        cls.app = app
        cls.client = cls.app.test_client()

    @classmethod
    def setUp(cls):
        """Runs before every individual test"""
        # Ensures that the app context is pushed before any db operations
        with cls.app.app_context():
            # Create tables before each test
            db.create_all()
            # Add default test data here if necessary
            cls.create_test_data()

    @classmethod
    def tearDown(cls):
        """Runs after every individual test"""
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()  # Drops all tables after each test

    @staticmethod
    def create_test_data():
        """Add test data for genres, authors, and books."""
        with app.app_context():
            genre = Genre(name="Fiction")
            author = Author(name="J.K. Rowling")
            book = Book(title="Harry Potter", author=author, genre=genre)
            db.session.add_all([genre, author, book])
            db.session.commit()

    def test_user_registration(self):
        """Test registration of a new user."""
        with self.client:
            response = self.client.post('/register', data=dict(email='test@test.com', password='password'))
            self.assertEqual(response.status_code, 302)  # Check for redirect to profile page

            with app.app_context():
                # Check if user is saved in the database
                user = User.query.filter_by(email='test@test.com').first()
                self.assertIsNotNone(user)

    def test_user_login(self):
        """Test login of a user."""
        with app.app_context():
        # Add a test user to the database
            user = User(email='test@test.com', password='password')
            db.session.add(user)
            db.session.commit()

        with self.client:
        # Log in user, disable follow_redirects to catch the redirect message
            response = self.client.post('/login', data=dict(email='test@test.com', password='password'), follow_redirects=False)
        
        # Check if the status code is 302, which means a redirect (successful login)
            self.assertEqual(response.status_code, 302)
        
        # Optionally, check the Location header to verify redirection to the homepage or dashboard
            self.assertIn('Location', response.headers)
            self.assertEqual(response.headers['Location'], '/')






    def test_profile_creation(self):
        """Test profile creation and preference selection."""
        with app.app_context():
            user = User(email='test@test.com', password='password')
            db.session.add(user)
            db.session.commit()

        with self.client:
            # Log in user
            self.client.post('/login', data=dict(email='test@test.com', password='password'))

            # Go to profile page and submit preferences
            response = self.client.post('/profile', data=dict(
                genres=[1],
                authors=[1],
                reading_history=[1],
                future_interests=[1]
            ))

            self.assertEqual(response.status_code, 302)  # Should redirect to homepage

    def test_add_default_data(self):
        """Test default data is added to the database if not present."""
        self.create_test_data()

        with app.app_context():
            genre = Genre.query.first()
            author = Author.query.first()
            book = Book.query.first()

            self.assertIsNotNone(genre)
            self.assertIsNotNone(author)
            self.assertIsNotNone(book)

if __name__ == '__main__':
    unittest.main()
