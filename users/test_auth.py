import pytest
from django.contrib.auth.models import User

REGISTER_URL = "/api/auth/register/"
LOGIN_URL = "/api/auth/login/"
ME_URL = "/api/auth/me/"

NEW_USER = {
    "username": "anna",
    "email": "anna@example.com",
    "password": "StrongPass123",
}


@pytest.mark.django_db
def test_register_creates_user(api_client):
    response = api_client.post(REGISTER_URL, NEW_USER, format="json")
    assert response.status_code == 201
    assert User.objects.filter(username="anna").exists()
    assert "password" not in response.data


@pytest.mark.django_db
def test_register_stores_hashed_password(api_client):
    api_client.post(REGISTER_URL, NEW_USER, format="json")
    assert User.objects.get(username="anna").password != NEW_USER["password"]


@pytest.mark.django_db
def test_register_without_password_fails(api_client):
    data = {"username": "anna", "email": "anna@example.com"}
    response = api_client.post(REGISTER_URL, data, format="json")
    assert response.status_code == 400


def test_login_returns_tokens(api_client, user):
    response = api_client.post(
        LOGIN_URL,
        {"username": "george", "password": "StrongPass123"},
        format="json",
    )
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


def test_login_with_wrong_password_fails(api_client, user):
    response = api_client.post(
        LOGIN_URL,
        {"username": "george", "password": "wrong"},
        format="json",
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_me_without_token_is_unauthorized(api_client):
    response = api_client.get(ME_URL)
    assert response.status_code == 401


def test_me_with_token_returns_user(api_client, user):
    login = api_client.post(
        LOGIN_URL,
        {"username": "george", "password": "StrongPass123"},
        format="json",
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
    response = api_client.get(ME_URL)
    assert response.status_code == 200
    assert response.data["username"] == "george"
    assert response.data["is_staff"] is False
