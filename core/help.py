from discord import Embed
from discord.ext import commands

__all__ = ['Help']

class Help(commands.HelpCommand):

    def get_command_signature(self, command: commands.Command, context: commands.Context):
        aliases = "|".join(command.aliases)
        partial_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name
        complete_invoke = command.qualified_name.replace(command.name, "")
        signature = f"{context.prefix}{complete_invoke}{partial_invoke} {command.signature}"
        return signature

    async def send_bot_help(self, mapping):
        embed = Embed(
            title = 'Help', 
            description = 'Here is my command set below! Specify a category or command after this command to get more information about each one! '
        )
        for cog in mapping:
            commandset = ', '.join([command.name for command in [await self.filter_commands(mapping[cog], sort = True)][0]])
            if commandset:
                embed.add_field(
                    name = cog.qualified_name if cog else (cog or 'Miscellaneous'), 
                    value = '`' + commandset + '`',
                    inline = False
                ) 
        channel = self.get_destination()     
        return await channel.send(embed = embed)

    async def send_command_help(self, command):
        cmd = self.get_command_signature(command, self.context)
        embed = Embed(title = f'Help for {command}', description = f'`{cmd}`')
        embed.add_field(name = 'Description', value = command.help)
        channel = self.get_destination()   
        return await channel.send(embed = embed)

    async def send_group_help(self, group):
        cmd = self.get_command_signature(group, self.context)
        embed = Embed(title = f'Help for {group}', description = f'`{cmd}`')
        embed.add_field(name = 'Description', value = group.help)
        subcommands = f'`{", ".join([command.name for command in group.walk_commands()])}`' if hasattr(group, "all_commands") else None
        embed.add_field(name = 'Subcommands', value = subcommands, inline = False) if subcommands else None
        channel = self.get_destination()    
        return await channel.send(embed = embed)

    async def send_cog_help(self, cog):
        cogdata = self.get_bot_mapping()
        cogdata = cogdata[cog]
        embed = Embed(title = f'Help for {cog.qualified_name if cog else cog}')
        embed.add_field(
                name = 'Commands', 
                value = '`'+', '.join([command.name for command in cogdata])+'`',
                inline = False
            )
        channel = self.get_destination()     
        return await channel.send(embed = embed)

    async def on_help_command_error(self, context, error):
        embed = Embed(
            title = 'Command / Group Not Found! ',
            description = error
        )
        return await context.send(embed = embed)

    async def command_not_found(self, string):
        embed = Embed(
            title = 'Command / Group Not Found! ',
            description = f'The command or category `{string}` simply does not exist! You may have mispelt the command name! '
        )
        return embed
    
    async def subcommand_not_found(self, command, string):
        embed = Embed(
            title = 'Subcommand Not Found! ',
            description = f'The subcommand `{string}` simply does not exist! You may have mispelt the subcommand name! '
        )
        return embed

    async def send_error_message(self, error):
        channel = self.get_destination()
        return await channel.send(embed = error)