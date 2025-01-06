# Book Nest - Personalized Book Recommendation Website

Welcome to **Book Nest**! This project is designed to help users discover their next favorite read by curating personalized book recommendations based on their preferences and reading history. Whether you're a casual reader or a bookworm, Book Nest aims to make finding great books easy and enjoyable.

---

## Project Overview
Book Nest curates a list of books users might enjoy by gathering input on:
- **Favorite Authors**
- **Books They Have Read and Liked**
- **Preferred Genres**
- **Books They Wish to Read**

Using this information, Book Nest generates personalized suggestions, providing users with a fresh reading list tailored to their unique tastes.

---

## Key Features
- **Personalized Recommendations**: Get book suggestions that match your interests and reading habits.
- **User-Friendly Input Form**: Easily add favorite authors, genres, and books.
- **Dynamic Curation**: Recommendations adapt as users update their preferences.
- **Interactive Experience**: Engage with a visually appealing and intuitive interface.

---

## How It Works
1. **User Inputs** their reading preferences through a simple form.
2. The system analyzes the data and **compares it to a book database**.
3. A curated list of book recommendations is generated based on:
   - Matching genres
   - Similar books by favorite authors
   - Books with themes the user enjoys
4. Users can update preferences anytime to receive new recommendations.

---

## Tech Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: MySQL (via XAMPP & PHPMyAdmin)



## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/Book-Nest.git
   ```
2. Navigate to the project folder:
   ```bash
   cd Book-Nest
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask server:
   ```bash
   python app.py
   ```
5. Access the website at:
   ```
   http://localhost:5000


## File Structure

Book-Nest/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── index.html
│   ├── recommendations.html
│   └── form.html
├── app.py
├── requirements.txt
└── README.md

## Future Improvements
- **User Authentication** to save personalized recommendations
- **Integration with Book APIs** for real-time data
- **Review System** allowing users to rate books
- **Social Features** to share lists with friends


