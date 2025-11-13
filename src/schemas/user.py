from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


# Base schema with common fields
class UserBase(BaseModel):
    """Base schema for User with common fields"""
    username: str = Field(..., min_length=3, max_length=50, description="Username must be between 3 and 50 characters")
    email: EmailStr = Field(..., description="Valid email address")
    full_name: Optional[str] = Field(None, max_length=100, description="User's full name")


# Schema for creating a new user (includes password)
class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


# Schema for updating a user
class UserUpdate(BaseModel):
    """Schema for updating user information"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


# Schema for user response (what we return to the client)
class UserResponse(UserBase):
    """Schema for user response (excludes sensitive data)"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy model


# Schema for user in database (includes all fields)
class UserInDB(UserResponse):
    """Schema for user stored in database (includes hashed password)"""
    hashed_password: str

    class Config:
        from_attributes = True

