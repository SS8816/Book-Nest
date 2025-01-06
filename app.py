from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination, get_page_args

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/aka'
db = SQLAlchemy(app)

# Define a route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Save the user to the database
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # Redirect to profile setup page after registration
        return redirect('/login')
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_email'] = user.email
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Logged out successfully.', 'success')
    return redirect('/')

# User profile setup route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('You need to login first!', 'error')
        return redirect('/login')

    user = User.query.filter_by(id=session['user_id']).first()

    if request.method == 'POST':
        # Handle form submission for profile setup
        genres = request.form.getlist('genres')  # List of genre IDs from form
        authors = request.form.getlist('authors')  # List of author IDs from form
        books_read = request.form.getlist('reading_history')  # List of book IDs from form
        future_books = request.form.getlist('future_interests')  # List of book IDs from form

        # Clear existing preferences in the many-to-many tables
        user.favorite_genres = []
        user.favorite_authors = []
        user.reading_history = []
        user.future_interests = []

        # Add selected genres, authors, books to the user
        for genre_id in genres:
            genre = Genre.query.get(genre_id)
            if genre:
                user.favorite_genres.append(genre)
        
        for author_id in authors:
            author = Author.query.get(author_id)
            if author:
                user.favorite_authors.append(author)
        
        for book_id in books_read:
            book = Book.query.get(book_id)
            if book:
                user.reading_history.append(book)

        for book_id in future_books:
            book = Book.query.get(book_id)
            if book:
                user.future_interests.append(book)

        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect('/')

    # Get all available genres, authors, and books for the user to select
    genres = Genre.query.all()
    authors = Author.query.all()
    books = Book.query.all()

    return render_template('profile.html', genres=genres, authors=authors, books=books)

# Recommendation route
@app.route('/recommendations')
def recommendations():
    if 'user_id' not in session:
        flash('Please log in to view recommendations.', 'error')
        return redirect('/login')

    user = User.query.filter_by(id=session['user_id']).first()

    # Get user preferences
    favorite_genres = [genre.id for genre in user.favorite_genres]
    favorite_authors = [author.id for author in user.favorite_authors]
    books_read = [book.id for book in user.reading_history]

    # Query books matching preferences but exclude already-read ones
    recommended_books = Book.query.filter(
        (Book.genre_id.in_(favorite_genres)) |
        (Book.author_id.in_(favorite_authors))
    ).filter(~Book.id.in_(books_read)).order_by(
        db.case(
            (Book.genre_id.in_(favorite_genres), 1),
            (Book.author_id.in_(favorite_authors), 2),
            else_=3
        )
    ).all()

    # Implement pagination
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page', per_page=5)
    total = len(recommended_books)
    paginated_books = recommended_books[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template(
        'recommendations.html',
        books=paginated_books,
        pagination=pagination
    )

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    favorite_genres = db.relationship('Genre', secondary='user_genres')
    favorite_authors = db.relationship('Author', secondary='user_authors')
    reading_history = db.relationship('Book', secondary='user_books')
    future_interests = db.relationship('Book', secondary='user_future_interests')

# Genre model
class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Author model
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    author = db.relationship('Author', backref=db.backref('books', lazy=True))
    genre = db.relationship('Genre', backref=db.backref('books', lazy=True))

# Many-to-many relationship tables
class UserGenres(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)

class UserAuthors(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), primary_key=True)

class UserBooks(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)

class UserFutureInterests(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True)

def add_default_data():
    # Create tables if they don't exist
    db.create_all()

    # Add genres if they do not exist
    if not Genre.query.first():
        genres = [
            'Fiction', 'Non-fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 
            'Thriller', 'Horror', 'Biography', 'Self-Help', 'Adventure', 'Historical Fiction', 
            'Young Adult', 'Children\'s', 'Dystopian', 'Psychological', 'Philosophy', 
            'Health & Wellness', 'Poetry', 'True Crime', 'Graphic Novels', 'Religion', 'Science', 
            'Art', 'Cookbooks', 'Travel', 'Business', 'Technology', 'Humor', 'Sports'
        ]
        for genre_name in genres:
            genre = Genre(name=genre_name)
            db.session.add(genre)

    # Commit genres to the database
    db.session.commit()

    # Add authors if they do not exist
    if not Author.query.first():
        authors = [
            'J.K. Rowling', 'George Orwell', 'J.R.R. Tolkien', 'Agatha Christie', 'Mark Twain', 
            'Ernest Hemingway', 'F. Scott Fitzgerald', 'Jane Austen', 'Leo Tolstoy', 'Charles Dickens',
            'Harper Lee', 'Stephen King', 'J.D. Salinger', 'George R.R. Martin', 'Isaac Asimov',
            'Ray Bradbury', 'Arthur C. Clarke', 'Margaret Atwood', 'Neil Gaiman', 'Orson Scott Card',
            'Dan Brown', 'Haruki Murakami', 'Gabriel García Márquez', 'Chimamanda Ngozi Adichie', 
            'Paulo Coelho', 'Terry Pratchett', 'Virginia Woolf', 'John Steinbeck', 'Maya Angelou', 
            'William Shakespeare', 'Agatha Christie', 'Douglas Adams', 'C.S. Lewis', 'Frank Herbert'
        ]
        for author_name in authors:
            author = Author(name=author_name)
            db.session.add(author)

    # Commit authors to the database
    db.session.commit()

    # Add books if they do not exist
    if not Book.query.first():
        books = [
            ('Harry Potter and the Sorcerer\'s Stone', 1, 1), ('1984', 2, 2), 
            ('The Hobbit', 3, 1), ('Murder on the Orient Express', 4, 5), 
            ('The Great Gatsby', 5, 1), ('The Catcher in the Rye', 6, 1), 
            ('Pride and Prejudice', 7, 1), ('War and Peace', 8, 1), 
            ('A Tale of Two Cities', 9, 1), ('To Kill a Mockingbird', 10, 1),
            ('The Shining', 11, 5), ('The Girl on the Train', 12, 5),
            ('Game of Thrones', 13, 1), ('Foundation', 14, 3),
            ('Fahrenheit 451', 15, 3), ('Brave New World', 16, 3)
        ]
        for book_title, author_id, genre_id in books:
            book = Book(title=book_title, author_id=author_id, genre_id=genre_id)
            db.session.add(book)

    # Commit books to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        add_default_data()  # Add default genres, authors, and books if not present
    app.run(debug=True)
