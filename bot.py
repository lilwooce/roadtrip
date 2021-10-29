import discord
import os
import sys
import mysql.connector
import traceback
from discord.ext import commands
from dotenv import load_dotenv

def get_prefix(client, message):
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db,
        port=dbport
    )
    mydb.reconnect()
    cursor = mydb.cursor()
    sql = "SELECT prefix FROM prefixes WHERE server = %s"
    cursor.execute(sql, (message.guild.id,))
    result = cursor.fetchone()
    print(result)
    mydb.close()
    return result


load_dotenv()
host = os.getenv('DB_HOST')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
dbport = os.getenv('DB_PORT')
db = os.getenv("DB_NAME")
token = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix=get_prefix, description="Listen to music on a roadtrip")

initial_extensions = {
    "cogs.Config",
    "cogs.Roadtrip"
}


@bot.event
async def on_ready():
    print(f'{bot.user} has connected')
    activity = discord.Game(name="Driving Simulator")
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.event
async def on_guild_join(guild):
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db,
        port=dbport
    )
    cursor = mydb.cursor()
    sql = "INSERT INTO prefixes (server, Prefix) VALUES (%s, %s)"
    val = (str(guild.id), "!",)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()

@bot.event
async def on_guild_remove(guild):
    mydb = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db,
        port=dbport
    )
    cursor = mydb.cursor()
    sql = "DELETE FROM prefixes WHERE server = %s"
    cursor.execute(sql, (str(guild.id),))
    mydb.commit()
    mydb.close()


for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

bot.run(token)