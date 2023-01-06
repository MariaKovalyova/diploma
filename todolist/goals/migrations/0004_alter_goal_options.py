from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_alter_goal_priority_alter_goal_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goal',
            options={'verbose_name': 'Цель', 'verbose_name_plural': 'Цели'},
        ),
    ]
