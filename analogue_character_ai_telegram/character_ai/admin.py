from django.contrib import admin
from character_ai.models import TelegramUser, Character

# Register your models here.
admin.site.register(TelegramUser)

admin.site.register(Character)
