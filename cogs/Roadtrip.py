from discord.ext import commands
import json
import os
import mysql.connector
import discord 
from dotenv import load_dotenv

load_dotenv()
host = os.getenv('DB_HOST')
usern = os.getenv('DB_USER')
passw = os.getenv('DB_PASS')
db = os.getenv("DB_NAME")

class Roadtrip(commands.Cog, name="Roadtrip"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command(aliases=["aps"])
    async def addplaylistsong(self, ctx, song):
        try:
            mydb = mysql.connector.connect(
            host=host,
            user=usern,
            password=passw,
            database=db
            )

            cursor = mydb.cursor()
            sql = f"INSERT INTO playlists (user, song) VALUE (%s, %s)"
            cursor.execute(sql, (ctx.author.id, song,))
            mydb.commit()
            await ctx.send(f"Added {song} to {ctx.author.name}'s playlist.")    
            mydb.close()
        except:
            await ctx.channel.send("Please input a valid song")

    @commands.command(aliases=["aps"])
    async def addplaylistsong(self, ctx, song):
        try:
            mydb = mysql.connector.connect(
            host=host,
            user=usern,
            password=passw,
            database=db
            )

            cursor = mydb.cursor()
            sql = f"DELETE FROM playlists WHERE user = %s AND song = %s"
            cursor.execute(sql, (ctx.author.id, song,))
            mydb.commit()
            await ctx.send(f"Removed {song} from {ctx.author.name}'s playlist.")    
            mydb.close()
        except:
            await ctx.channel.send("Please input a valid song")

def setup(bot):
    bot.add_cog(Roadtrip(bot))