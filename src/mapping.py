import uuid

from src.schemas.users import UserCreate, UserUpdate, UserExternal
from src.models.users import UserModel
from src.models.profiles import ProfileModel


class DataMapping:
    @staticmethod
    def map_create_data(user: UserCreate):
        new_profile = ProfileModel(
            **user.profile.model_dump()
        )
        return UserModel(
            id=uuid.uuid4(),
            title=user.title,

            profile=new_profile
        )

    @staticmethod
    def map_update_user(user: UserModel, updated_user: UserUpdate):
        data = updated_user.model_dump(exclude={'profile'})
        for key, value in data.items():
            setattr(user, key, value)

        profile_data = updated_user.profile.model_dump()
        for key, value in profile_data.items():
            setattr(user.profile, key, value)

    @staticmethod
    def map_external_user(user: UserExternal):
        new_profile = ProfileModel(**user.profile.model_dump())

        new_user = UserModel(profile=new_profile)
        user_data = user.model_dump(exclude={'profile'})

        for key, value in user_data.items():
            setattr(new_user, key, value)

        return new_user

