import os
from functools import lru_cache
from os.path import abspath, dirname

from dotenv import load_dotenv
from pydantic import BaseSettings

BASE_DIR = dirname(dirname(abspath(__file__)))


class Settings(BaseSettings):
    mysql_db_name: str
    mysql_password: str
    mysql_port: int
    mysql_host: str
    mysql_user: str
    port: int = 8000
    host: str = "127.0.0.1"

    class Config:
        env_file = os.path.join(BASE_DIR, "defaults.env")
        env_prefix = "app_"
        load_dotenv(
            dotenv_path=os.path.join(BASE_DIR, "local.env"), override=True, verbose=True,
            interpolate=True
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@lru_cache()
def build_sqlalchemy_database_uri() -> str:
    db_url = (
        f"mysql+aiomysql://{settings.mysql_user}:{settings.mysql_password}"
        f"@{settings.mysql_host}:{settings.mysql_port}/{settings.mysql_db_name}"
    )
    return db_url
