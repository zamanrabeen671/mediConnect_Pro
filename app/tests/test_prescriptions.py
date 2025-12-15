"""
Tests for prescription operations
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_list_prescriptions():
    """Test listing prescriptions"""
    response = client.get("/prescriptions/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_prescription():
    """Test getting a prescription by ID"""
    response = client.get("/prescriptions/1")
    # Will return 404 if prescription doesn't exist
    assert response.status_code in [200, 404]
