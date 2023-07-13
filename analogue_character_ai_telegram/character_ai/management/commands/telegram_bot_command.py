import os
import openai
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import WebAppInfo
from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from character_ai.models import TelegramUser, Character
from character_ai.amplitude_client import AmplitudeClient

load_dotenv(dotenv_path='.env')
DATETIME_FORMAT = '%H:%M:%S.%f'

openai.api_key = os.getenv('OPENAI_KEY')


@sync_to_async
def save_telegram_user(telegram_id, name, surname, username, time):
    telegram_user, created = TelegramUser.objects.get_or_create(
        telegram_user_id=telegram_id,
        defaults={
            'name': name,
            'surname': surname,
            'username': username,
            'time': time,
        }
    )
    print(f"User is Created:f'{telegram_user}")

    if not created:
        # If the user is not newly created (created is False), we update the user's information (name, surname, username, time) and save the changes.
        telegram_user.name = name
        telegram_user.surname = surname
        telegram_user.username = username
        telegram_user.time = time
        telegram_user.save()
        print("User info updated:", telegram_user)


def keyboard_markup(tgId):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(types.KeyboardButton('/menu',
                                    web_app=WebAppInfo(
                                        url=f"https://5111-185-177-104-185.ngrok-free.app/test?tgId={tgId}")))
    return markup


@sync_to_async
def save_user_message(tgId, text):
    """
    Сохраняем сообщение который отправили бота

    """
    TelegramUser.objects.filter(telegram_user_id=tgId).update(telegram_message=text)


@sync_to_async
def get_chosen_personage_name(tgId):
    """Получаем уже выбранного персонажа"""
    telegram_user = TelegramUser.objects.get(telegram_user_id=tgId)
    personage = telegram_user.personage_id.personage_name
    return personage
@sync_to_async
def get_chosen_personage_id(tgId):
    """Получаем уже выбранного персонажа"""
    telegram_user = TelegramUser.objects.get(telegram_user_id=tgId)
    personage_id = telegram_user.personage_id
    return personage_id


start_time = datetime.now()


class Command(BaseCommand):
    amplitude_client = AmplitudeClient()

    def handle(self, *args, **options):
        bot = Bot(os.getenv('TOKEN_API'))
        dp = Dispatcher(bot)
        dp.middleware.setup(LoggingMiddleware())

        @csrf_exempt
        @dp.message_handler(commands=['start'])
        async def send_welcome(message: types.Message):
            current_time = datetime.now()
            telegram_id = message.from_user.id
            name = message.from_user.first_name
            surname = message.from_user.last_name
            username = message.from_user.username
            dt = current_time - start_time

            time = datetime.strptime(str(dt), DATETIME_FORMAT)

            await save_telegram_user(telegram_id, name, surname, username, time)

            self.amplitude_client.registered(tgId=telegram_id)

            await message.answer("Hi!\nI'm Bot!\nWhere you can choose character.",
                                 reply_markup=keyboard_markup(tgId=telegram_id))
            await message.delete()

        @dp.message_handler()
        async def handle_message(message: types.Message):
            # Получите данные о пользователе и чате
            telegram_id = message.from_user.id
            print(telegram_id)
            text = message.text
            print(text)
            await save_user_message(tgId=telegram_id, text=text)
            character = await get_chosen_personage_name(tgId=telegram_id)
            character_id = await get_chosen_personage_id(tgId=telegram_id)
            self.amplitude_client.character_selected(character_id=character_id)

            if character == 'Mario':
                role = 'Mario from Super Mario'
            else:
                role = f'{character} Einstein'

            messages = [
                {"role": "system", "content": f"You are {role}. Do not give dangerous information."},
                {"role": "user",
                 "content": f"I am a user who wants to know all about {character}" if character == 'Mario'
                 else f"I am a user who wants to speak with {character}"},
                {"role": "assistant",
                 "content": "Greetings! What would you like to know?" if character == 'Mario'
                 else "Great! What would you like to talk about?"}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            await message.answer(response['choices'][0]['message']['content'])

        executor.start_polling(dp, skip_updates=True)
