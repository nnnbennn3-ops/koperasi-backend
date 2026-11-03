from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    db_driver: str = Field("ODBC Driver 17 for SQL Server", alias="DB_DRIVER")
    db_server: str = Field("localhost", alias="DB_SERVER")
    db_port: str = Field("1433", alias="DB_PORT")
    db_name: str = Field("koperasi_karyawan", alias="DB_NAME")
    db_user: str = Field("user_koperasi", alias="DB_USER")
    db_password: str = Field("KoperasiPassword123!", alias="DB_PASSWORD")

    # User Service URL
    user_service_url: str = Field(
        "https://testing-backendims.indomobil.co.id/user-service",
        alias="USER_SERVICE_URL",
    )


settings = Settings()
