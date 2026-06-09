from uuid import UUID

from fastapi import APIRouter, Depends

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.dependencies.session import get_session, SessionDep
from src.dependencies.user_service import get_user_service, UserServiceDep
from src.schemas.users import UserCreate, UserUpdate, UserOut, UserExternal


router = APIRouter(
    prefix="/api/v1/users_profiles",
    tags=['Пользователи и профили'],
    dependencies=[
        Depends(get_session),
        Depends(get_user_service),
    ]
)


@router.post("/users", status_code=HTTP_201_CREATED)
async def create_user(
        user: UserCreate,
        session: SessionDep,
        user_service: UserServiceDep
) -> UserOut:
    return await user_service.create_user_db(user, session)


@router.get("/users/{user_id}")
async def get_users(
        user_id: UUID,
        session: SessionDep,
        user_service: UserServiceDep
) -> UserOut:
    return await user_service.get_users_with_profile(user_id, session)


@router.patch("/users/{user_id}")
async def edit_user_by_id(
        user_id: UUID,
        edited_user: UserUpdate,
        session: SessionDep,
        user_service: UserServiceDep
) -> UserOut:
    return await user_service.update_user_db(user_id, edited_user, session)


@router.delete("/users/{user_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: UUID,
        session: SessionDep,
        user_service: UserServiceDep
):
    return await user_service.delete_user_db(user_id, session)


@router.post("/external_user")
async def create_internal(
        user: UserExternal,
        session: SessionDep,
        user_service: UserServiceDep
) -> UserOut:
    return await user_service.create_external_user(user, session)