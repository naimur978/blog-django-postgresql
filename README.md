# Blog Django PostgreSQL

A Django REST API for a blog application using PostgreSQL as the database backend. This project supports user registration, login, profile updates, post creation, and commenting, with session-based authentication and CSRF protection.


## Table of Contents
- [Dependencies & Software Requirements](#dependencies--software-requirements)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Database Setup](#database-setup)
- [API Endpoints](#api-endpoints)
- [CSRF Protection](#csrf-protection)
- [Using Postman](#using-postman)
# Dependencies & Software Requirements

Before you begin, make sure you have the following installed:

- **Python 3.10+** (recommended: Python 3.13)
- **PostgreSQL 13+**
- **pip** (Python package manager)
- **virtualenv** (optional, for creating isolated Python environments)
- **Git** (for cloning the repository)

Python dependencies are listed in `requirements.txt`:

- Django >= 4.2
- psycopg2 >= 2.9

Install them with:
```sh
pip install -r requirements.txt
```

---

## Features
- User registration, login, logout, and profile update
- Create blog posts and add comments
- Session-based authentication (no token authentication used)
- CSRF protection for all unsafe requests

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/naimur978/blog-django-postgresql.git
   cd blog-django-postgresql
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure your database settings in `blog_django_postgresql/settings.py`:**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'blogdb',
           'USER': 'bloguser',
           'PASSWORD': 'yourpassword',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```


5. **Setup the database:**
    - Access the PostgreSQL shell as the `postgres` user (use `-i` to bypass shell restrictions):
       ```sh
       sudo -u postgres -i psql
       ```

    - Create a PostgreSQL database and user:
       ```sql
       CREATE DATABASE blogdb;
       CREATE USER bloguser WITH PASSWORD 'yourpassword';
       GRANT ALL PRIVILEGES ON DATABASE blogdb TO bloguser;
       ```

    - To list all databases:
       ```sql
       \l
       ```

    - To connect to your new database:
       ```sql
       \c blogdb
       ```

    - To see all tables in the database:
       ```sql
       \dt
       ```

    - Exit the PostgreSQL shell:
       ```sql
       \q
       ```

    - Run migrations:
       ```sh
       python manage.py makemigrations
       python manage.py migrate
       ```

6. **Run the development server:**
   ```sh
   python manage.py runserver 8080
   ```

---


## API Endpoints

All endpoints are prefixed with `/api/`.

### Final API Endpoints

- **Home Page:** `GET /api/` — Lists all blog posts

- **Login:** `POST /api/login/`
- **Logout:** `POST /api/logout/`
- **Register:** `POST /api/register/`
- **Forgot Password:** `POST /api/forgot/`
- **Reset Password:** `POST /api/reset/`

- **Profile:** `GET /api/profile/` — Displays user profile

- **Create Post:** `POST /api/post/`
- **Edit Post:** `POST /api/post/:id/edit/`
- **Delete Post:** `POST /api/post/:id/delete/`
- **Post Details:** `GET /api/post/:id/`

- **Add Comment:** `POST /api/post/:id/comments/`
- **Post Comments:** `GET /api/post/:id/comments/`

- **CSRF Token:** `GET /api/csrf/` — Sets the CSRF cookie for the client

---

## CSRF Protection

This project uses **session authentication** (no token authentication). CSRF protection is enforced for all unsafe requests (POST, PUT, PATCH, DELETE).

- Before making POST/PUT/DELETE requests, you must obtain a CSRF token by sending a GET request to `/api/csrf/`.
- The CSRF token will be set in a cookie named `csrftoken`.
- For all unsafe requests, include the CSRF token in the `X-CSRFToken` header.

### Example (using curl):

1. Get CSRF token:
   ```sh
   curl -c cookies.txt http://localhost:8080/api/csrf/
   ```
2. Use the token for POST requests:
   ```sh
   csrftoken=$(grep csrftoken cookies.txt | awk '{print $7}')
   curl -b cookies.txt -H "X-CSRFToken: $csrftoken" -H "Content-Type: application/json" -X POST http://localhost:8080/api/post/ -d '{"title": "Test", "body": "Content"}'
   ```

---

## Using Postman

- Always use the **"Cookies"** tab in Postman to ensure cookies are preserved between requests.
- If you disable the "CSRF" tab or do not send the CSRF token, your session will not be authenticated for unsafe requests.
- To get the CSRF token:
  1. Send a GET request to `/api/csrf/`.
  2. Copy the value of the `csrftoken` cookie from the response.
  3. For POST/PUT/DELETE requests, add a header:
     ```
     X-CSRFToken: <csrftoken value>
     ```
- If you do not keep the "Cookies" tab enabled, Postman will remove the cookie and you will get CSRF errors.

---

## Notes
- All authentication is session-based. No token authentication is used in this project.
- Make sure your database is running and accessible before starting the server.
- For production, update your `ALLOWED_HOSTS` and set `DEBUG = False` in `settings.py`.
