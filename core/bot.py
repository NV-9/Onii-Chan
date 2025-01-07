from datetime import datetime
from discord.ext import commands
from discord.utils import oauth_url
from discord import Intents, Permissions
import logging

from config.settings import BOT_TOKEN, COGS_DIR, DATA_DIR, LOGS_DIR, LOG_FILE, WATCH_FILE
from core.handler import JSONHandler
from core.help import Help
from core.prefix import get_prefix

__all__ = ['Bot']

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

        self._ensure_paths_exist()

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

    def _ensure_paths_exist(self):
        """
        Ensures that the log and data directories exist
        """
        if not LOGS_DIR.exists():
            LOGS_DIR.mkdir(parents = True)
        if not DATA_DIR.exists():
            DATA_DIR.mkdir(parents = True)
        
    async def start(self, *args, **kwargs):
        """
        Start the bot
        """
        if not COGS_DIR.exists():
            self.logger.error('No cogs directory found')
            raise FileNotFoundError('No cogs directory found')
        
        self.logger.info('Loading data...')
        await self.load_all_data()

        self.logger.info('Loading cogs...')
        await self.reload_all_extensions()

        self.logger.info('Starting the bot...')
        await super().start(self.token, *args, **kwargs)

    async def load_all_data(self):
        """
        Load all the data
        """
        self._overwatch_handler = JSONHandler(WATCH_FILE, default_data={'Guilds': {}})
    
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
        self.logger.info('Generating invite URL...')
        self.client_id = (await self.application_info()).id
        self.invite_url = oauth_url(client_id = self.client_id, permissions = Permissions(administrator=True))

        self.logger.info(f'{self.user.name} is online!')

    async def on_command_error(self, context: commands.Context, exception: commands.CommandError):
        """
        Handle errors in command execution.
        """
        self.logger.error(f"An error occurred while processing the command '{context.command}': {exception}", exc_info=True)
        if self.is_owner(context.author):
            await context.send(f"An error occurred: {exception}")
