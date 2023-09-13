import discord 
import json 
import os 
import settings 
import uuid
from discord.ext import commands 


__all__ = ['open_or_create', 'save_to_file', 'get_prefix', 'reply_or_send']

def open_or_create(file: str, default = None, indent = 4):
    if os.path.exists(file):
        with open(file, 'r', encoding = 'utf-8') as f:
            data = json.load(f) or dict()
        return data 
    default = default or dict()
    try:
        os.makedirs((os.path.dirname(file)))
    except: 
        pass 
    with open(file, 'w', encoding = 'utf-8') as f:
        json.dump(default, f, indent = indent)
    return default


def save_to_file(name: str, path: str, file: str, data = None, indent = 4):
    temporary_file = os.path.join(path, f'{uuid.uuid4()}-{name}.tmp')
    data = data or dict()
    with open(temporary_file, 'w', encoding = 'utf-8') as open_file:
        json.dump(data, open_file, ensure_ascii = True, indent = indent)
    os.replace(temporary_file, file)


def get_prefix(bot: commands.Bot, message: discord.Message):
    prefixes = settings.PREFIXES + [f'<@!{bot.user.id}> ', f'<@{bot.user.id}> ', f'<@!{bot.user.id}>', f'<@{bot.user.id}>']
    if message.guild:
        if hasattr(bot, '_prefixes'):
            prefixes += bot._prefixes.get_value(str(message.guild.id)) or list()
    return prefixes 


async def reply_or_send(context: commands.Context, message: str, *args, **kwargs):
    try: 
        return await context.reply(message, *args, **kwargs)
    except:
        return await context.send(message, *args, **kwargs)
