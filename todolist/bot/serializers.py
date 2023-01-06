from rest_framework import serializers

from todolist.bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ('verification_code',)
