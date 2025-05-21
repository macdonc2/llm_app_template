from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.router import fastapi_users
from app.db.core import get_async_session
from app.db.user import get_user_db
from app.models import User as UserTable
from app.schemas import UserRead

# only superusers may hit any of these routes
current_superuser = fastapi_users.current_user(active=True, superuser=True)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(current_superuser)],
)


@router.get("/pending", response_model=List[UserRead])
async def list_pending_users(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Retrieve a list of users who have not yet been activated.

    Args:
        session (AsyncSession): The asynchronous SQLAlchemy session.

    Returns:
        List[UserRead]: A list of user records for users pending activation.
    """

    result = await session.execute(
        select(UserTable).where(UserTable.is_active == False)
    )
    return result.scalars().all()


@router.post("/approve/{user_id}", response_model=UserRead)
async def approve_user(
    user_id: UUID,
    user_db = Depends(get_user_db),
):
    """
    Approve and activate a user by setting their 'is_active' field to True.

    Args:
        user_id (UUID): The unique identifier of the user to activate.
        user_db: The user database dependency.

    Returns:
        UserRead: The updated user record with activation status.

    Raises:
        HTTPException: If the user with the specified ID is not found.
    """

    user = await user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_db.update(user, {"is_active": True})


@router.post("/verify/{user_id}", response_model=UserRead)
async def verify_user(
    user_id: UUID,
    user_db = Depends(get_user_db),
):
    """
    Verify a user by setting their 'is_verified' field to True.

    Args:
        user_id (UUID): The unique identifier of the user to verify.
        user_db: Dependency for user database access.

    Returns:
        UserRead: The updated user record with verification status.

    Raises:
        HTTPException: If the user with the specified ID is not found.
    """

    user = await user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_db.update(user, {"is_verified": True})

@router.get(
    "/users",
    response_model=List[UserRead],
    summary="List all users (superuser only)",
)
async def list_all_users(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Retrieve a list of all users.

    Args:
        session (AsyncSession): The asynchronous SQLAlchemy session.

    Returns:
        List[UserRead]: A list of all user records.
    """
    
    result = await session.execute(select(UserTable))
    return result.scalars().all()

