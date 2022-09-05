from pathlib import Path

import pytest
from mechanic.api.launch import setup_app

TEST_CONFIG_TWIN = Path("tests") / "test_config.json"


@pytest.fixture
def app():
    """Create and configure app instance for tests."""
    app = setup_app(config_path=TEST_CONFIG_TWIN)
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def client(app):
    return app.test_client()
