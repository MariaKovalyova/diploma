from datetime import datetime
from typing import Optional

from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from todolist.settings import TG_BOT_TOKEN, HOST_URL
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = "Runs telegram bot"
    tg_client = TgClient(TG_BOT_TOKEN)
    offset = 0

    def create_goal(self, msg: Message, tg_user: TgUser) -> None:
        """Создание целей"""
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goal_categories_str: str = '\n'.join(["- " + goal.title for goal in goal_categories])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Выберите категорию:\n{goal_categories_str}",
        )
        is_running: bool = True
        status: int = 0
        category: Optional[GoalCategory] = None

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, "message"):
                    try:
                        if item.message.text == "/cancel":
                            # Отмена операции создания
                            self.tg_client.send_message(
                                chat_id=item.message.chat.id,
                                text="Операция отменена"
                            )
                            is_running = False
                            status = 0
                        elif status == 0 and category is None:
                            # Ввод заголовка для создания и получение категории из бд
                            category = goal_categories.filter(title=item.message.text).first()
                            self.tg_client.send_message(
                                chat_id=msg.chat.id,
                                text=f"Введите пожалуйста заголовок для создания цели"
                            )
                            if category:
                                status = 1
                            else:
                                self.tg_client.send_message(
                                    chat_id=item.message.chat.id,
                                    text=f"Категории с названием {item.message.text} не существует"
                                )
                                is_running = False
                                status = 0
                        elif status == 1:
                            title = item.message.text
                            self.tg_client.send_message(
                                chat_id=item.message.chat.id,
                                text=f'Введите пожалуйста дедлайн цели:\n"{item.message.text}"\n'
                                     f'Формат ввода dd/mm/yyyy'
                            )
                            status = 2
                        elif status == 2:
                            due_date = datetime.strptime(item.message.text, '%d/%m/%Y')
                            status = 3
                            self.tg_client.send_message(
                                chat_id=item.message.chat.id,
                                text=f'Введите пожалуйста описание цели:'
                            )
                        elif status == 3:
                            description = item.message.text
                            goal = Goal.objects.create(
                                category=category,
                                description=description,
                                due_date=due_date,
                                user=tg_user.user,
                                title=title,
                            )
                            self.tg_client.send_message(
                                chat_id=item.message.chat.id,
                                text=f"Цель: {title} успешно создана!"
                            )

                            board_id = category.board.id
                            category_id = category.id
                            goal_id = goal.id
                            self.tg_client.send_message(
                                chat_id=item.message.chat.id,
                                text=f"http://{HOST_URL}/boards/{board_id}/categories/{category_id}/goals?goal={goal_id}"
                            )

                            is_running = False
                            status = 0
                            break

                    except:
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f"Что-то пошло не так\n"
                                 f"Создание отменено"
                        )
                        is_running = False
                        status = 0

    def get_goals(self, msg: Message, tg_user: TgUser) -> None:
        """Бот возвращает список целей"""
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user,
        ).exclude(status=Goal.Status.archived)
        goals_str = '\n'.join(["- " + goal.title for goal in goals])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Список ваших целей:\n{goals_str}",
        )

    def get_help(self, msg: Message) -> None:
        """Бот отправляет сообщение о списке команд"""
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f"Список команд:\n"
                 f"/goals # показывает список ваших целей\n"
                 f"/create # создает новую цель"
        )

    def handle_message(self, msg: Message) -> None:
        """Перехват сообщений с целью использования команд"""
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.msg_from.id,
            tg_chat_id=msg.chat.id,
        )
        if tg_user.user is None:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Подтвердите пожалуйста свой аккаунт.\n"
                     f"Для этого необходимо ввести код на сайте\n"
                     f"код: {tg_user.verification_code}"
            )
        elif msg.text == "/goals":
            self.get_goals(msg, tg_user)
        elif msg.text == "/create":
            self.create_goal(msg, tg_user)

        elif msg.text == "/help":
            self.get_help(msg)
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f"Неизвестная команда\n"
                     f"Список команд /help"
            )

    def handle(self, *args, **options) -> None:
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)
