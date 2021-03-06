import discord
import os
import sys
import requests
import traceback
from discord.ext import commands
from dotenv import load_dotenv

def get_prefix(client, message):
    obj = {"f1": "server", "q1": message.guild.id}
    result = requests.get(geturl, params=obj, headers={"User-Agent": "XY"})
    prefix = result.text.strip('\"')
    return prefix

load_dotenv()   
insertPURL = os.getenv('IP_URL')
deletePURL = os.getenv('DP_URL')
geturl = os.getenv('GET_URL')
token = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents, description=f"Listen to music on a roadtrip")

initial_extensions = {
    "cogs.Config",
    "cogs.Roadtrip"
}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    activity = discord.Game(name=f"!help")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_guild_join(guild):
    obj = {"f1": guild.id, "q1": '!'}
    result = requests.post(insertPURL, data=obj, headers={"User-Agent": "XY"})
    print(result.status_code)

@bot.event
async def on_guild_remove(guild):
    obj = {"q1": guild.id}
    result = requests.post(deletePURL, data=obj, headers={"User-Agent": "XY"})
    print(result.status_code)

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

bot.run(token)