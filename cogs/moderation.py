from discord.ext import commands
import discord
import typing

from core.bot import Bot
from core.cog import CustomCogMixin

class Moderation(commands.Cog, CustomCogMixin):

    async def cog_check(self, context: commands.Context):
        return context.guild is not None

    @commands.command(name = 'kick', description = 'Kicks a user from the server')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, context: commands.Context, member: commands.MemberConverter, *, reason = None):
        await member.kick(reason = reason)
        await context.send(f'{member} has been kicked from the server')
    
    @commands.command(name = 'ban', description = 'Bans a user from the server')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, context: commands.Context, member: commands.MemberConverter, *, reason = None):
        await member.ban(reason = reason)
        await context.send(f'{member} has been banned from the server')
    
    @commands.command(name = 'unban', description = 'Unbans a user from the server')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, context: commands.Context, member: commands.UserConverter):
        await context.guild.unban(member)
        await context.send(f'{member} has been unbanned from the server')
    
    @commands.command(name = 'purge', aliases = ['clear', 'prune'], help = 'Deletes specified number of messages by specified users! If no users are specified, it deletes any message. Default value is 100!', brief = 'Manage Messages')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _purge(self, context: commands.Context, messages: typing.Optional[int] = 100, params: commands.Greedy[typing.Union[discord.Member, discord.Role]] = None, exclude_pins: typing.Optional[bool] = False, *args):
        if messages > 1000:
            await context.send('You can only delete 1000 messages at a time!')
            return
        if params is None:
            values = await context.channel.purge(limit = messages, check = lambda message: not message.pinned if exclude_pins else True, bulk = True)
            await context.send(f'{len(values)} messages have been deleted!', delete_after = 5)
        else:
            def check(message):
                return message.author in params
            await context.channel.purge(limit = messages, check = lambda message: check(message) and (not message.pinned if exclude_pins else True), bulk = True)

    @commands.command(name = 'nick', aliases = ['nickname'], description = 'Changes the nickname of a user')
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def nick(self, context: commands.Context, member: commands.MemberConverter, *, nickname: str = None):
        await member.edit(nick = nickname)
        await context.send(f'{member}\'s nickname has been ' + ('reset' if nickname is None else f'changed to {nickname}'))
    
    

async def setup(bot: Bot):
    await bot.add_cog(Moderation(bot))