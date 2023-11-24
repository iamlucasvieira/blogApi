"""Module for CRUD operations on the database."""

from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_email(db: Session, email: str) -> models.User | None:
    """Get a user by email from the database.

    Args:
        db (Session): The database connection.
        email (str): The email of the user to get.

    Returns:
        models.User | None: The user, if found.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a user in the database.

    Args:
        db (Session): The database connection.
        user (schemas.UserCreate): The user to create.

    Returns:
        models.User: The created user.
    """
    fake_hashed_password = user.password + "fakehash"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> list[models.Post]:
    """Get all posts from the database.

    Args:
        db (Session): The database connection.
        skip (int, optional): The number of posts to skip. Defaults to 0.
        limit (int, optional): The number of posts to return. Defaults to 100.

    Returns:
        list[models.Post]: The posts.
    """
    return db.query(models.Post).offset(skip).limit(limit).all()


def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[models.Post]:
    """Get all posts from the database from a user.

    Args:
        db (Session): The database connection.
        user_id (int): The user id.
        skip (int, optional): The number of posts to skip. Defaults to 0.
        limit (int, optional): The number of posts to return. Defaults to 100.

    Returns:
        list[models.Post]: The posts.
    """
    return (
        db.query(models.Post)
        .filter(models.Post.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_post(db: Session, post_id: int, user_id: int) -> models.Post | None:
    """Get a post from the database.

    Args:
        db (Session): The database connection.
        post_id (int): The post id.
        user_id (int): The user id.

    Returns:
        models.Post | None: The post, if found.
    """
    return (
        db.query(models.Post)
        .filter(models.Post.id == post_id)
        .filter(models.Post.owner_id == user_id)
        .first()
    )


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int) -> models.Post:
    """Create a post in the database.

    Args:
        db (Session): The database connection.
        post (schemas.PostCreate): The post to create.
        user_id (int): The user id.

    Returns:
        models.Post: The created post.
    """
    db_post = models.Post(**post.model_dump(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_user_post(db: Session, post: schemas.PostUpdate, user_id: int, post_id: int) -> models.Post | None:
    """Update a post in the database.

    Args:
        db (Session): The database connection.
        post (schemas.PostUpdate): The post to update.
        user_id (int): The user id.
        post_id (int): The post id.

    Returns:
        models.Post | None: The updated post or None if the post doesn't exist.
    """
    db_post = get_post(db, post_id=post_id, user_id=user_id)

    if db_post:
        # Only update the field that are set in the request.
        for field, value in post.model_dump().items():
            if value is not None:
                setattr(db_post, field, value)

        db.commit()
        db.refresh(db_post)
        return db_post

    return None


def delete_user_post(db: Session, user_id: int, post_id: int) -> models.Post | None:
    """Delete a post from the database.

    Args:
        db (Session): The database connection.
        user_id (int): The user id.
        post_id (int): The post id.

    Returns:
        models.Post | None: The deleted post or None if the post doesn't exist.
    """
    db_post = get_post(db, post_id=post_id, user_id=user_id)

    # If the post doesn't exist, return None.
    if db_post:
        db.delete(db_post)  # type: ignore
        db.commit()
        return db_post

    return None
