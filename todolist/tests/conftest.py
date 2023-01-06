from datetime import datetime

import pytest

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tests import factories

USER_MODEL = get_user_model()


@pytest.fixture
def auth_client(test_user):
    client = APIClient()
    client.force_login(test_user)
    return client


@pytest.fixture
def test_user(db):
    user = USER_MODEL.objects.create(
        username='stone',
        password='test1234',
        email='12345@mail.ru',
    )
    return user


@pytest.fixture
def category(board, test_user):
    return factories.GoalCategoryFactory.create(
        board=board,
        user=test_user
    )


@pytest.fixture
def date_now():
    return str(datetime.now().date())


@pytest.fixture
def board(test_user):
    return factories.BoardFactory.create()


@pytest.fixture
def board_participant(test_user, board):
    return factories.BoardParticipantFactory.create(
        board=board,
        user=test_user,
        role=1,
    )


@pytest.fixture
def goal(category, date_now, test_user):
    return factories.GoalFactory.create(
        category=category,
        description="super goal",
        due_date=date_now,
        user=test_user,
    )


@pytest.fixture
def goal_comment(goal, test_user):
    return factories.GoalCommentFactory.create(
        goal=goal,
        user=test_user,
    )
