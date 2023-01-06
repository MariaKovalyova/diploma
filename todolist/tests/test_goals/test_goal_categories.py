import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_retrieve_goal_category(auth_client, goal, date_now, category, board_participant):
    url = reverse('retrieve_goal_category', kwargs={'pk': goal.pk})
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_goal_category(auth_client, goal, date_now, category, board_participant, board, test_user):
    url = reverse('retrieve_goal_category', kwargs={'pk': goal.pk})
    payload = {
        'board': board.pk,
        'title': 'super title',
        'user': test_user,
    }
    response = auth_client.patch(
        path=url,
        data=payload
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_goal_category(auth_client, goal, date_now, category, board_participant):
    url = reverse('list_goal_category')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_goal_category(auth_client, board, test_user):
    url = reverse('create_goal_category')
    payload = {
        'board': board.pk,
        'title': 'super title',
        'user': test_user,
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['board'] == payload['board']
    assert response_data['title'] == payload['title']
