import discord, os
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
        if ctx.author.id != 417983447488004097:
            return
        for file in os.listdir('./hololive chill/Midnight'):
            if file.endswith('.mp3'):
                self.queue.append((discord.FFmpegPCMAudio(f'./hololive chill/Midnight/{file}'), file[:-4]))
        for file in os.listdir('./hololive chill/Sunshine'):
            if file.endswith('.mp3'):
                self.queue.append((discord.FFmpegPCMAudio(f'./hololive chill/Sunshine/{file}'), file[:-4]))
        if self.channel == None:
            try:
                self.channel = channel
                voice_channel = self.client.get_channel(self.channel)
                self.player = await voice_channel.connect(reconnect=True)
            except:
                pass
        else:
            try:
                self.channel = channel
                voice_channel = self.client.get_channel(self.channel)
                self.player = self.client.move_to(voice_channel)
            except:
                pass
        queue = cycle(self.queue)
        playing = next(queue)
        self.player.play(playing[0])
        await voice_channel.edit(name=f"{playing[1]} - Hololive Chill (24/7)")
        while True:
            if self.player.is_playing():
                await sleep(3)
                continue
            playing = next(queue)
            self.player.play(playing[0])
            await voice_channel.edit(name=f"{playing[1]} - Hololive Chill (24/7)")

    @commands.command()
    async def hololive_end(self, ctx):
        if ctx.author.id != 417983447488004097:
            return
        await self.player.disconnect(force=True)
        self.queue = []
        self.player = None

def setup(client):
    client.add_cog(Hololive(client))