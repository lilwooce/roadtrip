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

mydb = mysql.connector.connect(
host=host,
user=usern,
password=passw,
database=db
)

cursor = mydb.cursor()

class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    async def prefix(self, ctx, new_prefix):
        sql = f"UPDATE prefixes SET prefix = {new_prefix} WHERE server = {str(ctx.message.guild.id)}"
        cursor.execute(sql)
        await ctx.send(f"Changed the prefix to: {new_prefix}")    

        

def setup(bot):
    bot.add_cog(Config(bot))