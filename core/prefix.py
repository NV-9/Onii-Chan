from discord.ext import commands
from discord import Message

from config.settings import COMMAND_PREFIX

__all__ = ['get_prefix']

async def get_prefix(bot: commands.Bot, message: Message):
    """
    Get the prefix for a message
    """
    prefix_set = [ COMMAND_PREFIX ]
    if message.guild:
        pass # To be implemented
    return commands.when_mentioned_or(*prefix_set)(bot, message)
