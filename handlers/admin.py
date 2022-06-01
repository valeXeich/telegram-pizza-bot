from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from db.methods import add_to_base, update_pizza, delete_pizza, get_pizza_list
from create_bot import bot

from .utils import photo, name, ingredients, price, ingredients_validate


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    ingredients = State()
    price = State()


class FSMAdminDelete(StatesGroup):
    name = State()


class FSMAdminUpdate(StatesGroup):
    old_name = State()
    photo = State()
    name = State()
    ingredients = State()
    price = State()


ID = None
# Call admin commands from group
async def open_admin_panel(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Список команд:\n \n/Загрузить\n/Удалить\n/Обновить\n/Отмена')
    await message.delete()

# Load
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузите изображение')

async def load_photo(message: types.Message, state: FSMContext):
    await photo(bot, message, state, 'photo')
    await FSMAdmin.next()
    await message.reply('Введите название')

async def load_name(message: types.Message, state: FSMContext):
    await name(message, state, 'name')
    await FSMAdmin.next()
    await message.reply('Введите ингридиенты через запятую')

async def load_ingredients_invalid(message: types.Message):
    await message.reply('Введите корректно')

async def load_ingredients(message: types.Message, state: FSMContext):
    await ingredients(message, state, 'ingredients')
    await FSMAdmin.next()
    await message.reply('Укажите цену')

async def load_price_invalid(message: types.Message):
    await message.reply('Введите корректно')

async def load_price(message: types.Message, state: FSMContext):
    await price(message, state, 'price')
    await add_to_base(state)
    await message.reply('Пицца успешно добавлена')
    await state.finish()

# Delete
async def delete_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminDelete.name.set()
        await message.reply('Введите название пиццы')

async def delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    result = await delete_pizza(state)
    if result is True:
        await message.reply('Пицца успешно удалена')
        await state.finish()
    else:
        await message.reply('Такой пиццы нету, попробуйте ещё раз')

# Update
async def update_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdminUpdate.old_name.set()
        await message.reply('Напишите название пиццы для обновления')

async def save_name_invalid(message: types.Message):
    await message.reply('Такой пиццы нету, попробуйте ещё раз')

async def save_name(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        data['old_name'] = message.text
    await FSMAdminUpdate.next()
    await message.reply('Загрузите новое изображение')

async def update_photo(message: types.Message, state: FSMContext):
    await photo(bot, message, state, 'new_photo')
    await FSMAdminUpdate.next()
    await message.reply('Введите новое название')

async def update_name(message: types.Message, state: FSMContext):
    await name(message, state, 'new_name')
    await FSMAdminUpdate.next()
    await message.reply('Введите новые ингридиенты через запятую')

async def update_ingredients_invalid(message: types.Message):
    await message.reply('Введите корректно')

async def update_ingredients(message: types.Message, state: FSMContext):
    await ingredients(message, state, 'new_ingredients')
    await FSMAdminUpdate.next()
    await message.reply('Введите новую цену')

async def update_price_invalid(message: types.Message):
    await message.reply('Введите корректно')

async def update_price(message: types.Message, state: FSMContext):
    await price(message, state, 'new_price')
    await update_pizza(state)
    await state.finish()
    await message.reply('Пицца успешно обновлена')

# Cancel FSM
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


def register_handlers_admin(dp: Dispatcher):
    # Create pizza
    dp.register_message_handler(cm_start, commands='Загрузить', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(
        load_ingredients_invalid,
        lambda message: ingredients_validate(message, 'invalid'),
        state=FSMAdmin.ingredients
    )
    dp.register_message_handler(
        load_ingredients,
        lambda message: ingredients_validate(message, 'valid'),
        state=FSMAdmin.ingredients
    )
    dp.register_message_handler(load_price_invalid, lambda message: not message.text.isdigit(), state=FSMAdmin.price)
    dp.register_message_handler(load_price, lambda message: message.text.isdigit(), state=FSMAdmin.price)
    # Delete pizza
    dp.register_message_handler(delete_start, commands='Удалить', state=None)
    dp.register_message_handler(delete, state=FSMAdminDelete.name)
    # Update pizza
    dp.register_message_handler(update_start, commands='Обновить', state=None)
    dp.register_message_handler(
        save_name_invalid,
        lambda message: message.text not in get_pizza_list(),
        state=FSMAdminUpdate.old_name
    )
    dp.register_message_handler(
        save_name,
        lambda message: message.text in get_pizza_list(),
        state=FSMAdminUpdate.old_name
    )
    dp.register_message_handler(update_photo, content_types=['photo'], state=FSMAdminUpdate.photo)
    dp.register_message_handler(update_name, state=FSMAdminUpdate.name)
    dp.register_message_handler(
        update_ingredients_invalid,
        lambda message: ingredients_validate(message, 'invalid'),
        state=FSMAdminUpdate.ingredients
    )
    dp.register_message_handler(
        update_ingredients,
        lambda message: ingredients_validate(message, 'valid'),
        state=FSMAdminUpdate.ingredients
    )
    dp.register_message_handler(
        update_price_invalid,
        lambda message: not message.text.isdigit(),
        state=FSMAdminUpdate.price
    )
    dp.register_message_handler(update_price, lambda message: message.text.isdigit(), state=FSMAdminUpdate.price)
    # Cancel
    dp.register_message_handler(cancel_handler, state='*', commands='Отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state='*')
    # Call admin commands from group
    dp.register_message_handler(open_admin_panel, commands=['admin'], is_chat_admin=True)







