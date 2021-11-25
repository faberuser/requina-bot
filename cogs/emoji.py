import discord
import random
from discord.ext import commands

client = discord.Client()

class Emoji(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fk(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send("<:fk:628969759182028800> ")
        await ctx.send("\"phắc du!!\"")

    @commands.command()
    async def letsgo(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:letsgo:525666754626715688> ")

    @commands.command()
    async def doubt(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:doubt:623894511621505034> ")

    @commands.command()
    async def whrope(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:whrope:624886064393355264> ")

    @commands.command()
    async def rope(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:rope:624885593024757801> ")

    @commands.command()
    async def heh(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:heh:624905856483328002> ")

    @commands.command()
    async def hehe(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:hehe:624905967749955595> ")

    @commands.command()
    async def wow(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:wow:624906006496804904> ")

    @commands.command()
    async def stare(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:stare:624993223420542976> ")

    @commands.command(aliases=['buff'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def buffluck(self, ctx, *, guy):
        if guy:
            await ctx.send(f"{guy} <:WorryBuffLuck:697834453275377705> *Luck is increased by {random.choice(['', '-'])}{random.randrange(1,100,1)}%*")
        else:
            await ctx.send('Who ?')

    @commands.command(aliases=['debuff', 'tach', 'neft', 'neftluck', 'nerf', 'nerfluck'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def debuffluck(self, ctx, *, guy):
        if guy:
            await ctx.send(f'<:WorryTachTachTach:697835039987073114> {guy} *Luck is decreased by {random.randrange(1,101,1)}%*')
        else:
            await ctx.send('Who ?')

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rip(self, ctx, *, guy):
        await ctx.send(f'<:WorryRip:697835039697666088> {guy}')

def setup(client):
    client.add_cog(Emoji(client))