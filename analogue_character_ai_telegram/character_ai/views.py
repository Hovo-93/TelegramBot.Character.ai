import json
import os

from aiogram import Bot, Dispatcher
from django.shortcuts import render
from character_ai.models import *

import asyncio

from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')


def character_view(request):
    characters = Character.objects.all()
    telegram_user_id = TelegramUser.objects.first()
    context = {
        'characters': characters,
        'user_id': telegram_user_id
    }
    return render(request, 'index.html', context)


bot = Bot(token=os.getenv('TOKEN_API'))
dp = Dispatcher(bot)


async def send_message_to_user(user_id: int, text: str) -> None:
    try:
        await bot.send_message(chat_id=user_id, text=text)
    except Exception as e:
        print(f"Failed to send message to user {user_id}: {str(e)}")


def choose_character(request):
    if request.method == "POST":
        data = json.loads(request.body)
        perosange_id = data.get('id')
        user_id = data.get('telegram_id')
        character = Character.objects.get(id=perosange_id)
        TelegramUser.objects.filter(telegram_user_id=user_id).update(personage_id=character)
        message = f" {character.welcome_message}!"
        asyncio.run((send_message_to_user)(user_id, message))

    return render(request, "index.html")
