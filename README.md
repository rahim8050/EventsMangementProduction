# Event Management System API

This project provides a simple backend API for managing events and RSVPs. It is built with Django and Django REST Framework and uses token based authentication.

## Features

- User registration and token-based authentication

- Role-based permissions for organizers and attendees


- Role-based permissions for organizers and attendees


- Organizers can create and manage events
- Attendees can RSVP to events
- RSVP capacity limit with organizer approval
- Pagination and filtering on event list
- Swagger UI documentation


## Authentication

1. Register a new user at `/api/register/` using an email address and
   specifying a `role` of either `organizer` or `attendee`. Example:
   ```json
   {"email": "john@example.com", "password": "pass", "role": "organizer"}
   ```
2. Obtain an authentication token by POSTing your email and password to
   `/api/token/`. The response includes the user's role:
   ```json
   {"token": "<token>", "user_id": 1, "email": "john@example.com", "role": "organizer"}


## Authentication

1. Register a new user at `/api/register/`. Include `is_organizer=true` in the
   request body to create an organizer account.
2. Obtain an authentication token by POSTing your username and password to
   `/api/token/`. The response includes the user's role:
   ```json
   {"token": "<token>", "user_id": 1, "username": "john", "is_organizer": true}

   ```
3. Include the returned token in the `Authorization: Token <token>` header when
   accessing protected endpoints.
4. Organizer accounts can create and manage events, while regular attendees can
   RSVP to them.


## Setup

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Copy `.env.example` to `.env` and update the values for your PostgreSQL database and secret key.
3. Apply migrations and create a superuser:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Run the development server:
   ```bash
   python manage.py runserver
   ```
5. Access the API documentation at `http://localhost:8000/swagger/`.

## API Endpoints

- `POST /api/register/` – create a new user account with email and role
- `POST /api/token/` – log in with email/password and receive a token plus the
  user's `role`

- `POST /api/register/` – create a new user account
- `POST /api/token/` – log in and receive a token plus the `is_organizer` flag

- `GET /api/events/` – list events with pagination and filtering
- `POST /api/events/` – create an event (organizers only)
- `POST /api/rsvps/` – RSVP to an event (attendees only)
- `POST /api/rsvps/<id>/approve/` – approve an RSVP (event organizer only)





## Running Tests

```bash
python manage.py test
```
