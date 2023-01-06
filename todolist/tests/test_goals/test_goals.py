import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_retrieve_goal(auth_client, goal, date_now, category, board_participant):
    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_goal(auth_client, goal, date_now, category, board_participant, test_user):
    url = reverse('retrieve_goal', kwargs={'pk': goal.pk})
    payload = {
        'title': 'New Goal',
        'category': category.pk,
        'description': 'This is a nice goal to have',
        'due_date': date_now,
        'user': test_user,
    }
    response = auth_client.patch(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_goal(auth_client, goal, date_now, category, board_participant):
    url = reverse('list_goal')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_goal(auth_client, test_user, category, date_now):
    url = reverse('create_goal')
    payload = {
        'title': 'New Goal',
        'category': category.pk,
        'description': 'This is a nice goal to have',
        'due_date': date_now,
        'user': test_user,
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']
    assert response_data['category'] == payload['category']
    assert response_data['description'] == payload['description']
    assert response_data['due_date'] == payload['due_date']
