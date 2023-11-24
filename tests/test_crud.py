"""Tests for the crud module."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas

# Create a SQLAlchemy engine for testing.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SQLAlchemy session for testing.
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a database for the tests and delete it."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.rollback()
    Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    """Test creating a user."""
    user = schemas.UserCreate(email="test", password="test")
    db_user = crud.create_user(db=db, user=user)
    assert db_user.email == user.email
    assert hasattr(db_user, "hashed_password")


def test_create_user_same_email(db):
    """Test creating a user with the same email raises error."""
    user_1 = schemas.UserCreate(email="test", password="test")
    user_2 = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user_1)
    with pytest.raises(Exception):
        crud.create_user(db=db, user=user_2)


def test_get_user_by_email(db):
    """Test getting a user by email."""
    user = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user)
    db_user = crud.get_user_by_email(db=db, email=user.email)
    assert db_user is not None
    assert db_user.email == user.email


def test_get_user_by_email_not_found(db):
    """Test getting a user by email when not found."""
    db_user = crud.get_user_by_email(db=db, email="test")
    assert db_user is None


def test_post(db):
    """Test creating a post."""
    user = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user)
    post = schemas.PostCreate(title="test", content="test")
    db_post = crud.create_user_post(db=db, post=post, user_id=1)
    assert db_post.title == post.title
    assert db_post.content == post.content
    assert db_post.owner_id == 1


def test_delete_post(db):
    """Test deleting a post."""
    user = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user)
    post = schemas.PostCreate(title="test", content="test")
    crud.create_user_post(db=db, post=post, user_id=1)
    crud.delete_user_post(db=db, user_id=1, post_id=1)
    db_post = crud.get_post(db=db, post_id=1, user_id=1)
    assert db_post is None


@pytest.mark.parametrize("update_dict", [{"title": "test2"}, {"title": "test3", "content": "test2"}])
def test_update_post(db, update_dict):
    """Test updating a post."""
    # each user is unique for each mark.parametrize
    user = schemas.UserCreate(email=update_dict["title"], password="test")
    crud.create_user(db=db, user=user)
    post = schemas.PostCreate(title="test", content="test")
    crud.create_user_post(db=db, post=post, user_id=1)
    post_update = schemas.PostUpdate(**update_dict)
    crud.update_user_post(db=db, post=post_update, user_id=1, post_id=1)
    db_post = crud.get_post(db=db, post_id=1, user_id=1)
    if "title" in update_dict:
        assert db_post.title == post_update.title
    if "content" in update_dict:
        assert db_post.content == post_update.content
    assert db_post.owner_id == 1


def test_get_posts(db):
    """Test getting all posts."""
    user = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user)
    post_1 = schemas.PostCreate(title="test", content="test")
    post_2 = schemas.PostCreate(title="test2", content="test2")
    crud.create_user_post(db=db, post=post_1, user_id=1)
    crud.create_user_post(db=db, post=post_2, user_id=1)
    db_posts = crud.get_posts(db=db, skip=0, limit=100)
    assert len(db_posts) == 2
    assert db_posts[0].title == post_1.title
    assert db_posts[1].title == post_2.title


def test_get_posts_by_user(db):
    """Test getting all posts by a user."""
    user_1 = schemas.UserCreate(email="test", password="test")
    user_2 = schemas.UserCreate(email="test2", password="test2")
    crud.create_user(db=db, user=user_1)
    crud.create_user(db=db, user=user_2)
    post_1 = schemas.PostCreate(title="test", content="test")
    post_2 = schemas.PostCreate(title="test2", content="test2")
    crud.create_user_post(db=db, post=post_1, user_id=1)
    crud.create_user_post(db=db, post=post_2, user_id=2)
    db_posts = crud.get_user_posts(db=db, user_id=1, skip=0, limit=100)
    assert len(db_posts) == 1
    assert db_posts[0].title == post_1.title
    assert db_posts[0].owner_id == 1


def test_get_post(db):
    """Test getting a post."""
    user = schemas.UserCreate(email="test", password="test")
    crud.create_user(db=db, user=user)
    post = schemas.PostCreate(title="test", content="test")
    crud.create_user_post(db=db, post=post, user_id=1)
    db_post = crud.get_post(db=db, post_id=1, user_id=1)
    assert db_post.title == post.title
    assert db_post.content == post.content
    assert db_post.owner_id == 1
