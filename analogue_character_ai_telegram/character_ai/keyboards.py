from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton
from aiogram.types.web_app_info import WebAppInfo

from character_ai.models import Character

MENU_BOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='/menu')]
    ]
    ,
    resize_keyboard=True
)

ikb = InlineKeyboardMarkup(row_width=2)
characters = Character.objects.all()
for character in characters:
    button = types.InlineKeyboardButton(text=character.personage_name, callback_data=f"select_character_{character.id}")
    ikb.add(button)


# markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# markup.add(types.KeyboardButton('/menu', web_app=WebAppInfo(url="https://9a91-45-15-150-246.ngrok-free.app/test?tgid=xxx")))
