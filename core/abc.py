import asyncio 
import datetime
import discord
import logging
import os

from discord.message import Message
import settings
from discord.ext import commands 
from .components import get_prefix, open_or_create, save_to_file


__all__ = ['JSONStore', 'Logger', 'Embed', 'GuildCog', 'HiddenCog', 'Help', 'Bot']

# JSON manager 
class JSONStore:

    name = None 
    path = None 
    indent = 4 
    default = None 
    data = None 
    lock = None

    def __init__(
            self,
            file_name: str,
            *args,
            file_path: str = settings.DATA_DIR,
            indent = 4,
            default = None, 
            **kwargs):
        
        self.name = file_name
        self.path = file_path 
        self.file = os.path.join(self.path,self.name)
        self.indent = indent 
        self.default = default or dict()

        self.lock = asyncio.Lock()
        self.loop = kwargs.pop('loop', asyncio.get_event_loop())

        self.load_data()

    def load_data(self):
        self.data = open_or_create(self.file, self.default, self.indent)
    
    def save_data(self):
        save_to_file(self.name, self.path, self.file, self.data, self.indent)
    
    def get_value(self, key):
        return self.data.get(key, None)

    def __getitem__(self, key):
        return self.get_value(key)
    
    def edit_value(self, key, value):
        self.data[key] = value 
        self.save_data()

    def __setitem__(self, key, value):
        self.edit_value(key, value)

    def clear_value(self, key):
        try:
            value = self.data.pop(key)
            self.save_data()
            return value 
        except:
            return None 
    
    def get_keys(self):
        return list(self.data.keys())

    def get_values(self):
        return list(self.data.values())
    
    def clear_file(self, overwrite = None):
        self.data = overwrite or self.default
        self.save_data()
        return self.data

    def __len__(self):
        return len(self.data)
    
    async def load(self):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.load_data)
        return data
    
    async def save(self):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.save_data)
        return data
    
    async def get(self, key):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.get_value, key)
        return data
    
    async def edit(self, key, value):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.edit_value, key, value)
        return data

    async def remove(self, key):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.clear_value, key)
        return data
    
    async def keys(self, *args):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.get_keys)
        return data

    async def values(self, *args):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.get_values)
        return data 

    async def clear(self, *args):
        async with self.lock:
            data = await self.loop.run_in_executor(None, self.clear_file)
        return data
    

# Logger
class Logger:

    name = None 
    file = None 
    path = None
    level = None

    def __init__(
            self, 
            name: str,
            file: str,
            path: str = settings.LOGS_DIR, 
            level = logging.DEBUG,
            *args, 
            **kwargs):
        
        self.name = name 
        self.file = (file[:-3] + '.log') if file.endswith('.py') else file
        self.path = path 
        self.level = level


    def __call__(self) -> logging.Logger:
        
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)
        
        if not os.path.exists(self.path):
            try:
                os.makedirs(self.path)
            except:
                pass
           
        file_handler = logging.FileHandler(os.path.join(self.path, self.file))
        formatter    = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger


    def clear(self):
        if os.path.exists(self.path / self.file):
            os.remove(self.path / self.file)


# Custom Embed
class Embed(discord.Embed):

    def __init__(self, title = None, description = "", timestamp = datetime.datetime.utcnow(), colour = discord.Colour.random(), **kwargs):
        changes = {
            'timestamp': timestamp,
            'description': description,
            'title': title,
            'colour': colour    
        }
        kwargs.update(**changes)
        super().__init__(**kwargs)


# Guild Cog
class GuildCog(commands.Cog):

    def __init__(self, bot: commands.Bot, logger: logging.Logger = None):
        self.bot = bot 
        self.logger = logger 

        if logger is None:
            raise Exception('Logger Not Set!')
        
    async def cog_check(self, context: commands.Context):
        return context.guild 

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"{self.__class__.__name__} cog has been loaded")


# Hidden Cog
class HiddenCog(commands.Cog, command_attrs = dict(hidden = True)):

    def __init__(self, bot: commands.Bot, logger: logging.Logger = None):
        self.bot = bot 
        self.logger = logger

        if logger is None:
            raise Exception('Logger Not Set')
            

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"{self.__class__.__name__} cog has been loaded")


