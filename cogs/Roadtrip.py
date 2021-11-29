
from discord.ext import commands
import os
import requests
import discord 
from dotenv import load_dotenv
import youtube_dl
import asyncio
from discord.utils import get

load_dotenv()
asurl = os.getenv("AS_URL")
rsurl = os.getenv("RS_URL")
geturl = os.getenv('GET_URL')
gpurl = os.getenv('GP_URL')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

def endSong(guild, path):
    os.remove(path)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Roadtrip(commands.Cog, name="Roadtrip"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command(aliases=['pl'])
    async def playlist(self, ctx, user=None):
        if user == None:
            user = ctx.author.id
        
        print(user)
        r = requests.get(gpurl, params={"user": user}, headers={"User-Agent": "XY"});
        result = r.json()
        embed = discord.Embed(title=f"{ctx.author.name}'s Playlist", description=f' ')
        counter = 1
        for x in range(len(result)):
            s = result[x]['song'].strip("\'")
            embed.add_field(name=f"{counter} {s}", value='\u200b', inline=False)
            embed.add_field(name=f"{counter} {s}", value='\u200b', inline=False)
            counter += 1
        await ctx.channel.send(embed=embed)
            

    @commands.command(aliases=["aps"])
    async def addplaylistsong(self, ctx, *song):
        if (len(ctx.message.content) > 1024):
            await ctx.channel.send("Too long")
            return
        try:
            fullsong = ""
            songLength = len(song)
            if (len(song) > 1):
                for x in range(songLength):
                    if (x!=songLength-1):
                        fullsong += f"{song[x]} "
                    else:
                        fullsong += song[x]
            else:
                fullsong = song[0]
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
            fullsong = ""
            songLength = len(song)
            if (len(song) > 1):
                for x in range(songLength):
                    if (x!=songLength-1):
                        fullsong += f"{song[x]} "
                    else:
                        fullsong += song[x]
            else:
                fullsong = song[0]
            obj = {"q1": ctx.author.id, "q2": fullsong}
            print(obj)
            result = requests.post(rsurl, data=obj, headers={"User-Agent": "XY"})
            print(result.status_code)
            print(result.url)
            print(result.text)
            await ctx.channel.send(f"Removed {fullsong} from {ctx.author.name}'s playlist")
        except:
            await ctx.channel.send("Please input a valid song")

    @commands.command(aliases=['st'])
    async def startTrip(self, ctx):
        channel = ctx.message.author.voice.channel
        connected = ctx.author.voice
        if connected:
            await channel.connect()
            await ctx.channel.send("joined voice channel")

    @commands.command(aliases=['et'])
    async def endTrip(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.channel.send("left voice channel")

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    '''@commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')'''

    '''@commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {query}')'''

    @commands.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['p', 'play'])
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await ctx.send(f'Now playing: {player.title}')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    '''@play.before_invoke
    @yt.before_invoke'''
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @stream.before_invoke
    async def banGrace(self, ctx):
        if (ctx.author == 347162620996091904):
            return

def setup(bot):
    bot.add_cog(Roadtrip(bot))