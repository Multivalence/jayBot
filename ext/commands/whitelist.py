import discord
from discord.ext import commands
from datetime import datetime
from sqlite3 import IntegrityError
from ext.custom_errors import NoSubcommandFound, WhitelistNotFound, WhitelistAlreadyExists


# Custom Errors




class Whitelist(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    @commands.group(invoke_without_command=True, name='whitelist', description='Command to add whitelist', aliases=['w', 'wl'])
    async def whitelist(self, ctx):
        raise NoSubcommandFound


    @whitelist.command(name='add', description='Add something to whitelist')
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *, filter : str):

        sql = 'INSERT INTO filters(whitelist) VALUES (?)'

        try:
            await self.bot.db.execute(sql, (filter.lower(),))
            await self.bot.db.commit()

        except IntegrityError:
            raise WhitelistAlreadyExists

        else:

            embed = discord.Embed(
                title = 'Action Successful',
                description=f"Whitelist added: {filter}",
                colour=discord.Colour.from_rgb(255,255,255),
                timestamp=datetime.utcnow()
            )

            return await ctx.send(embed=embed)



    @whitelist.command(name='remove', description='Remove something from whitelist')
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, *, filter : str):

        async with self.bot.db.execute('SELECT whitelist from filters') as cursor:
            whitelisted_terms = await cursor.fetchall()

            if filter.lower() not in [i[0] for i in whitelisted_terms]:
                raise WhitelistNotFound

        sql = 'DELETE FROM filters where whitelist=?'

        async with self.bot.db.execute(sql, (filter.lower(),)) as _:
            await self.bot.db.commit()

        embed = discord.Embed(
            title="Action Successful",
            description=f"Whitelist removed: {filter}",
            colour=discord.Colour.from_rgb(255,255,255),
            timestamp=datetime.utcnow()
        )

        return await ctx.send(embed=embed)


#Setup
def setup(bot):
    bot.add_cog(Whitelist(bot))