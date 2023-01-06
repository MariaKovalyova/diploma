from django.db import migrations, transaction, models
from django.utils import timezone


def create_objects(apps, schema_editor):

    User = apps.get_model("core", "User")
    Board = apps.get_model("goals", "Board")
    BoardParticipant = apps.get_model("goals", "BoardParticipant")
    GoalCategory = apps.get_model("goals", "GoalCategory")

    with transaction.atomic():
        for user in User.objects.all():
            new_board = Board.objects.create(
                title="Мои цели",
                created=timezone.now(),
                updated=timezone.now()
            )
            BoardParticipant.objects.create(
                user=user,
                board=new_board,
                role=1,
                created=timezone.now(),
                updated=timezone.now()
            )

            GoalCategory.objects.filter(user=user).update(board=new_board)

class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_board_goalcategory_board_boardparticipant'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='board',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.AddField(
            model_name='boardparticipant',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='boardparticipant',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
        migrations.RunPython(create_objects)
    ]
