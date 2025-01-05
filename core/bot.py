from datetime import datetime
from discord.ext import commands
from discord import Intents
import logging

from config.settings import BOT_TOKEN, COGS_DIR, LOG_FILE
from core.help import Help
from core.prefix import get_prefix

class Bot(commands.Bot):

    token: str
    logger: logging.Logger
    start_time: datetime

    def __init__(self, **kwargs):
        """
        Initialising bot with state variables and setting required attributes
        """
        if not BOT_TOKEN:
            raise ValueError('No bot token provided')
        self.token = BOT_TOKEN

        self.logger = self._setup_logger(LOG_FILE)
        self.start_time = datetime.now()
        
        super().__init__(
            case_insensitive = True,
            command_prefix = get_prefix,
            heartbeat_timeout = 150.0,
            help_command = Help(),
            intents = Intents.all(),
            **kwargs,
        )
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """
        Sets up the logger for the bot.
        """
        logger = logging.getLogger('bot')
        logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
    
    async def start(self, *args, **kwargs):
        """
        Start the bot
        """
        if not COGS_DIR.exists():
            self.logger.error('No cogs directory found')
            raise FileNotFoundError('No cogs directory found')

        self.logger.info('Loading cogs...')
        await self.reload_all_extensions()

        self.logger.info('Starting the bot...')
        await super().start(self.token, *args, **kwargs)
    
    async def reload_all_extensions(self):
        """
        Reloads all the extensions
        """
        for cog in COGS_DIR.glob('*.py'):
            try:
                await self.reload_extension(f'cogs.{cog.stem}')
                self.logger.info(f'Reloaded cog: {cog.stem}')
            except commands.ExtensionNotLoaded:
                try:
                    await self.load_extension(f'cogs.{cog.stem}')
                    self.logger.info(f'Loaded cog: {cog.stem}')
                except Exception as e:
                    self.logger.error(f'Failed to load cog {cog.stem}: {e}')
            except Exception as e:
                self.logger.error(f'Failed to load cog {cog.stem}: {e}')

    async def on_ready(self):
        """
        On bot ready event
        """
        self.logger.info(f'{self.user.name} is online!')

