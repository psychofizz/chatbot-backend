# Hai

A basic Django + Postgres backend for testing the chatbot. Dockerized for your and my convenience.

## Getting Started

To run the project:

```bash
docker compose build
docker compose up -d
```

The backend runs on port **4000** (since port 8000 is probably busy).

## Features

- Create a user
- Delete a user
- Get user by ID
- Get all users

## Example: Creating a Test User

**Endpoint:** `POST http://localhost:4000/api/customers/`

**Request Body:**

```json
{
    "full_name": "Armando Paredes",
    "phone_number": "99009900",
    "identity_card_number": "0801193105141"
}
```