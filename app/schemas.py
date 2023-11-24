"""Module with Pydantic schemas for the API."""

from pydantic import BaseModel


class PostBase(BaseModel):
    """Pydantic model for a post."""
    title: str
    content: str


class PostCreate(PostBase):
    """Pydantic model for a post create."""
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
