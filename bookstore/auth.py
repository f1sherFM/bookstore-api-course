"""
Authentication and Authorization System

This module handles user authentication and authorization for our BookStore API.
It provides secure user login, password management, and JWT token-based authentication.

Key Security Concepts for Beginners:

1. Password Hashing: We never store passwords in plain text. Instead, we use bcrypt
   to create a "hash" - a scrambled version that can't be reversed.

2. JWT Tokens: JSON Web Tokens are like "digital tickets" that prove a user is logged in.
   They contain encrypted information about the user and expire after a set time.

3. OAuth2: A standard protocol for secure authentication. We use the "password flow"
   where users provide username/password and get back a token.

4. Dependencies: FastAPI's dependency injection system automatically checks if users
   are authenticated before allowing access to protected endpoints.

Security Features:
- Bcrypt password hashing with salt
- JWT tokens with expiration
- User activation/deactivation
- Superuser permissions
- Secure credential validation
"""

import bcrypt  # Industry-standard password hashing library
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt  # JSON Web Token library
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer  # OAuth2 authentication scheme
from sqlalchemy.orm import Session

# Import our custom modules
from .database import get_db
from .models import User
from .schemas import TokenData
from .config import settings

# OAuth2 Configuration
# This tells FastAPI where users should go to get their authentication tokens
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Password Security Functions

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password
    
    This function checks if a user's entered password matches the hashed password
    stored in our database. It uses bcrypt's secure comparison method.
    
    Args:
        plain_password (str): The password the user entered (plain text)
        hashed_password (str): The hashed password from our database
        
    Returns:
        bool: True if passwords match, False otherwise
        
    For beginners: This is like checking if a key fits a lock. We take the
    password the user typed, hash it the same way we did when they registered,
    and see if it matches what we have stored.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    """
    Hash a plain text password for secure storage
    
    This function takes a plain text password and creates a secure hash using bcrypt.
    The hash includes a random "salt" to prevent rainbow table attacks.
    
    Security Features:
    - Uses bcrypt with automatic salt generation
    - Truncates passwords to 72 bytes (bcrypt limitation)
    - Validates password is not empty
    
    Args:
        password (str): Plain text password to hash
        
    Returns:
        str: Securely hashed password ready for database storage
        
    Raises:
        ValueError: If password is empty or None
        
    For beginners: This is like putting your password through a "scrambler"
    that turns it into gibberish. Even if someone steals our database,
    they can't see the original passwords.
    """
    if not password or len(password.strip()) == 0:
        raise ValueError("Password cannot be empty")
    
    # Convert password to bytes for bcrypt
    password_bytes = password.encode('utf-8')
    
    # Bcrypt has a 72-byte limit, so we truncate if necessary
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    
    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()  # Creates a random salt for this password
    hashed = bcrypt.hashpw(password_bytes, salt)
    
    return hashed.decode('utf-8')  # Convert back to string for database storage


# User Lookup Functions

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """
    Find a user by their username
    
    Args:
        db (Session): Database session
        username (str): Username to search for
        
    Returns:
        Optional[User]: User object if found, None otherwise
        
    For beginners: This searches our user database for someone with
    a specific username, like looking up a contact in your phone.
    """
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Find a user by their email address
    
    Args:
        db (Session): Database session
        email (str): Email address to search for
        
    Returns:
        Optional[User]: User object if found, None otherwise
        
    For beginners: Similar to username lookup, but searches by email address.
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, username: str, password: str) -> Union[User, bool]:
    """
    Authenticate a user with username and password
    
    This is the main authentication function that:
    1. Looks up the user by username
    2. Verifies their password
    3. Returns the user if authentication succeeds
    
    Args:
        db (Session): Database session
        username (str): Username provided by user
        password (str): Plain text password provided by user
        
    Returns:
        Union[User, bool]: User object if authentication succeeds, False if it fails
        
    For beginners: This is like the "login check" - it verifies that the
    username exists and the password is correct. If both are good, you get
    the user's information. If not, you get False.
    """
    # First, find the user by username
    user = get_user_by_username(db, username)
    if not user:
        return False  # User doesn't exist
    
    # Then, check if the password is correct
    if not verify_password(password, user.hashed_password):
        return False  # Password is wrong
    
    return user  # Authentication successful!


