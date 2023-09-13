import aiohttp
import os 
import discord
import settings 
from core import Bot, HiddenCog, Logger
from discord.ext import commands


class Owner(HiddenCog, command_attrs = dict(hidden = True)):

    async def cog_check(self, context: commands.Context):
        return await self.bot.is_owner(context.message.author)

    async def reload_or_load_extension(self, module):
        try:
            await self.bot.reload_extension(f'{os.path.basename(settings.COGS_DIR)}.{module}')
        except commands.ExtensionNotLoaded:
            await self.bot.load_extension(f'{os.path.basename(settings.COGS_DIR)}.{module}')

    @commands.command(name = 'shutdown', aliases = ['sd'])
    async def _shutdown(self, context: commands.Context):
        if self.logger is not None:
            self.logger.info('Bot shut down from command! ')
        await context.send(':wave:')
        await self.bot.close()

    @commands.command(name = 'dcall')
    async def _dcall(self, context: commands.Context):
        if context.message.author.voice:
            vc = context.message.author.voice.channel
            for member in vc.members:
                await member.move_to(None)

    @commands.command(name = 'load')
    async def _load(self, context: commands.Context, *, module: str):
        try:
            async with context.typing():
                await self.reload_or_load_extension(module)
        except commands.ExtensionError as e:
            await context.send(f'{e.__class__.__name__}: {e}')
        else:
            await context.send('\N{OK HAND SIGN}')

    @commands.command(name = 'unload')
    async def _unload(self, context: commands.Context, *, module: str):
        try:
            print(self.bot.extensions)
            async with context.typing():
                await self.bot.unload_extension(f'{os.path.basename(settings.COGS_DIR)}.{module}')
        except commands.ExtensionError as e:
            await context.send(f'{e.__class__.__name__}: {e}')
        else:
            await context.send('\N{OK HAND SIGN}')
    
    @commands.group(name = 'reload', invoke_without_command = True)
    async def _reload(self, context: commands.Context, *, module: str):
        try:
            async with context.typing():
                await self.reload_or_load_extension(module)
        except commands.ExtensionError as e:
            await context.send(f'{e.__class__.__name__}: {e}')
        else:
            await context.send('\N{OK HAND SIGN}')

    @_reload.command(name = 'all')
    async def _reload_all(self, context: commands.Context):
        try:
            async with context.typing():
                dirname = os.path.basename(settings.COGS_DIR)
                if os.path.exists(settings.COGS_DIR):
                    for cog in os.listdir(f'{settings.COGS_DIR}'):
                        if cog.endswith('.py'):
                            await self.reload_or_load_extension(cog[:-3])
        except commands.ExtensionError as e:
            await context.send(f'{e.__class__.__name__}: {e}')
        else:
            await context.send('\N{OK HAND SIGN}')


    @commands.command(name = 'clearlogs')
    async def _clearlogs(self, context: commands.Context):
        for file in os.listdir(settings.LOGS_DIR):
            if str(file).endswith('.log'):
                with open(os.path.join(settings.LOGS_DIR, file), 'w'):
                    pass
        await context.send('\N{OK HAND SIGN}')
    
    @commands.command(name = 'changepfp')
    async def _changepfp(self, context: commands.Context, pfp: str):
        name = 'image' + ('.png' if pfp.endswith('.png') else '.jpg')
        img = os.path.join(settings.DATA_DIR, 'temp', name)
        async with aiohttp.ClientSession() as session:
            async with session.get(pfp) as resp:
                if resp.status == 200:
                    with open(img, 'wb') as fd:
                        async for chunk in resp.content.iter_chunked(10):
                            fd.write(chunk)
                else:
                    return await context.send("Could not fetch image!", delete_after = 5)
        with open(img, 'rb') as image:
            await self.bot.user.edit(avatar = image.read())
        await context.send('\N{OK HAND SIGN}')
        os.remove(img)



async def setup(bot: Bot):
    await bot.add_cog(
        Owner(
            bot,
            Logger('owner', 'owner.log')()
        )
    )

