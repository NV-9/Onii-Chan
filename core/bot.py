from discord.ext import commands
from discord import Intents

from config.settings import BOT_TOKEN
from core.prefix import get_prefix

class Bot(commands.Bot):

    token: str

    def __init__(self, **kwargs):
        """
        Initialising bot with state variables and setting required attributes
        """
        if not BOT_TOKEN:
            raise ValueError('No bot token provided')
        self.token = BOT_TOKEN
        
        super().__init__(
            case_insensitive = True,
            command_prefix = get_prefix,
            heartbeat_timeout = 150.0,
            intents = Intents.all(),
            **kwargs,
        )

    def run(self, *args, **kwargs):
        """
        Run the bot
        """
        super().run(self.token, *args, **kwargs)
    
    async def on_ready(self):
        """
        On bot ready event
        """
        print(f'{self.user.name} is online! ')

