"""Tests for schemas.py"""
import pytest

from app import schemas


class TestPost:
    """Test Post schema."""

    def test_post_base(self):
        """Test PostBase schema."""
        post = schemas.PostBase(title="Test", content="Test")
        assert post.title == "Test"
        assert post.content == "Test"

    def test_post_base_empty(self):
        """Test PostBase schema with empty values."""
        post = schemas.PostBase()
        assert post.title is None
        assert post.content is None

    def test_post_create(self):
        """Test PostCreate schema."""
        post = schemas.PostCreate(title="Test", content="Test")
        assert post.title == "Test"
        assert post.content == "Test"

    def test_post_create_empty(self):
        """Test PostCreate raises error with empty values."""
        with pytest.raises(ValueError):
            schemas.PostCreate()

    def test_post_update(self):
        """Test PostUpdate schema."""
        post = schemas.PostUpdate(title="Test", content="Test")
        assert post.title == "Test"
        assert post.content == "Test"

    def test_post_update_empty(self):
        """Test PostUpdate schema with empty values."""
        post = schemas.PostUpdate()
        assert post.title is None
        assert post.content is None

    def test_post(self):
        """Test Post schema."""
        post = schemas.Post(id=1, title="Test", content="Test", owner_id=1)
        assert post.id == 1
        assert post.title == "Test"
        assert post.content == "Test"
        assert post.owner_id == 1


class TestUser:
    """Test User schema."""

    def test_user_base(self):
        """Test UserBase schema."""
        user = schemas.UserBase(email="test")
        assert user.email == "test"

    def test_user_base_empty(self):
        """Tests UserBase schema with empty values raises error."""
        with pytest.raises(ValueError):
            schemas.UserBase()

    def test_user_create(self):
        """Test UserCreate schema."""
        user = schemas.UserCreate(email="test", password="test")
        assert user.email == "test"
        assert user.password == "test"

    def test_user_create_empty(self):
        """Tests UserCreate schema with empty values raises error."""
        with pytest.raises(ValueError):
            schemas.UserCreate()

    def test_user(self):
        """Test User schema."""
        user = schemas.User(id=1, email="test", is_active=True)
        assert user.id == 1
        assert user.email == "test"
        assert user.is_active is True
