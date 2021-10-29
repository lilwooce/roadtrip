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



class Config(commands.Cog, name="Configuration"):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command()
    async def prefix(self, ctx, new_prefix=None):
        if(new_prefix):
            mydb = mysql.connector.connect(
            host=host,
            user=usern,
            password=passw,
            database=db
            )

            cursor = mydb.cursor()
            sql = f"UPDATE prefixes SET prefix = (%s) WHERE server = (%s)"
            cursor.execute(sql, (new_prefix, ctx.message.guild.id,))
            mydb.commit()
            await ctx.send(f"Changed the prefix to: {new_prefix}")    
            mydb.close()
        else:
            await ctx.send("Please input a new prefix.")

        

def setup(bot):
    bot.add_cog(Config(bot))