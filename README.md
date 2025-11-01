# Lab Submission: Course 10, Module 2 - Authenticating Users

This repository contains my solution for the "Authenticating Users" lab. The goal is to implement a complete authentication workflow (login, logout, and session checking) in a Flask-RESTful backend, building on the existing blog site. The work follows the patterns and rubric from the Flatiron lesson.

## Features

  * **Login:** Implemented a `Login` resource (`POST /login`) that verifies a user by `username` and creates a persistent session by storing the `user_id`.
  * **Logout:** Implemented a `Logout` resource (`DELETE /logout`) that destroys the session by clearing the `user_id`.
  * **Session Check:** Implemented a `CheckSession` resource (`GET /check_session`) to allow the frontend to verify an active session on page load.
  * **Structural Integrity:** Resolved structural import conflicts between the Flask app, seed scripts, and pytest runner to ensure all components function correctly within a consistent environment.

## Environment

  * **Backend:** Python 3.13.7 (via `pipenv`), Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-RESTful, Marshmallow
  * **Frontend:** React (via `npm`)
  * **Testing:** `pytest`

## Setup

Please follow these steps to ensure the environment is built correctly. The database commands must be run from within the `server/` directory due to the project's import structure.

1.  Clone and enter the project directory:

    ```bash
    git clone https://github.com/walbeck85/flask-authenticating-users-lab
    cd flask-authenticating-users-lab
    ```

2.  Install backend and frontend dependencies:

    ```bash
    pipenv install
    npm install --prefix client
    ```

3.  Activate the virtual environment:

    ```bash
    pipenv shell
    ```

4.  Build and seed the database:

    ```bash
    # From the project root, navigate into the server directory
    cd server

    # Set the Flask app context for this directory
    export FLASK_APP=app.py

    # Run migrations and seed the database
    flask db upgrade
    python seed.py

    # Return to the project root
    cd ..
    ```

## How to Run the Application

The application requires two terminals to run the backend and frontend concurrently.

**Terminal 1: Run the Backend (Flask)**

```bash
# Activate the virtual environment if not already active
pipenv shell

# Navigate into the server directory
cd server

# Set the Flask app context
export FLASK_APP=app.py

# Run the application
python app.py
```

**Terminal 2: Run the Frontend (React)**

```bash
# From the project root
npm start --prefix client
```

The React app will open at `http://localhost:3000` and is proxied to the Flask server at `http://localhost:5555`.

## Tests

Run the test suite from the project **root** with the virtual environment active.

```bash
pytest -x -v
```

## Rubric Alignment

  * **Login (`POST /login`):** Retrieves a user by `username`, sets `session['user_id']` to the `user.id`, and returns the serialized user object with a 200 status.
  * **Logout (`DELETE /logout`):** Removes the `user_id` from the session (by setting it to `None`) and returns an empty dictionary with a 204 status.
  * **Check Session (`GET /check_session`):**
      * If `session['user_id']` exists, returns the full user object with a 200 status.
      * If `session['user_id']` does not exist, returns an empty dictionary with a 401 status, as required by the tests.

## Branch and PR Workflow

All work was completed on a `feature/login` branch. This branch includes the core logic for the three endpoints as well as the necessary structural fixes to align the import paths for Flask, the seed script, and pytest. This branch was merged into `main` after all tests passed.

## Instructor Checklist

To verify the submission:

1.  `pipenv install && npm install --prefix client`
2.  `pipenv shell`
3.  `cd server`
4.  `export FLASK_APP=app.py`
5.  `flask db upgrade && python seed.py`
6.  `cd ..`
7.  `pytest -x -v` (from project root) to verify all 3 tests pass.
8.  (Optional) Run the backend (`cd server && python app.py`) and frontend (`npm start --prefix client`) to test login/logout in the browser.