# Help Command 
class Help(commands.HelpCommand):

    def get_command_signature(self, command: commands.Command, context: commands.Context):
        aliases = "|".join(command.aliases)
        # Providing all aliases
        partial_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name
        # Constructing command and aliases
        complete_invoke = command.qualified_name.replace(command.name, "")
        # Getting full command and removing name for groups
        signature = f"{context.prefix}{complete_invoke}{partial_invoke} {command.signature}"
        # Combining data to create signature
        return signature


    async def send_bot_help(self, mapping):
        # Default command with 0 parameters
        embed = Embed(
            title = 'Help', 
            description = 'Here is my command set below! Specify a category or command after this command to get more information about each one! '
        )
        # Setting up embed
        for cog in mapping:
            # Fetching every cog
            commandset = ', '.join([command.name for command in [await self.filter_commands(mapping[cog], sort = True)][0] if not command.hidden ])
            # Retrieving all commands
            if commandset:
                # Excluding hidden cogs
                embed.add_field(
                    name = cog.qualified_name if cog else (cog or 'Miscellaneous'), 
                    value = '`' + commandset + '`',
                    inline = False
                ) 
                # Adding cog commands to embed
        channel = self.get_destination()
        # Fetching channel and sending help        
        return await channel.send(embed = embed)

    async def send_command_help(self, command):
        # Help specific for commands
        cmd = self.get_command_signature(command, self.context)
        # Signature of a specific command
        embed = Embed(title = f'Help for {command}', description = f'`{cmd}`')
        embed.add_field(name = 'Description', value = command.help)
        channel = self.get_destination()
        # Fetching channel and sending help        
        return await channel.send(embed = embed)

    async def send_group_help(self, group):
        # Specific for group help
        cmd = self.get_command_signature(group, self.context)
        # Signature of a specific group
        embed = Embed(title = f'Help for {group}', description = f'`{cmd}`')
        embed.add_field(name = 'Description', value = group.help)
        subcommands = f'`{", ".join([command.name for command in group.walk_commands() if not command.hidden])}`' if hasattr(group, "all_commands") else None
        # Adding in all subcommands
        embed.add_field(name = 'Subcommands', value = subcommands, inline = False) if subcommands else None
        channel = self.get_destination()
        # Fetching channel and sending help        
        return await channel.send(embed = embed)

    async def send_cog_help(self, cog):
        # Specific for cog help
        cogdata = self.get_bot_mapping()
        cogdata = cogdata[cog]
        # Getting cog data
        embed = Embed(title = f'Help for {cog.qualified_name if cog else cog}')
        embed.add_field(
                name = 'Commands', 
                value = '`'+', '.join([command.name for command in cogdata if not command.hidden])+'`',
                inline = False
            )
        # Listing all cog commands
        channel = self.get_destination()
        # Fetching channel and sending help        
        return await channel.send(embed = embed)

    async def on_help_command_error(self, context, error):
        # Any help commands error
        embed = Embed(
            title = 'Command / Group Not Found! ',
            description = error
        )
        return await context.send(embed = embed)

    async def command_not_found(self, string):
        # When a command does not exist
        embed = Embed(
            title = 'Command / Group Not Found! ',
            description = f'The command or category `{string}` simply does not exist! You may have mispelt the command name! '
        )
        return embed
    
    async def subcommand_not_found(self, command, string):
        # When a subcommand does not exist
        embed = Embed(
            title = 'Subcommand Not Found! ',
            description = f'The subcommand `{string}` simply does not exist! You may have mispelt the subcommand name! '
        )
        return embed

    async def send_error_message(self, error):
        # Sending generated embed on error
        channel = self.get_destination()
        return await channel.send(embed = error)


# Bot class
class Bot(commands.Bot):

    def __init__(self, **kwargs):
        if not settings.TOKEN:
            raise Exception('Bot Token not set!')
        
        super().__init__(
            command_prefix = get_prefix,
            case_insensitive = True,
            heartbeat_timeout = 150.0,
            intents = discord.Intents.all(),
            help_command = Help(),
            **kwargs
        )
        # Setting tokens and meta data
        self.token = settings.TOKEN 
        self.invite_url = settings.INVITE_URL

        self._logger: logging.Logger = kwargs.pop('logger', None)
        self.start_time = datetime.datetime.now().replace(microsecond = 0)

    async def on_ready(self):
        print(f'{self.user.name} is online! ')
        self._logger.info(f'{self.user.name} is online! ')

    async def load_extensions(self):
        # dynamic extension loading
        dirname = os.path.basename(settings.COGS_DIR)
        if os.path.exists(settings.COGS_DIR):
            for cog in os.listdir(f'{settings.COGS_DIR}'):
                if cog.endswith('.py'):
                    await self.load_extension(f'{dirname}.{cog[:-3]}')
        else:
            os.makedirs(settings.COGS_DIR)
        print(self.extensions)



