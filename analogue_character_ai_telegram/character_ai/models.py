from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    surname = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Character(models.Model):
    personage_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='photos/')

    def __str__(self):
        return self.personage_name

