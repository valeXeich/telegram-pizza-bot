async def photo(bot, message, state, string):
    async with state.proxy() as data:
        photo_info = await bot.get_file(message.photo[-1].file_id)
        file_path = photo_info.file_path
        photo_obj = await bot.download_file(file_path, 'media/' + file_path.split('photos/')[1])
        data[string] = photo_obj.name

async def name(message, state, string):
    async with state.proxy() as data:
        data[string] = message.text

async def ingredients(message, state, string):
    async with state.proxy() as data:
        data[string] = message.text.split(',')

async def price(message, state, string):
    async with state.proxy() as data:
        data[string] = int(message.text)

def ingredients_validate(message, status):
    if status == 'invalid':
        return message.text.count(',') + 1 != len(message.text.split(' '))
    else:
        return message.text.count(',') + 1 == len(message.text.split(' '))

