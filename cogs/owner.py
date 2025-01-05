from discord.ext import commands

from core.bot import Bot
from core.cog import CustomCogMixin

class Owner(commands.Cog, CustomCogMixin):

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
        Reload all cogs
        """
        self.bot.logger.info('Reloading cogs...')
        await self.bot.reload_all_extensions()
        await context.send('All cogs reloaded!', delete_after = 30)
        await context.message.delete(delay = 30)


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))