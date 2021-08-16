import discord, os, config, traceback
from itertools import cycle
from asyncio import sleep
from discord.ext import commands

client = discord.Client()

class Hololive(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = []
        self.player = None
        self.channel = None
        self.options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
        }

    @commands.command() # 24/7 hololive chill music player
    async def hololive(self, ctx, channel:int=None):
        if ctx.author.id not in config.owners:
            return
        try:
            self.get_songs()
            # join voice channel
            if self.channel is None:
                if channel is None:
                    self.channel = ctx.author.voice.channel
                    voice_channel = ctx.author.voice.channel
                    self.player = await self.channel.connect(reconnect=True, timeout=30)
                else:
                    try:
                        voice_channel = self.client.get_channel(channel)
                        self.player = await voice_channel.connect(reconnect=True, timeout=30)
                        self.channel = channel
                    except:
                        try:
                            voice_channel = await self.client.fetch_channel(channel)
                            self.player = await voice_channel.connect(reconnect=True, timeout=30)
                            self.channel = channel
                        except:
                            guild = self.client.get_guild(ctx.author.guild.id)
                            voice_channel = guild.get_channel(channel)
                            self.player = await voice_channel.connect(reconnect=True, timeout=30)
                            self.channel = channel
            else:
                self.channel = channel
                try:
                    voice_channel = self.client.get_channel(channel)
                    self.player = await self.client.move_to(voice_channel)
                except:
                    voice_channel = await self.client.fetch_channel(channel)
                    self.player = await self.client.move_to(voice_channel)
            # loop music player
            await player(voice_channel, self.channel)
        except:
            traceback.print_exc()

    async def hololive_(self):
        try:
            self.get_songs()
            # join voice channel
            voice_channel = await self.connect(config.hololive_channel)
            self.channel = voice_channel
            # loop music player
            await player(voice_channel, config.hololive_channel)
        except:
            traceback.print_exc()

    async def player(self, voice_channel, channel):
        # loop music player
        voice_channel = voice_channel
        queue = cycle(self.queue)
        while True:
            if self.player == None or self.channel == None or self.queue == []:
                try:
                    await self.player.disconnect(force=True)
                except:
                    pass
                break
            if self.player.is_playing():
                await sleep(3)
                continue
            playing = next(queue)
            audio = discord.FFmpegPCMAudio(playing[0], options = self.options)
            try:
                await voice_channel.edit(name=f"{playing[1]} - Hololive Chill (24/7)")
            except:
                pass
            try:
                self.player.play(audio)
            except:
                voice_channel = await self.connect(channel)

    def get_songs(self):
        # get music songs path
        midnight = []
        for file in os.listdir('./hololive chill/Midnight'):
            if file.endswith('.mp3'):
                midnight.append((f'./hololive chill/Midnight/{file}', file[:-4]))
        midnight.sort()
        sunshine = []
        for file in os.listdir('./hololive chill/Sunshine'):
            if file.endswith('.mp3'):
                sunshine.append((f'./hololive chill/Sunshine/{file}', file[:-4]))
        sunshine.sort()

        # append to a public list
        for music in midnight:
            self.queue.append(music)
        for music in sunshine:
            self.queue.append(music)

    async def connect(self, channel:int):
        try:
            voice_channel = self.client.get_channel(channel)
            self.player = await voice_channel.connect(reconnect=True, timeout=30)
        except:
            try:
                voice_channel = await self.client.fetch_channel(channel)
                self.player = await voice_channel.connect(reconnect=True, timeout=30)
            except:
                try:
                    voice_channel = self.client.get_channel(channel)
                    self.player = await self.client.move_to(voice_channel)
                except:
                    voice_channel = await self.client.fetch_channel(channel)
                    self.player = await self.client.move_to(voice_channel)
        return voice_channel

    @commands.command()
    async def hololive_list(self, ctx):
        midnight = []
        for file in os.listdir('./hololive chill/Midnight'):
            if file.endswith('.mp3'):
                midnight.append(file[:-4])
        midnight.sort()
        sunshine = []
        for file in os.listdir('./hololive chill/Sunshine'):
            if file.endswith('.mp3'):
                sunshine.append(file[:-4])
        sunshine.sort()

        des = ''
        try:
            current = (ctx.author.voice.channel.name)[:-24]
            for music in midnight:
                if current == music:
                    des+=music+' **(Now playing)**'+'\n'
                else:
                    des+=music+'\n'
            for music in sunshine:
                if current == music:
                    des+=music+' **(Now playing)**'+'\n'
                else:
                    des+=music+'\n'
        except:
            for music in midnight:
                des+=music+'\n'
            for music in sunshine:
                des+=music+'\n'

        embed = discord.Embed(title='Hololive Chill Songs', description=des)
        await ctx.send(embed=embed)

    @commands.command() # end the player
    async def hololive_end(self, ctx):
        if ctx.author.id not in config.owners:
            return
        if self.player == None:
            return
        await self.player.disconnect(force=True)
        self.queue = []
        self.player = None
        self.channel = None

def setup(client):
    client.add_cog(Hololive(client))