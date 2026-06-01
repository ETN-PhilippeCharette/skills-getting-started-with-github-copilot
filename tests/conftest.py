import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture: TestClient for making requests to the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture: Reset activities to known state before each test.
    Yields control to the test, then restores original state after.
    """
    original_activities = {
        name: {
            "description": details["description"],
            "schedule": details["schedule"],
            "max_participants": details["max_participants"],
            "participants": details["participants"].copy()
        }
        for name, details in activities.items()
    }
    
    yield
    
    # Restore original state
    activities.clear()
    activities.update(original_activities)
