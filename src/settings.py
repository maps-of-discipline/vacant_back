from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv(".env")


class DBSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10
    autoflush: bool = False
    autocommit: bool = False
    flush_on_commit: bool = False


class RunSettigns(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiSettings(BaseModel):
    prefix: str = "/api"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DBSettings
    run: RunSettigns
    api: ApiSettings


import os

print(os.environ["DB__URL"])
settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
