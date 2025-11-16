from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    truth_social_api_key: str
    truth_social_base_url: str
    allowed_origins: str = "*"

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()




        
