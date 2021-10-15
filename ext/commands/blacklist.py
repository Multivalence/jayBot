import discord
from discord.ext import commands
from datetime import datetime
from sqlite3 import IntegrityError
from ext.custom_errors import NoSubcommandFound, BlacklistNotFound, BlacklistAlreadyExists

# Custom Errors




class Blacklist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.group(invoke_without_command=True, name='blacklist', description='Command to add whitelist', aliases=['b', 'bl'])
    async def blacklist(self, ctx):
        raise NoSubcommandFound


    @blacklist.command(name='add', description='Add something to blacklist')
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *, filter : str):

        sql = 'INSERT INTO filters(blacklist) VALUES (?)'

        try:
            await self.bot.db.execute(sql, (filter.lower(),))
            await self.bot.db.commit()

        except IntegrityError:
            raise BlacklistAlreadyExists

        else:

            embed = discord.Embed(
                title = 'Action Successful',
                description=f"Blacklist added: {filter}",
                colour=discord.Colour.default(),
                timestamp=datetime.utcnow()
            )

            return await ctx.send(embed=embed)



    @blacklist.command(name='remove', description='Remove something from blacklist')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, *, filter : str):

        async with self.bot.db.execute('SELECT blacklist from filters') as cursor:
            blacklisted_terms = await cursor.fetchall()

            if filter.lower() not in [i[0] for i in blacklisted_terms]:
                raise BlacklistNotFound

        sql = 'DELETE FROM filters where blacklist=?'

        async with self.bot.db.execute(sql, (filter.lower(),)) as _:
            await self.bot.db.commit()

        embed = discord.Embed(
            title="Action Successful",
            description=f"Blacklist removed: {filter}",
            colour=discord.Colour.default(),
            timestamp=datetime.utcnow()
        )

        return await ctx.send(embed=embed)


#Setup
def setup(bot):
    bot.add_cog(Blacklist(bot))