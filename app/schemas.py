"""Module with Pydantic schemas for the API."""

from pydantic import BaseModel
from typing import Optional


class PostBase(BaseModel):
    """Pydantic model for a post."""
    title: Optional[str] = None
    content: Optional[str] = None


class PostCreate(PostBase):
    """Pydantic model for a post create."""
    title: str
    content: str


class PostUpdate(PostBase):
    """Pydantic model for a post update."""
    pass


class Post(PostBase):
    """Pydantic model for a post with owner."""
    id: int
    owner_id: int

    class Config:
        """Pydantic model configuration."""
        from_attributes = True


class UserBase(BaseModel):
    """Pydantic model for a user."""
    email: str


class UserCreate(UserBase):
    """Pydantic model for a user create."""
    password: str


class User(UserBase):
    """Pydantic model for a user with id."""
    id: int
    is_active: bool
    posts: list[Post] = []

    class Config:
        """Pydantic model configuration."""
        from_attributes = True
