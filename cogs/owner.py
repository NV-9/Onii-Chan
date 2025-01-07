from discord.ext import commands

from core.bot import Bot
from core.cog import CustomCogMixin

class Owner(commands.Cog, CustomCogMixin, command_attrs=dict(hidden=True)):

    async def cog_check(self, context: commands.Context):
        return await self.bot.is_owner(context.author)

    @commands.command(name = 'shutdown')
    async def _shutdown(self, context: commands.Context):
        """
        Shutdown the bot
        """
        self.bot.logger.info('Shutting down from user command...')
        await context.message.delete()
        await self.bot.close()
    
    @commands.command(name = 'reload', help = 'Reloads all cogs')
    async def _reload(self, context: commands.Context):
        """
        Reload all cogs and data
        """
        self.bot.logger.info('Reloading cogs...')
        await self.bot.load_all_data()
        await self.bot.reload_all_extensions()
        await context.send('All data and cogs reloaded!', delete_after = 30)
        await context.message.delete(delay = 30)

    @commands.command(name = 'kickall', help = 'Kicks all members from current voice channel')
    async def _kickall(self, context: commands.Context):
        """
        Kicks all members from the current voice channel
        """
        await context.message.delete(delay = 30)

        if context.author.voice is None:
            return await context.send('You must be in a voice channel to use this command!', delete_after = 30)

        voice_channel = context.author.voice.channel
        for member in voice_channel.members:
            await member.move_to(None)
        await context.send('All members have been kicked from the voice channel!', delete_after = 5)


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))