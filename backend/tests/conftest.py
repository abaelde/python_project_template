import pathlib

import pytest
from app.config import Settings, get_settings
from app.main import create_application
from fastapi.testclient import TestClient
from pydantic.env_settings import BaseSettings

uploads_test_folder = str(pathlib.Path(__file__).parent / "uploads_test")


def get_settings_override() -> BaseSettings:
    """Overrides the settings for testing

    Returns:
        BaseSettings: fastapi testing settings
    """

    return Settings(
        testing=1,
        environment="dev",
        uploads_folder=uploads_test_folder,
    )


@pytest.fixture(scope="module")
def test_app():
    """yields the test_app to use in all the tests

    Yields:
        the test app
    """
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:

        # testing
        yield test_client

    # tear down
    for child in pathlib.Path(uploads_test_folder).glob("*"):
        if child.name != ".gitignore":
            child.unlink()
