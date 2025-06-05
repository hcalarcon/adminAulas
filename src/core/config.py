# Archivo donde definimos datos importantes de nuestro sistema


from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "prueba"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str
    SECRET_KEY: str
    API_KEY: str
    ALGORITHM: str = "HS256"
    RATE_LIMIT: str = "30/minute"

    class Config:
        env_file = ".env"


settings = Settings()
