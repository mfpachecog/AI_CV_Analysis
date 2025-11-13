from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from database.user import get_db
from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.services.user import UserService

# Create router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# CREATE - Create a new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    
    - **username**: Unique username (3-50 characters)
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    - **full_name**: Optional full name
    """
    return UserService.create_user(db, user)


# READ - Get user by ID
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by ID.
    
    - **user_id**: The ID of the user to retrieve
    """
    return UserService.get_user_by_id(db, user_id)


# READ - Get all users
@router.get("/", response_model=List[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all users with pagination.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    return UserService.get_users(db, skip=skip, limit=limit)


# READ - Get user by username
@router.get("/username/{username}", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """
    Get a user by username.
    
    - **username**: The username to search for
    """
    return UserService.get_user_by_username(db, username)


# READ - Get user by email
@router.get("/email/{email}", response_model=UserResponse)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """
    Get a user by email.
    
    - **email**: The email to search for
    """
    return UserService.get_user_by_email(db, email)


# UPDATE - Update user by ID
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user by ID.
    
    - **user_id**: The ID of the user to update
    - **user_update**: User data to update (only provided fields will be updated)
    """
    return UserService.update_user(db, user_id, user_update)


# DELETE - Delete user by ID
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by ID.
    
    - **user_id**: The ID of the user to delete
    """
    UserService.delete_user(db, user_id)
    return None

