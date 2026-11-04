from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Database Configuration
    db_driver: str = Field(..., alias="DB_DRIVER")
    db_server: str = Field(..., alias="DB_SERVER")
    db_port: str = Field(..., alias="DB_PORT")
    db_name: str = Field(..., alias="DB_NAME")
    db_user: str = Field(..., alias="DB_USER")
    db_password: str = Field(..., alias="DB_PASSWORD")

    user_service_url: str = Field(..., alias="USER_SERVICE_URL")
    finance_service_url: str = Field(..., alias="FINANCE_SERVICE_URL")
    general_service_url: str = Field(..., alias="GENERAL_SERVICE_URL")


settings = Settings()
