import json
from dataclasses import asdict
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from agregates import get_agregated, AgregateResultDTO
from db import get_db
from config import Config
from enums import GroupTypeEnum
from messages import MESSAGE_REQUEST_EXAMPLE, MESSAGE_AVAIBLE_FORMATS


bot = Bot(token=Config.BOT_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(f"Hi! @{message.from_user.first_name}")


async def parse_message(message: types.Message):
    """Parse and validate message format"""
    try:
        dict_message = json.loads(message.text)
    except json.decoder.JSONDecodeError:
        await message.answer(MESSAGE_REQUEST_EXAMPLE)
    else:
        keys = ["dt_from", "dt_upto", "group_type"]
        if list(dict_message.keys()) != keys:
            await message.answer(MESSAGE_AVAIBLE_FORMATS)
            return
        if not GroupTypeEnum.contain(dict_message["group_type"]):
            await message.answer(MESSAGE_AVAIBLE_FORMATS)
            return

        dict_message["group_type"] = GroupTypeEnum(dict_message["group_type"])
        dict_message["dt_from"] = datetime.fromisoformat(dict_message["dt_from"])
        dict_message["dt_upto"] = datetime.fromisoformat(dict_message["dt_upto"])
        return dict_message


@dp.message_handler(content_types=types.ContentTypes.ANY)
async def send_aggregation(message: types.Message):
    """
    This handler will be called for any message and if message has correct format will execute request to mongodb
    """
    dict_message = await parse_message(message)
    if dict_message:
        client = get_db()
        collection = client[Config.MONGO_DATABASE].sample_collection
        agregated: AgregateResultDTO = await get_agregated(collection, **dict_message)
        result = json.dumps(asdict(agregated))
        if len(result) > 4096:
            for x in range(0, len(result), 4096):
                await message.answer(result[x:x + 4096])
        else:
            await message.answer(result)