# JWT Token Management

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token for authenticated users
    
    JWT (JSON Web Token) is like a "digital passport" that proves a user is logged in.
    The token contains encrypted information about the user and has an expiration time.
    
    How it works:
    1. We take user information (like username)
    2. Add an expiration time
    3. Encrypt it all into a token string
    4. The user includes this token in future API requests to prove they're logged in
    
    Args:
        data (dict): Information to include in the token (usually {"sub": username})
        expires_delta (Optional[timedelta]): How long the token should be valid
        
    Returns:
        str: Encrypted JWT token string
        
    For beginners: This creates a "ticket" that proves you're logged in.
    Like a concert ticket, it has your information and an expiration time.
    You show this ticket (include it in API requests) to prove you belong there.
    """
    # Make a copy of the data so we don't modify the original
    to_encode = data.copy()
    
    # Set the expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Use default expiration time from settings
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    
    # Add expiration time to the token data
    to_encode.update({"exp": expire})
    
    # Create and return the encrypted token
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


# FastAPI Dependencies for Authentication
# These functions are used by FastAPI to automatically check if users are authenticated

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from a JWT token
    
    This function is used as a FastAPI dependency to automatically:
    1. Extract the JWT token from the request headers
    2. Decrypt and validate the token
    3. Look up the user in the database
    4. Return the user object if everything is valid
    
    Args:
        token (str): JWT token from Authorization header (injected by FastAPI)
        db (Session): Database session (injected by FastAPI)
        
    Returns:
        User: The authenticated user object
        
    Raises:
        HTTPException: 401 Unauthorized if token is invalid or user not found
        
    For beginners: This is like a "bouncer" at a club who checks your ID.
    FastAPI automatically calls this function for protected endpoints to make
    sure the user has a valid "ticket" (JWT token) and is who they claim to be.
    """
    # Create a standard error for authentication failures
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decrypt the JWT token
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        
        # Extract the username from the token
        username: str = payload.get("sub")  # "sub" is the standard JWT field for subject (username)
        if username is None:
            raise credentials_exception
            
        # Create a token data object
        token_data = TokenData(username=username)
        
    except JWTError:
        # Token is invalid, expired, or corrupted
        raise credentials_exception
    
    # Look up the user in the database
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        # Token is valid but user doesn't exist (maybe user was deleted)
        raise credentials_exception
        
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current user and ensure they are active
    
    This builds on get_current_user by adding an additional check:
    the user must be marked as "active" in the database.
    
    Args:
        current_user (User): Current authenticated user (injected by get_current_user)
        
    Returns:
        User: The authenticated and active user
        
    Raises:
        HTTPException: 400 Bad Request if user is inactive
        
    For beginners: This is like checking that your membership card is not only
    valid, but also that your membership hasn't been suspended. Some users
    might be temporarily deactivated by administrators.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current user and ensure they have superuser privileges
    
    This is used for admin-only endpoints that require elevated permissions.
    
    Args:
        current_user (User): Current authenticated user (injected by get_current_user)
        
    Returns:
        User: The authenticated superuser
        
    Raises:
        HTTPException: 403 Forbidden if user is not a superuser
        
    For beginners: This is like checking for a "VIP pass" - not only do you
    need to be logged in, but you need special administrator privileges to
    access certain functions like creating/deleting books.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user


def check_user_permissions(current_user: User, target_user_id: int) -> bool:
    """
    Check if a user has permission to access another user's data
    
    This implements a simple permission system:
    - Superusers can access anyone's data
    - Regular users can only access their own data
    
    Args:
        current_user (User): The user making the request
        target_user_id (int): The ID of the user whose data is being accessed
        
    Returns:
        bool: True if access is allowed, False otherwise
        
    For beginners: This is like checking if you're allowed to open someone's
    locker. You can always open your own locker, and teachers (superusers)
    can open any locker, but students can't open other students' lockers.
    """
    return current_user.is_superuser or current_user.id == target_user_id