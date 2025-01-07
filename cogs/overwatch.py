from discord.ext import commands
import discord

from core.bot import Bot
from core.cog import CustomCogMixin
from core.handler import JSONLineHandler

class Overwatch(commands.Cog, CustomCogMixin):

    _file_ext = 'json1'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config = self.bot._overwatch_handler
        self._guilds = self._config.s_get('Guilds') or {}
        self._message_handlers = {}

    async def cog_check(self, context: commands.Context):
        return context.guild is not None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        guild_id = str(message.guild.id)
        if guild_id in self._guilds:
            if message.channel.id in self._guilds[guild_id]:
                await self._handle_message(message)
    
    async def _handle_message(self, message: discord.Message):
        channel_id = message.channel.id
        handler = self._message_handlers.get(channel_id)
        if handler is None:
            handler = JSONLineHandler(f'overwatch/{channel_id}.{self._file_ext}', 'id', loop=self.bot.loop, unique_only=True)
            self._message_handlers[channel_id] = handler
        message_data = {
            "id": message.id,
            "content": message.content,
            "author": {
                "id": message.author.id,
                "name": message.author.name,
                "discriminator": message.author.discriminator,
                "bot": message.author.bot,
            },
            "channel": {
                "id": message.channel.id,
                "name": message.channel.name,
            },
            "guild": {
                "id": message.guild.id,
                "name": message.guild.name,
            },
            "created_at": message.created_at.isoformat(),
            "edited_at": message.edited_at.isoformat() if message.edited_at else None,
            "attachments": [
                {"id": attachment.id, "filename": attachment.filename, "url": attachment.url}
                for attachment in message.attachments
            ],
            "embeds": [embed.to_dict() for embed in message.embeds],
            "reactions": [
                {"emoji": str(reaction.emoji), "count": reaction.count}
                for reaction in message.reactions
            ],
            "pinned": message.pinned,
            "tts": message.tts,
        }
        await handler.add(message_data)
    
    @commands.group(name='overwatch', aliases=['ow'], invoke_without_command=True)
    @commands.has_guild_permissions(administrator=True)
    async def overwatch_group(self, context: commands.Context):
        await context.send('Overwatch is a group command. Use `add`, `remove`, or `list` subcommands.')
    
    @overwatch_group.command(name='add')
    async def overwatch_add(self, context: commands.Context, channel: discord.TextChannel):
        guild_id = str(context.guild.id)
        channel_id = channel.id
        if guild_id not in self._guilds:
            self._guilds[guild_id] = []
        if channel_id in self._guilds[guild_id]:
            await context.message.delete(delay = 5)
            return await context.send(f'Channel {channel.mention} is already being logged.')
        self._guilds[guild_id].append(channel.id)
        await self._config.update('Guilds', self._guilds)
        await context.send(f'Added channel {channel.mention} to be logged.', delete_after = 30)
        await context.message.delete(delay = 5)

    @overwatch_group.command(name='remove')
    async def overwatch_remove(self, context: commands.Context, channel: discord.TextChannel):
        guild_id = str(context.guild.id)
        channel_id = channel.id
        if guild_id in self._guilds:
            if channel_id in self._guilds[guild_id]:
                self._guilds[guild_id].remove(channel_id)
                if not self._guilds[guild_id]:
                    del self._guilds[guild_id]
                await self._config.update('Guilds', self._guilds)
                await context.send(f'Removed channel {channel.mention} from being logged.', delete_after = 30)
            else:
                await context.send(f'Channel {channel.mention} is not being logged.', delete_after = 30)
        else:
            await context.send('No channels are being logged.', delete_after = 30)
        await context.message.delete(delay = 5)
        
    @overwatch_group.command(name='list')
    async def overwatch_list(self, context: commands.Context):
        guild_id = str(context.guild.id)
        if guild_id in self._guilds:
            channels = [context.guild.get_channel(int(channel_id)).mention for channel_id in self._guilds[guild_id]]
            await context.send(f'Channels being current logged: {", ".join(channels)}', delete_after = 30)
        else:
            await context.send('No channels are being logged in this server.', delete_after = 30)
        await context.message.delete(delay = 5)


async def setup(bot: Bot):
    await bot.add_cog(Overwatch(bot))