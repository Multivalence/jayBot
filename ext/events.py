import discord
import os
import aiohttp
from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.input_channel = int(os.environ["INPUT-CHANNEL"])
        self.output_channel = int(os.environ["OUTPUT-CHANNEL"])


    async def fetch_whitelist_data(self):
        sql = 'SELECT whitelist FROM filters'

        async with self.bot.db.execute(sql) as cursor:
            terms = await cursor.fetchall()
            whitelisted_terms = [i[0] for i in terms if i[0] != None]

        return whitelisted_terms


    async def fetch_blacklist_data(self):
        sql = 'SELECT blacklist FROM filters'

        async with self.bot.db.execute(sql) as cursor:
            terms = await cursor.fetchall()
            blacklisted_terms = [i[0] for i in terms if i[0] != None]

        return blacklisted_terms


    async def identifyWebhook(self, channel_id):

        channel = self.bot.get_channel(channel_id)
        whooks = await channel.webhooks()

        for i in whooks:
            if i.name == "Zoomer Influencers":
                return i.url


        async with aiohttp.ClientSession() as cs:
            async with cs.get(str(self.bot.user.avatar_url)) as r:
                image_bytes = await r.read()

        web = await channel.create_webhook(name="Zoomer Influencers", avatar=image_bytes, reason="Jay Bot")
        return web.url


    @commands.Cog.listener()
    async def on_message(self, message):

        if not message.embeds:
            return

        if message.channel.id != self.input_channel:
            return

        input_embed = message.embeds[0]


        description = input_embed.description if not str(input_embed.description) == 'Embed.Empty' else ""
        title = input_embed.title if not str(input_embed.title) == 'Embed.Empty' else ""
        author_name = input_embed.author.name if not str(input_embed.author.name) == 'Embed.Empty' else ""


        blacklisted_terms = await self.fetch_blacklist_data()

        for term in blacklisted_terms:
            if term in description or term in title or term in author_name:
                return

            for i in input_embed.fields:
                if term in i.name or term in i.value:
                    return



        whitelisted_terms = await self.fetch_whitelist_data()

        found = False

        if len(whitelisted_terms) != 0:

            for term in whitelisted_terms:
                if term in description or term in title or term in author_name:
                    found = True

                for i in input_embed.fields:
                    if term in i.name or term in i.value:
                        found = True

                if found:
                    break


            else:
                return


        input_embed.timestamp = discord.Embed.Empty
        input_embed.set_footer(text=discord.Embed.Empty, icon_url=discord.Embed.Empty)

        try:
            a_name = input_embed.author.name.split()[0]

        except AttributeError:
            a_name = ""

        input_embed.set_author(name=a_name, icon_url=input_embed.author.icon_url)

        whook = await self.identifyWebhook(self.output_channel)


        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(whook, adapter=AsyncWebhookAdapter(session))
            await webhook.send(embed=input_embed)







#Setup
def setup(bot):
    bot.add_cog(Events(bot))




