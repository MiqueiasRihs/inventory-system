from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "SolFácil - Inventário"

    class Config:
        env_file = ".env"

settings = Settings()