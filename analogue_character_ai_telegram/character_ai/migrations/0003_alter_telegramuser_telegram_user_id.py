# Generated by Django 4.2.2 on 2023-07-05 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('character_ai', '0002_alter_telegramuser_telegram_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='telegram_user_id',
            field=models.PositiveIntegerField(null=True, unique=True),
        ),
    ]
