from discord.ext import commands

class CustomCogMixin:

    def __init__(self, bot: commands.Bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} cog has been loaded")
    