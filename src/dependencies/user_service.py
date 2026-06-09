from typing import Annotated

from fastapi import Depends

from src.dependencies.repository import RepositoryDep
from src.services.users import UserService
from src.dependencies.cache_service import CacheDep


async def get_user_service(cache: CacheDep, repo: RepositoryDep) -> UserService:
    return UserService(cache=cache, repo=repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]