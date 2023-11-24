# Blog Platform Backend
![example workflow](https://github.com/iamlucasvieira/blogApi/actions/workflows/ci.yml/badge.svg)

This project is the backend implementation of a blogging platform using FastAPI. It allows users to create, edit,
browse, and delete blog posts.

## Features

- Create blog posts
- Edit existing posts
- Delete posts
- View posts from other users
- View own posts

## Technologies

- FastAPI
- SQLAlchemy
- Sqlite
- Pydantic
- Uvicorn

## Design Choices

- FastAPI: Modern, fast, and easy to use framework for building APIs
- Pydantic: Data validation and settings management using Python type annotations
- Sqlite: Lightweight database for development

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry

### Installation

Clone the repository:

```bash
git clone https://github.com/iamlucasvieira/blogApi.git
 ```

Install dependencies:

```bash
poetry install
```

## Usage

### Run the server

```bash
poetry run uvicorn app.main:app --reload
```

### Test the API

Go to [localhost:8000/docs](localhost:8000/docs) to view the FastApi docs and test the API

### Run tests

```bash
poetry run pytest
```

### Run linters, and formatters

```bash
poetry run nox 
```