from pathlib import Path
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



class MusicBot(commands.Bot):
    def __init__(self):
        self._cogs = [p.stem for p in Path(".").glob("./bot/cogs/*.py")]
        super().__init__(command_prefix=get_prefix, case_insensitive=True)
        activity = discord.Game(name=f"!help")
        self.change_presence(status=discord.Status.online, activity=activity)

    def setup(self):
        print("Running setup...")

        for cog in self._cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")

        print("Setup complete.")

    def run(self):
        self.setup()
        print("Running bot...")
        super().run(token, reconnect=True)

    async def shutdown(self):
        print("Closing connection to Discord...")
        await super().close()

    async def close(self):
        print("Closing on keyboard interrupt...")
        await self.shutdown()

    async def on_connect(self):
        print(f" Connected to Discord (latency: {self.latency*1000:,.0f} ms).")

    async def on_resumed(self):
        print("Bot resumed.")

    async def on_disconnect(self):
        print("Bot disconnected.")

    async def on_error(self, err, *args, **kwargs):
        raise

    async def on_command_error(self, ctx, exc):
        raise getattr(exc, "original", exc)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Bot ready.")

    async def prefix(self, bot, msg):
        return commands.when_mentioned_or("+")(bot, msg)

    async def process_commands(self, msg):
        ctx = await self.get_context(msg, cls=commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)