import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_retrieve_goal_category(auth_client, goal_comment, date_now, category, board_participant):
    url = reverse('retrieve_goal_comment', kwargs={'pk': goal_comment.pk})
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_goal_category(auth_client, goal_comment, date_now, category, board_participant, goal, test_user):
    url = reverse('retrieve_goal_comment', kwargs={'pk': goal_comment.pk})
    payload = {
        'goal': goal.pk,
        'text': 'super text',
        'user': test_user,
    }
    response = auth_client.patch(
        path=url,
        data=payload,
    )

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_goal_category(auth_client, goal_comment, date_now, category, board_participant):
    url = reverse('list_goal_comment')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_goal_category(auth_client, goal, test_user):
    url = reverse('create_goal_comment')
    payload = {
        'goal': goal.pk,
        'text': 'super text',
        'user': test_user,
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['goal'] == payload['goal']
    assert response_data['text'] == payload['text']
