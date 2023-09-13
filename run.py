import asyncio
import os
from core import Bot, Logger

logger =  Logger('main', 'main.log')()
bot = Bot(logger = logger)


async def main():
    async with bot:
        await bot.load_extensions()
        await bot.start(bot.token)

asyncio.run(main())