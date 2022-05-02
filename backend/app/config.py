import logging
import os
import pathlib
from functools import lru_cache

import app
from pydantic import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    """Main settings"""

    environment: str = os.getenv("ENVIRONMENT", "dev")
    testing: bool = os.getenv("TESTING", 0)
    uploads_folder: str = str(pathlib.Path(app.__file__).parent / "uploads")
    secret: str = os.getenv("MYSECRET", "secret")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> BaseSettings:
    """Retrieves the settings
    Returns:
        BaseSettings: the fastapi settings
    """
    log.info("----Loading config settings from the environment----")
    return Settings()
