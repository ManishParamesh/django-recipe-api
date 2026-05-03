# Recipe API

A Django REST Framework backend for managing recipes, ingredients, and tags. The API is designed as a backend for web or mobile recipe applications and includes JWT authentication, user-owned recipe data, filtering, and a browsable API for development.

## Features

- User registration and profile management
- JWT authentication with access and refresh tokens
- Recipe CRUD API
- Tags and ingredients API
- Attach tags and ingredients to recipes
- Filter recipes by tag or ingredient ids
- Image field support for recipes
- Django admin support
- Test coverage for auth and recipe workflows

## Tech Stack

- Python 3.14
- Django 6
- Django REST Framework
- Simple JWT
- SQLite for local development

## Project Structure

```text
app/
  app/       Django project settings and URLs
  core/      Custom user model and auth API
  recipe/    Recipe, tag, and ingredient API
  manage.py
```

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Apply migrations:

```powershell
python app\manage.py migrate
```

Add sample data:

```powershell
python app\manage.py seed_data
```

Run the development server:

```powershell
python app\manage.py runserver
```

Open the browsable API:

```text
http://127.0.0.1:8000/api/recipes/
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/api/auth/register/` | Create a user account |
| POST | `/api/auth/token/` | Get JWT access and refresh tokens |
| POST | `/api/auth/token/refresh/` | Refresh an access token |
| GET/PATCH | `/api/auth/me/` | View or update the logged-in user |
| GET/POST | `/api/recipes/` | List or create recipes |
| GET/PATCH/DELETE | `/api/recipes/<id>/` | Retrieve, update, or delete a recipe |
| GET/POST | `/api/tags/` | List or create tags |
| GET/POST | `/api/ingredients/` | List or create ingredients |

## Authentication

Create a token:

```powershell
curl -X POST http://127.0.0.1:8000/api/auth/token/ `
  -H "Content-Type: application/json" `
  -d "{\"username\":\"chef\",\"password\":\"testpass123\"}"
```

Use the access token for protected requests:

```text
Authorization: Bearer <access-token>
```

The sample data command creates this demo user:

```text
username: chef
password: testpass123
```

## Filtering Recipes

Filter by tag ids:

```text
/api/recipes/?tags=1,2
```

Filter by ingredient ids:

```text
/api/recipes/?ingredients=1,3
```

## Tests

Run all tests:

```powershell
python app\manage.py test core recipe
```

## Notes

This project is configured for local development. Before deploying, move sensitive settings such as `SECRET_KEY`, `DEBUG`, database credentials, and allowed hosts into environment variables.
