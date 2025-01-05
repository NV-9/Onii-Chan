from decouple import config

COMMAND_PREFIX = config('DISCORD_COMMAND_PREFIX', default='$')

BOT_TOKEN = config('DISCORD_BOT_TOKEN')