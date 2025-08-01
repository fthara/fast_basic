import pytest
from fastapi.testclient import TestClient

from fast_basic.app import app


@pytest.fixture
def client():
    return TestClient(app)
