import pytest

from bot.models import TgUser


@pytest.mark.django_db
def test_generate_verification_code():
    tg_user, created = TgUser.objects.get_or_create(
        tg_user_id=1,
        tg_chat_id=1,
    )

    code = tg_user.generate_verification_code()

    assert len(code) == 10
    assert type(code) == str
