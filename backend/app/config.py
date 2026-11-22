from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    FRONTEND_PORT: int
    SERVICE_VERSION: str


settings = Settings()