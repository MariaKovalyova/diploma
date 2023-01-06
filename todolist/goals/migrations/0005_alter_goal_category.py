from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0004_alter_goal_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goals.goalcategory', verbose_name='Категория'),
        ),
    ]
