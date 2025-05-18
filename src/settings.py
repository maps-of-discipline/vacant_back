from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 10
    max_overflow: int = 10
    autoflush: bool = False
    autocommit: bool = False
    expire_on_commit: bool = False


class RunSettigns(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiSettings(BaseModel):
    prefix: str = "/api"
    allowed_origins: list[str] = [
        "http://localhost:7000",
    ]


class AdminApiSettings(BaseModel):
    base_url: str
    service_title: str


class FileStorageSettings(BaseModel):
    base_dir: str


class EmailCreadentials(BaseModel):
    host: str
    port: int
    sender: str
    password: str


class NotificationsSettings(BaseModel):
    email: EmailCreadentials


class AuthSettings(BaseModel):
    secret: str
    algorithm: str = "HS256"


class GRPCSettings(BaseModel):
    host: str
    port: int

    @property
    def url(self) -> str:
        return f"{self.host}:{self.port}"


class LoggingSettings(BaseModel):
    level: str = "DEBUG"
    log_file: str = "logs/app.log"
    use_file_handler: bool = False


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__")

    db: DBSettings
    run: RunSettigns
    api: ApiSettings
    admin_api: AdminApiSettings
    auth: AuthSettings
    logging: LoggingSettings
    grpc: GRPCSettings
    file_storage: FileStorageSettings
    notifications: NotificationsSettings
    maps_base_url: str


settings: Settings = Settings(_env_file=".env")

if __name__ == "__main__":
    print(settings.model_dump())
