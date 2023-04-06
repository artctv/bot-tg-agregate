import asyncio
from datetime import datetime
from dataclasses import asdict
from aiogram import executor
from db import get_db
from bot import dp
from agregates import get_agregated, AgregateResultDTO
from enums import GroupTypeEnum


dt_from = datetime.fromisoformat("2022-09-01T00:00:00")
dt_upto = datetime.fromisoformat("2022-12-31T23:59:00")
# dt_upto = datetime.fromisoformat("2022-12-31T23:59:00")
_group_type = "month"


async def main():
    client = get_db()
    collection = client.agregate.sample_collection
    group_type = GroupTypeEnum(_group_type)
    agregated: AgregateResultDTO = await get_agregated(collection, dt_from, dt_upto, group_type)
    print(asdict(agregated))


if __name__ == "__main__":
    # asyncio.run(main())
    executor.start_polling(dp, skip_updates=True)

