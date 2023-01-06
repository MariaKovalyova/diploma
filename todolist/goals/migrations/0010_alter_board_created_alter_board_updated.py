from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0009_board_created_board_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='board',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления'),
        ),
    ]
