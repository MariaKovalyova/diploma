from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0002_goal_alter_goalcategory_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Низкий'), (2, 'Средний'), (3, 'Высокий'), (4, 'Критический')], default=2, verbose_name='Приоритет'),
        ),
        migrations.AlterField(
            model_name='goal',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'К выполнению'), (2, 'В процессе'), (3, 'Выполнено'), (4, 'Архив')], default=1, verbose_name='Статус'),
        ),
    ]
