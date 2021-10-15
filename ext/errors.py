import discord
import sys
import traceback
from discord.ext import commands
from ext.custom_errors import NoSubcommandFound
from ext.custom_errors import WhitelistNotFound, WhitelistAlreadyExists
from ext.custom_errors import BlacklistAlreadyExists, BlacklistNotFound





class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Gets original attribute of error
        error = getattr(error, "original", error)

        if isinstance(error, commands.errors.BadArgument):
            return await ctx.send("Bad argument.",delete_after=10)

        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send("You are missing a required argument",delete_after=10)

        elif isinstance(error, discord.ext.commands.errors.NoPrivateMessage):
            return

        elif isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return await ctx.send("You require Administrator privileges to do this command!")

        elif isinstance(error, WhitelistAlreadyExists):
            return await ctx.send("That term is already whitelisted!")

        elif isinstance(error, WhitelistNotFound):
            return await ctx.send("Cannot find that term in whitelist")

        elif isinstance(error, BlacklistAlreadyExists):
            return await ctx.send("That term is already blacklisted")

        elif isinstance(error, BlacklistNotFound):
            return await ctx.send("Cannot find that term in blacklist")

        elif isinstance(error, NoSubcommandFound):
            return await ctx.send("No sub-command found!")

        else:
            # Prints original traceback if it isnt handled
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



#Setup
def setup(bot):
    bot.add_cog(Errors(bot))