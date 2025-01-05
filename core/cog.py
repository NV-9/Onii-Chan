from discord.ext import commands

from core.bot import Bot

class CustomCogMixin:

    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded")
    