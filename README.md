# Notes Management Web Application

A secure and user-friendly Notes Management Web Application built with Flask, Python, and MySQL, enabling users to create, manage, and organize notes with advanced authentication and email verification features.

## Features

User Authentication & Authorization

* Register and login with email verification

* Password reset via OTP/email using SendGrid API

* Role-based access control for different users

Notes Management

* Create, Read, Update, Delete (CRUD) operations for notes

* User-specific access to ensure privacy

* Responsive and clean UI using HTML, CSS, Bootstrap

Security & Performance

* Passwords hashed for security

* Token-based sessions with JWT for authentication

* Optimized database interactions using MySQL

## Tech Stack

* **Backend**: Python, Flask, Flask-JWT-Extended, Flask-SQLAlchemy

* **Frontend**: HTML5, CSS3, Bootstrap

* **Database**: MySQL

* **Email Service**: SendGrid API

* **Deployment**: Render

## Installation & Setup

Clone the repository:
```
git clone https://github.com/yourusername/notes-management.git
cd notes-management
```

Create a virtual environment:
```
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

Install dependencies:
```
pip install -r requirements.txt
```

Set environment variables:
```
export SECRET_KEY='your_secret_key'
export SENDGRID_API_KEY='your_sendgrid_api_key'
export DATABASE_URL='mysql://username:password@host/dbname'
```

Run the application:
```
flask run
```
## Usage

* Open your browser and navigate to http://127.0.0.1:5000

* Register a new account and verify your email

* Login and start creating, editing, or deleting notes

* Use the password reset feature if needed

## Future Enhancements

* Add real-time collaboration on notes

* Integrate tags and search functionality

* Deploy to AWS/GCP for scalable production use

* Add dark mode for improved user experience