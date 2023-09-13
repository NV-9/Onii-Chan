import datetime
import time 
from core import Embed, GuildCog, Logger, Bot
from discord.ext import commands


class Utility(GuildCog):
        
    @commands.command(name = 'ping', help = 'Provides current latency and ping! ')
    async def _ping(self, context: commands.Context, *args):
        embed = Embed(title = '🏓 Current Ping 🏓', description = 'Pinging...')
        before_time = time.time()
        message = await context.send(embed = embed)
        latency = round(self.bot.latency * 1000)
        elapsed_ms = round((time.time() - before_time) * 1000) - latency
        embed.description = None
        embed.add_field(name = 'Ping', value = f'{elapsed_ms}ms')
        embed.add_field(name = 'Latency', value = f'{latency}ms')
        await message.edit(embed = embed, delete_after = 30)

    @commands.command(name = 'uptime', help = 'States how long it has been since I last woke up! ')
    async def _uptime(self, context: commands.Context, *args):
        current_time = datetime.datetime.now().replace(microsecond=0)
        embed = Embed(title = '📶 Uptime 📶', description=f"Time since I went online: \n`{current_time - self.bot.start_time}`")
        await context.send(embed = embed, delete_after = 30)

    @commands.command(name = 'starttime', help = 'States the exact time when I last woke up! ')
    async def _starttime(self, context: commands.Context, *args):
        embed = Embed(title = '🌅 Starttime 🌅', description=f"I have been awake since `{self.bot.start_time}`! ")
        await context.send(embed = embed, delete_after = 30)

    @commands.command(name = 'invite', help = 'Provides invite link to invite me to another server! ')
    async def _invite(self, context: commands.Context, *args):
        embed = Embed(title = '✉️ Invite ✉️', description = f'[Invite me]({self.bot.invite_url})')
        await context.send(embed = embed, delete_after = 30)
    
    @commands.command(name = 'info', aliases= ['about'], help = 'Provides my application details! ')
    async def _info(self, context: commands.Context, *args):
        embed = Embed(title = f'{self.bot.user.name}')   
        embed.set_thumbnail(url = self.bot.user.avatar.url) if self.bot.user.avatar else None
        info = await self.bot.application_info()
        owner = info.owner
        try:
            embed.add_field(
                name = 'My Stats',
                value = f'''```Guilds: {len(self.bot.guilds)}\nUsers: {len(self.bot.users)}\nShards: {self.bot.shard_count}\nShard ID: {context.guild.shard_id}```''',
                inline = False
            )
            embed.add_field(name = 'Type', value = f'```Language: Python\nVersion: 3.11.4\nBase: discord.py```', inline = False)
            embed.add_field(name = 'Invite', value = f'[Invite me]({self.bot.invite_url})', inline = False)
            embed.set_author(name = 'Requested by ' + (context.message.author.nick or context.message.author.name), url = context.message.author.avatar_url)
            embed.set_footer(text = f'Made by {owner}', icon_url = owner.avatar.url)
        except:
            pass
        await context.send(embed = embed, delete_after = 30)


async def setup(bot: Bot):
    await bot.add_cog(
        Utility(
            bot,
            Logger('utility', 'utility.log')()
        )
    )