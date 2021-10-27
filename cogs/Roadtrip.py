from discord.ext import commands
import json
import os
import mysql.connector
import discord 
from dotenv import load_dotenv

class Roadtrip(commands.Cog, name="Roadtrip"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

def setup(bot):
    bot.add_cog(Roadtrip(bot))