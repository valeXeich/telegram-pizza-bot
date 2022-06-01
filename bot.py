from aiogram.utils import executor

from handlers import client, admin
from create_bot import dp


async def on_startup(_):
    print('Bot online')

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

