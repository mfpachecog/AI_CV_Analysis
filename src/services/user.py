from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from passlib.context import CryptContext

from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    """Service class for User business logic"""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def check_username_exists(db: Session, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """Check if username already exists in database"""
        query = db.query(User).filter(User.username == username)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None
    
    @staticmethod
    def check_email_exists(db: Session, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """Check if email already exists in database"""
        query = db.query(User).filter(User.email == email)
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        return query.first() is not None
    
    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        """
        Create a new user in the database.
        
        Args:
            db: Database session
            user: User creation schema
            
        Returns:
            Created User object
            
        Raises:
            HTTPException: If username or email already exists
        """
        # Check if username already exists
        if UserService.check_username_exists(db, user.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if UserService.check_email_exists(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        hashed_password = UserService.get_password_hash(user.password)
        
        # Create new user
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=True,
            is_superuser=False
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get a user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found
        """
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return db_user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """
        Get a user by username.
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found
        """
        db_user = db.query(User).filter(User.username == username).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with username '{username}' not found"
            )
        return db_user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Get a user by email.
        
        Args:
            db: Database session
            email: Email address
            
        Returns:
            User object
            
        Raises:
            HTTPException: If user not found
        """
        db_user = db.query(User).filter(User.email == email).first()
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with email '{email}' not found"
            )
        return db_user
    
    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get all users with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of User objects
        """
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        """
        Update a user by ID.
        
        Args:
            db: Database session
            user_id: User ID to update
            user_update: User update schema with fields to update
            
        Returns:
            Updated User object
            
        Raises:
            HTTPException: If user not found or validation fails
        """
        # Get user
        db_user = UserService.get_user_by_id(db, user_id)
        
        # Get update data (only fields that were provided)
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Check if username is being updated and if it's already taken
        if "username" in update_data:
            if UserService.check_username_exists(db, update_data["username"], exclude_user_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )
        
        # Check if email is being updated and if it's already taken
        if "email" in update_data:
            if UserService.check_email_exists(db, update_data["email"], exclude_user_id=user_id):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )
        
        # If password is being updated, hash it
        if "password" in update_data:
            update_data["hashed_password"] = UserService.get_password_hash(update_data.pop("password"))
        
        # Update user fields
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        """
        Delete a user by ID.
        
        Args:
            db: Database session
            user_id: User ID to delete
            
        Raises:
            HTTPException: If user not found
        """
        # Get user (will raise exception if not found)
        db_user = UserService.get_user_by_id(db, user_id)
        
        db.delete(db_user)
        db.commit()
        
        return None
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        
        Args:
            db: Database session
            username: Username
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

