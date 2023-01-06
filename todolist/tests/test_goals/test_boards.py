import pytest
from django.urls import reverse
from rest_framework import status

from goals.models import Board


@pytest.mark.django_db
def test_retrieve_board(auth_client, goal, date_now, category, board_participant):
    url = reverse('retrieve_board', kwargs={'pk': goal.pk})
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_list_board(auth_client, goal, date_now, category, board_participant):
    url = reverse('list_board')
    response = auth_client.get(path=url)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_create_board(auth_client, board, test_user):
    url = reverse('create_board')
    payload = {
        'title': 'super title',
    }
    response = auth_client.post(
        path=url,
        data=payload
    )
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data['title'] == payload['title']


@pytest.mark.django_db
def test_create_board_db():
    board, created = Board.objects.get_or_create(
        title="gfdgdfgdf",
    )

    assert type(board) == type(Board())
