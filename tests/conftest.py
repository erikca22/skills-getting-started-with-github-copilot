import copy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

import src.app as app_module

_BASE_ACTIVITIES = copy.deepcopy(app_module.activities)


def _activity_segment(activity_name: str) -> str:
    return quote(activity_name, safe="")


@pytest.fixture
def activity_segment():
    return _activity_segment


@pytest.fixture(autouse=True)
def reset_activities() -> None:
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_BASE_ACTIVITIES))
    yield
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_BASE_ACTIVITIES))


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_module.app)
