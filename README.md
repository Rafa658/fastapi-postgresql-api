# FastAPI + PostgreSQL Todo API

## PostgreSQL Database

PostgreSQL 15.3 was used in this application. By default, the database `postgres` is used, alongside the password `123` (as specified at core `core/database/database.ini`).

## Starting API

1. Run `py main.py`
2. API will run at port 8000 by default (`http://localhost:8000`)

## Auth Routes

#### POST `/auth`

Creates a new user at database. Expected request JSON syntax:

```
{
    "username": "user1",
    "password: "123"
}
```

Returns success message upon registration

#### POST `/auth/token`

Authenticate users. Expected request JSON syntax:

```
{
    "username": "user1",
    "password: "123"
}
```

If user exists returns access token:

```
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWZvbGxvIiwiZXhwIjoxNjkxMDAzNTY1fQ.0ehE2LamPXwYv9n2EQVSOrR8WhmnzwfwY29ZAImasvM",
    "token_type": "bearer"
}
```

Else, raises 401 Unauthorized status code.

#### GET `/protected`

If token is valid, returns a payload. Expected syntax for request:

```
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWZvbGxvIiwiZXhwIjoxNjkwOTk3OTE0fQ.V882VlfHez0MMhBgl1cI8Hz8IIiqzs4dJl0SYsJUC34f"
}
```

If token is valid, returns user's name. Else, returns 401 Unauthorized status code.

## Todo routes

Routes marked with `*` are protected by JWT auth. In order to access them, you must pass an <strong>Authorization</strong> header containing the token obtained in auth as <strong>Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyYWZvbGxvIiwiZXhwIjoxNjkwOTk3OTE0fQ.V882VlfHez0MMhBgl1cI8Hz8IIiqzs4dJl0SYsJUC34f</strong> (for the token shown).

#### GET `/todos`

Returns all todos in database. These contain three fields: <strong>titulo</strong> (title), <strong>descr</strong> (description) and <strong>status</strong>. containing respectively 20, 50 and 1 character(s), alongside a serialized <strong>user_id</strong> (must be 'P' for pending or 'C' for concluded).

#### POST `/todos` *

Add a todo to todos table. If JSON body does not have either of the three fields, returns 400 Bad Request status code. By default, adds a todo at 'P' status. Expected syntax:

```
{
    "titulo": "Todo #1",
    "descr": "Let's get started!"
}
```

#### PUT `/todos` *

Alters a todo status from 'P' to 'C'. Expected syntax:

```
{
    "titulo": "Todo #1"
}
```

If todo does not exist, returns 404 Not Found status code.

#### DELETE `/todos` *

Delete a todo. Expected syntax:

```
{
    "titulo": "Todo #1"
}
```

If todo does not exist, returns 404 Not Found status code.