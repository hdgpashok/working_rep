from typing import Annotated

from fastapi import Depends

from src.services.users import UserService
from src.dependencies.cache_service import CacheDep


async def get_user_service(cache: CacheDep) -> UserService:
    return UserService(cache=cache)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]