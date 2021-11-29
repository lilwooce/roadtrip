
from discord.ext import commands
import os
import requests
import discord 
from dotenv import load_dotenv
import youtube_dl
import asyncio

load_dotenv()
asurl = os.getenv("AS_URL")
rsurl = os.getenv("RS_URL")
geturl = os.getenv('GET_URL')
gpurl = os.getenv('GP_URL')

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   

def endSong(guild, path):
    os.remove(path)

class Roadtrip(commands.Cog, name="Roadtrip"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n----")

    @commands.command(aliases=['pl'])
    async def playlist(ctx, user=None):
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
    async def addplaylistsong(ctx, *song):
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
    async def removeplaylistsong(ctx, *song):
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
    async def startTrip(ctx):
        channel = ctx.message.author.voice.channel
        connected = ctx.author.voice
        if connected:
            await channel.connect()
            await ctx.channel.send("joined voice channel")

    @commands.command(aliases=['et'])
    async def endTrip(ctx):
        await ctx.voice_client.disconnect()
        await ctx.channel.send("left voice channel")

    '''@commands.command()
    async def play(ctx, url):
        channel = ctx.author.voice.channel

        if channel != None:
            await channel.connect()
            await ctx.channel.send("joined voice channel")
            
            try:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except:
                os.system(f"""youtube-dl -o "song.%(ext)s" --extract-audio -x --audio-format mp3 {url}""")

            channelName = channel.name
            vc = await channel.connect()
            await ctx.channel.send("joined voice channel")

            vc.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
            vc.source = discord.PCMVolumeTransformer(vc.source, 1)
                
            while vc.is_playing(): #waits until song ends
                await asyncio.sleep(1)
            else:
                await vc.disconnect() #and disconnects
                print("Disconnected")
        else:
            await ctx.send("Please join a voice channel")'''

    @commands.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['p'])
    async def play(ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music end or use the 'stop' command")
            return
        await ctx.send("Getting everything ready, playing audio soon")
        print("Someone wants to play music let me get that ready for them...")
        voice = ctx.author.voice
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')
        voice.play(discord.FFmpegPCMAudio("song.mp3"))
        voice.volume = 100
        voice.is_playing()

def setup(bot):
    bot.add_cog(Roadtrip(bot))