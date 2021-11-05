from discord.ext import commands
import os
import requests
import discord 
from dotenv import load_dotenv

load_dotenv()
asurl = os.getenv("AS_URL")
rsurl = os.getenv("RS_URL")
geturl = os.getenv('GET_URL')

class Roadtrip(commands.Cog, name="Roadtrip"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command(aliases=["aps"])
    async def addplaylistsong(self, ctx, *song):
        if (len(ctx.message.content) > 1024):
            await ctx.channel.send("Too long")
            return
        try:
            fullsong=""
            count = 0
            for word in song:
                if count > 0:
                    fullsong += f"{word} "
                else:
                    fullsong += word
            obj = {"q1": ctx.author.id, "q2": fullsong}
            print(obj)
            result = requests.post(asurl, data=obj, headers={"User-Agent": "XY"})
            print(result.status_code)
            print(result.url)
            print(result.text)
            await ctx.channel.send(f"Added {fullsong} to {ctx.author.name}'s playlist")
        except:
            await ctx.channel.send("Please input a valid song")

    @commands.command(aliases=["rps"])
    async def removeplaylistsong(self, ctx, *song):
        if (len(ctx.message.content) > 1024):
            await ctx.channel.send("Too long")
            return
        try:
            fullsong=""
            for word in song:
                fullsong += f"{word} "
            obj = {"q1": ctx.author.id, "q2": fullsong}
            print(obj)
            result = requests.post(rsurl, data=obj, headers={"User-Agent": "XY"})
            print(result.status_code)
            print(result.url)
            print(result.text)
            await ctx.channel.send(f"Removed {fullsong} from {ctx.author.name}'s playlist")
        except:
            await ctx.channel.send("Please input a valid song")

def setup(bot):
    bot.add_cog(Roadtrip(bot))