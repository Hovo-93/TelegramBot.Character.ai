from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class TelegramUser(AbstractUser):
    telegram_user_id = models.PositiveIntegerField(unique=True, null=True)
    surname = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    personage_id = models.ForeignKey('Character', on_delete=models.PROTECT,null=True)
    telegram_message = models.TextField()

    def __str__(self):
        return self.username


class Character(models.Model):
    personage_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')
    welcome_message = models.TextField()

    def __str__(self):
        return self.personage_name
