from typing import Annotated

from fastapi import Depends

from src.repository.user import UserRepository


async def get_repo():
    return UserRepository


RepositoryDep = Annotated[UserRepository, Depends(get_repo)]


