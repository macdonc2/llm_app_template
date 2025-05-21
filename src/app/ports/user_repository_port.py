from abc import ABC, abstractmethod
from app.models import User
from app.schemas import UserCreate

class UserRepositoryPort(ABC):
    """
    Abstract base class defining the interface for user repository adapters.

    Methods:
        create_user(user: UserCreate) -> User:
            Asynchronously create a new user in the repository.

        get_user_by_email(email: str) -> User | None:
            Asynchronously retrieve a user by their email address.

        get_by_id(user_id: str) -> User | None:
            Asynchronously retrieve a user by their unique identifier.

        update(user: User) -> User:
            Asynchronously update a user's information in the repository.
    """

    @abstractmethod
    async def create_user(self, user: UserCreate) -> User:
        """
        Asynchronously create a new user.

        Args:
            user (UserCreate): The user creation data.

        Returns:
            User: The newly created user object.
        """
        ...
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        """
        Asynchronously retrieve a user by their email address.

        Args:
            email (str): The user's email address.

        Returns:
            User | None: The user object if found, else None.
        """
        ...
    
    @abstractmethod
    async def get_by_id(self, user_id: str) -> User | None: 
        """
        Asynchronously retrieve a user by their unique identifier.

        Args:
            user_id (str): The user's unique identifier.

        Returns:
            User | None: The user object if found, else None.
        """
        ...

    @abstractmethod
    async def update(self, user: User) -> User: 
        """
        Asynchronously update an existing user's information.

        Args:
            user (User): The user object with updated information.

        Returns:
            User: The updated user object.
        """
        ...
