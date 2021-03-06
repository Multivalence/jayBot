import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv(find_dotenv())

class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
        return '%s%s %s' % (self.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort=True)
            command_signatures = [self.get_command_signature(c) for c in filtered]
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


bot = commands.Bot(command_prefix=commands.when_mentioned_or(os.environ["PREFIX"]),
                   status = discord.Status.offline,
                   intents = discord.Intents.all(),
                   help_command=MyHelp())


extensions = [
    'ext.startup',
    'ext.errors',
    'ext.commands.blacklist',
    'ext.commands.whitelist',
    'ext.events'
]

for ext in extensions:
    bot.load_extension(ext)


# For Testing Purpose Only

# @bot.command()
# async def test(ctx):
#
#     embed = discord.Embed(
#         description="--- (10/13 - Recap) ---\n\n$JSPR 25%\n$GROM 27%\n$PALT 21%\n$AEHR 11%",
#         colour=discord.Colour.blue(),
#         timestamp=datetime.utcnow()
#     )
#     embed.set_author(name="Mini_Tradez (@Mini_Tradez)",icon_url=ctx.author.avatar_url)
#     await ctx.send(embed=embed)


bot.run(os.environ["TOKEN"])