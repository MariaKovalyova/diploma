from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient
from todolist.settings import TG_BOT_TOKEN


class BotVerifyView(generics.UpdateAPIView):
    """Вьюшка для связи бота с пользователем"""
    model = TgUser
    permission_classes = [IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = TgUserSerializer

    def patch(self, request, *args, **kwargs):
        data = self.serializer_class(request.data).data
        tg_client = TgClient(TG_BOT_TOKEN)
        tg_user = TgUser.objects.filter(verification_code=data['verification_code']).first()
        if not tg_user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tg_user.user = request.user
        tg_user.user_verificated = True
        tg_user.save()
        tg_client.send_message(chat_id=tg_user.tg_chat_id, text='Аккаунт успешно связан!')
        return Response(data=data, status=status.HTTP_201_CREATED)
