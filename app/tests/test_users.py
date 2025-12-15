"""
Tests for user operations
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.database import get_db
from app.schemas import UserCreate


client = TestClient(app)


def test_register_user():
    """Test user registration"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "role": "patient"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]


def test_login_user():
    """Test user login"""
    # First register a user
    user_data = {
        "email": "login_test@example.com",
        "password": "testpassword123",
        "role": "patient"
    }
    client.post("/auth/register", json=user_data)
    
    # Then login
    response = client.post(
        "/auth/login",
        params={
            "email": user_data["email"],
            "password": user_data["password"]
        }
    )
    assert response.status_code == 200
    assert "token" in response.json()


def test_get_current_user():
    """Test getting current user info"""
    response = client.get("/users/me")
    # Will return 401 since not authenticated
    assert response.status_code == 401
