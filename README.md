# Scientific Computing API

A modular scientific computing backend built with FastAPI. The project separates numerical computation from the API layer, while also including a small browser frontend for authenticated research notes.

## Features

### Scientific API

* Linear algebra endpoints for determinants, inverses, transposes, traces, eigenvalues, eigenvectors, and matrix arithmetic
* Statistics endpoints for mean, standard deviation, variance, minimum, maximum, and summaries
* Ordinary differential equation endpoints for Euler and Runge-Kutta 4 methods
* Request validation with Pydantic response models
* OpenAPI documentation through FastAPI

### Authenticated Notes

* User registration and login
* JWT bearer token authentication
* User-specific notes
* Create, list, read, update, and delete note endpoints
* Browser frontend for login, registration, and note management
* Admin panel for managing users

## Project Structure

```text
app/
|-- api/
|   |-- routes/
|   |-- services/
|   `-- main.py
|-- db/
|   |-- crud.py
|   |-- database.py
|   |-- models.py
|   `-- schemas.py
`-- engine/
    |-- linalg/
    |-- ode/
    `-- stats/

frontend/
|-- css/
|-- js/
|-- index.html
|-- login.html
|-- admin.html
`-- notes.html

tests/
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a local environment file:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` and replace `JWT_SECRET_KEY` with a long random value.

## Running the API

Start the FastAPI server:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.api.main:app --reload --port 8001
```

API documentation is available at:

```text
http://127.0.0.1:8001/docs
```

Health check:

```text
http://127.0.0.1:8001/health
```

## Running the Frontend

Start a static file server from the `frontend` directory:

```powershell
cd frontend
..\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1
```

Or from the project root:

```powershell
.\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Open the frontend:

```text
http://127.0.0.1:5500/login.html
```

Register a user, log in, and then create notes. Notes are scoped to the logged-in user, so one user cannot see or modify another user's notes.

The first registered user is created as an admin. Admin users see an `Admin` button on the notes page.

## Authentication Flow

Register:

```http
POST /auth/register
```

```json
{
    "username": "alice",
    "email": "alice@example.com",
    "password": "valid-password"
}
```

Log in:

```http
POST /auth/login
```

```json
{
    "username": "alice",
    "password": "valid-password"
}
```

The login response includes an access token:

```json
{
    "access_token": "<jwt>",
    "token_type": "bearer"
}
```

Use that token with note endpoints:

```http
Authorization: Bearer <jwt>
```

## Notes API

Create a note:

```http
POST /notes/
```

```json
{
    "title": "Experiment notes",
    "content": "Initial observations..."
}
```

List the current user's notes:

```http
GET /notes/
```

Get, update, or delete one of the current user's notes:

```http
GET /notes/{note_id}
PUT /notes/{note_id}
DELETE /notes/{note_id}
```

Requests without a bearer token return `401`. Requests for another user's note return `404`.

## Admin Users API

Admin endpoints require a bearer token for a user with `is_admin=true`.

List users:

```http
GET /admin/users
```

Update a user:

```http
PUT /admin/users/{user_id}
```

```json
{
    "username": "new-username",
    "email": "new-email@example.com",
    "is_admin": true
}
```

Delete a user and that user's notes:

```http
DELETE /admin/users/{user_id}
```

Admins cannot delete their own account or remove their own admin access.

## Scientific API Examples

Determinant:

```http
POST /linalg/determinant
```

```json
{
    "matrix": [
        [1, 2],
        [3, 4]
    ]
}
```

Statistics summary:

```http
POST /stats/summary
```

```json
{
    "vector": [1, 2, 3, 4, 5]
}
```

Euler method:

```http
POST /ode/euler
```

```json
{
    "y0": 1.0,
    "t0": 0.0,
    "step_size": 0.5,
    "steps": 3
}
```

## Running Tests

Run the full test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

The tests cover:

* Scientific endpoint success and validation paths
* Authentication validation
* Password length handling for bcrypt
* User-specific note access
* Cross-user note isolation for list, read, update, and delete operations
* Admin-only user management

## Database

By default, the app uses SQLite at:

```text
notes.db
```

You can override the database by setting `DATABASE_URL`.

For local SQLite databases, startup includes a compatibility check that adds the `notes.user_id` column when needed. Existing notes without an owner are not returned to any user.

## Design Goals

* Keep computation logic reusable outside the API layer
* Use typed request and response models
* Enforce authentication and note ownership in the backend
* Keep the frontend simple enough to run without a build step
* Maintain automated tests for API behavior and access control

## Live API

<https://scientific-api-1ufm.onrender.com>

## API Documentation

<https://scientific-api-1ufm.onrender.com/docs>
