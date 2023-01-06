import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_signup(auth_client):
    url = reverse('signup')
    payload = {
        'password': 'Super12345',
        'password_repeat': 'Super12345',
        'username': 'MrDavid',
    }
    response = auth_client.post(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_update_password(auth_client, test_user):
    url = reverse('update_password')
    payload = {
        'new_password_repeat': 'test1234',
        'new_password': 'test1234',
        'old_password': 'test1234',
        'user': test_user,
    }
    response = auth_client.patch(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_profile(auth_client):
    url = reverse('profile')

    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_login(auth_client, test_user):
    client = APIClient()
    client.force_login(test_user)

    assert not (client is None)
