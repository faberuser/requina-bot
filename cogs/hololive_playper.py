import discord, os, config
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

    @commands.command()
    async def hololive(self, ctx, channel:int):
        if ctx.author.id not in config.owners:
            return
        midnight = []
        for file in os.listdir('./hololive chill/Midnight'):
            if file.endswith('.mp3'):
                midnight.append((f'./hololive chill/Midnight/{file}', file[:-4]))
        midnight.sort()
        sunshine = []
        for file in os.listdir('./hololive chill/Sunshine'):
            if file.endswith('.mp3'):
                sunshine.append((f'./hololive chill/Sunshine/{file}', file[:-4]))
        sunshin.sort()
        for music in midnight:
            self.queue.append((discord.FFmpegPCMAudio(music[0]), music[1]))
        if self.channel == None:
            try:
                self.channel = channel
                voice_channel = self.client.get_channel(channel)
                self.player = await voice_channel.connect(reconnect=True)
            except:
                pass
        else:
            try:
                self.channel = channel
                voice_channel = self.client.get_channel(channel)
                self.player = await self.client.move_to(voice_channel)
            except:
                pass
        queue = cycle(self.queue)
        while True:
            if self.player == None:
                try:
                    await self.player.disconnect(force=True)
                except:
                    pass
                break
            if self.player.is_playing():
                await sleep(3)
                continue
            playing = next(queue)
            self.player.play(playing[0])
            try:
                await voice_channel.edit(name=f"{playing[1]} - Hololive Chill (24/7)")
            except:
                pass

    @commands.command()
    async def hololive_end(self, ctx):
        if ctx.author.id not in config.owners:
            return
        if self.player == None:
            return
        await self.player.disconnect(force=True)
        self.queue = []
        self.player = None

def setup(client):
    client.add_cog(Hololive(client))