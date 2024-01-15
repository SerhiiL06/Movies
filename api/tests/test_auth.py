import asyncio

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main.web import app

client = TestClient(app=app)


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def test_register():
    response = client.post(
        "http://127.0.0.1:8000/users/register",
        json={
            "email": "test@example.com",
            "password1": "string",
            "password2": "string",
        },
    )

    response.status_code == 200


def test_login():
    response = client.post(
        "http://127.0.0.1:8000/users/token",
        data={
            "username": "sergiy06061997@gmail.com",
            "password": "string",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    assert response.status_code == 200


@pytest.mark.anyio
def test_me():
    client.post(
        "http://127.0.0.1:8000/users/token",
        data={
            "username": "sergiy06061997@gmail.com",
            "password": "string",
        },
        headers={"content-type": "application/x-www-form-urlencoded"},
    )

    response = client.get("http://127.0.0.1:8000/users/me")

    assert response.status_code == 200
