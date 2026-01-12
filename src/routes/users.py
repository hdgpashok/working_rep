from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.db import get_session, SessionDep
from src.schemas.users import UserCreate, UserUpdate, UserOut, UserExternal

from src.services.users import UserService


router = APIRouter(
    prefix="/api/v1/users_profiles",
    tags=['Пользователи и профили'],
    dependencies=[Depends(get_session)]
)


@router.post("/users", status_code=HTTP_201_CREATED)
async def create_user(user: UserCreate, session: SessionDep) -> UserOut:
    return await UserService.create_user_db(user, session)


@router.get("/users/{user_id}")
async def get_users(user_id: UUID, session: SessionDep) -> UserOut:
    return await UserService.get_users_with_profile(user_id, session)


@router.patch("/users/{user_id}")
async def edit_user_by_id(user_id: UUID, edited_user: UserUpdate, session: SessionDep) -> UserOut:
    return await UserService.update_user_db(user_id, edited_user, session)


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, session: SessionDep):
    return await UserService.delete_user_db(user_id, session)


@router.post("/external_user")
async def create_internal(user: UserExternal, session: SessionDep) -> UserOut:
    return await UserService.create_external_user(user, session)