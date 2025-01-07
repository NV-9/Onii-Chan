from decouple import config
from pathlib import Path

# Base Settings
COMMAND_PREFIX = config('DISCORD_COMMAND_PREFIX', default='$')
BOT_TOKEN = config('DISCORD_BOT_TOKEN')

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
COGS_DIR = BASE_DIR / 'cogs'
LOGS_DIR = BASE_DIR / 'logs'
DATA_DIR = BASE_DIR / 'data'

# Logging
LOG_FILE = LOGS_DIR / 'bot.log'

# Data
WATCH_FILE = DATA_DIR / 'overwatch.json'
