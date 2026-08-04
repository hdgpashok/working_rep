import os

from pydantic import PostgresDsn, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    postgres_url: PostgresDsn = Field(env='postgres_url')

    REDIS_HOST: str = Field(env='REDIS_HOST')
    REDIS_PORT: int = Field(env='REDIS_PORT')
    REDIS_DB: int = Field(env='REDIS_DB')

    KAFKA_HOST: str = Field(env="KAFKA_HOST")
    KAFKA_PORT: int = Field(env="KAFKA_PORT")
    KAFKA_TOPIC: str = Field(env="KAFKA_TOPIC")

    KAFKA_DQL_TOPIC: str = Field(env="KAFKA_DLQ_TOPIC")

    MAX_RETRIES: int = Field(env='MAX_RETRIES')

    class Config:
        env_file = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', '..', '.env')
        )


settings = Settings()