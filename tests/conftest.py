from typing import Generator, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.public import api as public_api


def start_application():
    app = FastAPI()
    app.include_router(public_api)
    return app


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a fresh database on each test case.
    """
    _app = start_application()
    yield _app


@pytest.fixture(scope="function")
def client(
        app: FastAPI
) -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client
