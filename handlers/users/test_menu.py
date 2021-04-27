from aiogram.types import (Message, InlineKeyboardMarkup, InlineKeyboardButton,
                           CallbackQuery)

from database.database import DBCommands
from loader import dp

d_con = DBCommands()


@dp.message_handler(commands=['start'])
async def start(message: Message):
    user = message.from_user
    user_data = {
        "uniq_user_id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
    }
    profile = await d_con.create_profile(user_data)
    text = "Добрый день, {name}!\n\n" \
           "Я могу помочь вам поработать с нашей системой\n" \
           "Чтобы начать работу, напишите: /menu".format(name=profile)
    await message.answer(text)


@dp.message_handler(commands=['menu'])
async def start(message: Message):
    menu = await get_menu()

    await message.answer(text=menu.get('text'), reply_markup=menu.get('reply_markup'))


async def get_menu():
    choice = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Изменить свои данные", callback_data='change_profile')
        ],
        [
            InlineKeyboardButton(text="Связь с оператором", callback_data='connection_with_operator')
        ],
        [
            InlineKeyboardButton(text="Приостановить доставку", callback_data='make_pause')
        ]
    ])

    return {'text': 'Что вы можете сделать в боте: ', 'reply_markup': choice}


@dp.callback_query_handler(text_contains="change_profile")
async def profile_settings(call: CallbackQuery):
    await call.answer(cache_time=60)
    name = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Личные данные (ФИО, телефон, адресс)", callback_data='personal_detail')],
        [InlineKeyboardButton(text="Пакет (Размер, содержание)", callback_data='package')],
        [InlineKeyboardButton(text="Доставка", callback_data='delivery')],
        [InlineKeyboardButton(text="Отменить", callback_data='cancel')],
    ]
    )

    await call.message.answer("Выберите раздел настройки", reply_markup=name)


@dp.callback_query_handler(text_contains=['personal_detail'])
async def personal_detail(call: CallbackQuery):
    choice = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ФИО", callback_data='name_surname')],
        [InlineKeyboardButton(text="Телефон +38(000)-00-00-000", callback_data='phone_number')],
        [InlineKeyboardButton(text="Адресс", callback_data='address')],
        [InlineKeyboardButton(text="Отмена", callback_data='cancel')]
    ])

    await call.message.answer(text='Выберите раздел настройки ваших данных', reply_markup=choice)


@dp.callback_query_handler(text_contains=['name_surname'])
async def name_surname(call: CallbackQuery):
    await call.message.answer('Введите ваше имя: ')


@dp.callback_query_handler(text_contains="cancel")
async def approval(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Вы отменили изменения данных")


@dp.message_handler()
async def echo(message: Message):
    menu = await get_menu()

    await message.answer(text=menu.get('text'), reply_markup=menu.get('reply_markup'))
