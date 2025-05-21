from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.core import get_db
from .config import settings
from .models import User
from .schemas import TokenData
from sqlalchemy.future import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def hash_password(password: str) -> str:
    """
    Hash the provided plain-text password using the configured password context.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """

    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain-text password against the given hashed password.

    Args:
        plain_password (str): The plain-text password to check.
        hashed_password (str): The hashed password to compare with.

    Returns:
        bool: True if the password matches the hash, False otherwise.
    """

    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create a new JWT access token with an optional expiration delta.

    Args:
        data (dict): The payload data to encode in the token.
        expires_delta (timedelta | None, optional): The time duration for token expiration. 
            If not provided, the default token expiration setting is used.

    Returns:
        str: The encoded JWT access token.
    """

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Retrieve the currently authenticated user based on a JWT access token.

    Decodes the JWT to extract the user ID and fetches the corresponding user from the database.
    Raises an HTTP 401 exception if the token is invalid or the user does not exist.

    Args:
        token (str): JWT access token provided via dependency injection.
        db (AsyncSession): Asynchronous database session for user retrieval.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the credentials are invalid or the user is not found.
    """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise credentials_exception
    return user
