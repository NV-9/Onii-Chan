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
        await self.bot.close()


async def setup(bot: Bot):
    await bot.add_cog(Owner(bot))