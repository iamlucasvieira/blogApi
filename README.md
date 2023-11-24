# Blog Platform Backend

This project is the backend implementation of a blogging platform using FastAPI. It allows users to create, edit, browse, and delete blog posts.

## Features

- Create blog posts
- Edit existing posts
- Browse user posts
- Delete posts
- View posts from other users

## Technologies
- FastAPI
- SQLAlchemy 
- Pydantic 
- Uvicorn 

## Design Choices
- FastAPI: Modern, fast, and easy to use framework for building APIs
- Pydantic: Data validation and settings management using Python type annotations
- SQLite: Lightweight database for development

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry

### Installation

Clone the repository:

```bash
git clone
 ```

Install dependencies:

```bash
poetry install
```

Run the server:

```bash
poetry run uvicorn app.main:app --reload
```