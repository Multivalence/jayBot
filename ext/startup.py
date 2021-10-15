import discord
import os
from discord.ext import commands
import aiosqlite

class Startup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initializeDB())




    async def initializeDB(self):
        self.bot.db = await aiosqlite.connect('filters.db')

        sql = """CREATE TABLE IF NOT EXISTS filters (
            whitelist TEXT UNIQUE,
            blacklist TEXT UNIQUE)
        """

        await self.bot.db.execute(sql)
        await self.bot.db.commit()



    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} | {self.bot.user.id}')




#Setup
def setup(bot):
    bot.add_cog(Startup(bot))