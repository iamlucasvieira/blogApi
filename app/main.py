from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import Generator

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)  # type: ignore

app = FastAPI()


# Dependency
def get_db() -> Generator[Session, None, None]:
    """Get a database connection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """Create a user.

    Args:
        user (schemas.UserCreate): The user to create.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        schemas.User: The created user.
    """
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post("/users/{user_id}/post/", response_model=schemas.Post)
def create_post_for_user(
        user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)
) -> models.Post:
    """Create a post for a user.

    Args:
        user_id (int): The user id.
        post (schemas.PostCreate): The post to create.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        schemas.Post: The created post.
    """
    return crud.create_user_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> list[models.Post]:
    """Get all posts.

    Args:
        skip (int, optional): The number of posts to skip. Defaults to 0.
        limit (int, optional): The number of posts to return. Defaults to 100.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        list[schemas.Post]: The posts.
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@app.get("/users/{user_id}/posts/", response_model=list[schemas.Post])
def read_user_posts(
        user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[models.Post]:
    """Get all posts from a user.

    Args:
        user_id (int): The user id.
        skip (int, optional): The number of posts to skip. Defaults to 0.
        limit (int, optional): The number of posts to return. Defaults to 100.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        list[schemas.Post]: The posts.
    """
    posts = crud.get_user_posts(db, user_id=user_id, skip=skip, limit=limit)
    return posts


@app.delete("/users/{user_id}/posts/{post_id}", response_model=schemas.Post)
def delete_post(user_id: int, post_id: int, db: Session = Depends(get_db)) -> models.Post:
    """Delete a post from a user.

    Args:
        user_id (int): The user id.
        post_id (int): The post id.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        schemas.Post: The deleted post.
    """
    post = crud.get_post(db, post_id=post_id, user_id=user_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)  # type: ignore
    db.commit()
    return post


@app.put("/users/{user_id}/posts/{post_id}", response_model=schemas.Post)
def update_post(
        user_id: int, post_id: int, post: schemas.PostUpdate, db: Session = Depends(get_db)
) -> models.Post:
    """Update a post from a user.

    Args:
        user_id (int): The user id.
        post_id (int): The post id.
        post (schemas.PostUpdate): The post to update.
        db (Session, optional): The database connection. Defaults to Depends(get_db).

    Returns:
        schemas.Post: The updated post.
    """
    db_post = crud.update_user_post(db, post, user_id, post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.get("/")
def root() -> dict[str, str]:
    """Root route.

    Returns:
        dict[str, str]: The root route.
    """
    return {"message": "Hello World"}
