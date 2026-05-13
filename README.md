
# Digital Notebook

A REST API for storing and managing personal class notes.

## Stack
FastAPI, PostgreSQL, SQLAlchemy, Docker, Alembic, JWT auth

## Features
- Full CRUD for notes and users
- JWT authentication with protected routes
- Bookmark notes for quick access
- Search, filter, limit and skip query parameters
- Alembic migrations
- 26 pytest tests
- CI/CD with GitHub Actions
- Deployed on Render

## Run locally
```
docker-compose up --build
```

## Live API
https://digital-notebook-l5jz.onrender.com
