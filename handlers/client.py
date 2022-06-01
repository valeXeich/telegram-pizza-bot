from aiogram import types, Dispatcher

from keyboards import kb_client
from create_bot import bot
from db import s, Pizza

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)

async def pizza_open_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'вторник 09:00–23:00\n'
        'среда	09:00–23:00\n'
        'четверг 09:00–23:00\n'
        'пятница 09:00–23:00\n'
        'суббота 09:00–23:00\n'
        'воскресенье 09:00–23:00\n'
        'понедельник 09:00–23:00\n'
    )

async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'ул.Франко')

async def pizza_menu(message: types.Message):
    pizza_all = s.query(Pizza).all()
    print(await bot.get_chat_member(message.chat.id, message.from_user.id))
    for pizza in pizza_all:
        with open(pizza.photo, 'rb') as photo:
            await bot.send_photo(
                message.from_user.id,
                photo,
                f'Название: {pizza.name}\nЦена: {pizza.price}\nИнгредиенты: {str(pizza.ingredients).strip("[]")}'
            )


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(pizza_open_command, commands=['Режим_работы'])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu, commands=['Меню'])

