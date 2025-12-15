"""
Tests for doctor operations
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_doctors():
    """Test listing doctors"""
    response = client.get("/doctors/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_doctor():
    """Test getting a doctor by ID"""
    response = client.get("/doctors/1")
    # Will return 404 if doctor doesn't exist
    assert response.status_code in [200, 404]
