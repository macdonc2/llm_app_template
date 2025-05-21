from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas import UserCreate, UserRead, UserUpdate
from ..services.user_service import UserService
from ..dependencies import get_user_service
from ..security import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    user_svc: UserService = Depends(get_user_service),
):
    """
    Register a new user if the email address is not already taken.

    Checks for an existing user with the provided email and, if not found,
    delegates user creation to the user service.

    Args:
        user_in (UserCreate): The information required to create a new user.
        user_svc (UserService): Dependency-injected user service for user operations.

    Returns:
        UserRead: The newly created user record.

    Raises:
        HTTPException: If the email is already registered.
    """

    # Optionally check for existing:
    if await user_svc.get_user_by_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    # Delegate creation (including hashing) to your service
    new_user = await user_svc.create_user(user_in)
    return new_user

@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user = Depends(get_current_user),
):
    """
    Retrieve the profile information for the currently authenticated user.

    Args:
        current_user: The currently authenticated user, provided via dependency injection.

    Returns:
        UserRead: The user record of the authenticated user.
    """

    return current_user

@router.patch("/me", response_model=UserRead)
async def update_profile(
    update:       UserUpdate,
    user_svc:     UserService = Depends(get_user_service),
    current_user = Depends(get_current_user),
):
    """
    Update the profile information of the currently authenticated user.

    Applies changes provided by the client, including secure password hashing
    if a new password is submitted, and updates the user's record.

    Args:
        update (UserUpdate): The user-provided fields to update.
        user_svc (UserService): Dependency-injected user service.
        current_user: The currently authenticated user.

    Returns:
        UserRead: The updated user record.
    """
    
    # Build a dict of only the fields the client provided:
    changes = update.model_dump(exclude_none=True)

    # Apply each change dynamically:
    if "password" in changes:
        changes["hashed_password"] = hash_password(changes.pop("password"))

    for field, value in changes.items():
        setattr(current_user, field, value)

    # Call your new update_user method (or upsert):
    updated = await user_svc.update_user(current_user.id, update)
    return updated
