"""
Tests for appointment operations
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_appointments():
    """Test listing appointments"""
    response = client.get("/appointments/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_appointment():
    """Test getting an appointment by ID"""
    response = client.get("/appointments/1")
    # Will return 404 if appointment doesn't exist
    assert response.status_code in [200, 404]
