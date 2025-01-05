import asyncio 
from core.bot import Bot

bot = Bot()

async def main():
    async with bot:
        await bot.start(bot.token)

if __name__ == '__main__':
    asyncio.run(main())