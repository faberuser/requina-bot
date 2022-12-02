import discord
import random
from discord.ext import commands

class Say(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliase=["echo"])
    async def clr(self, ctx, amount):
        if ctx.author.name =="Kuroneko" and ctx.author.id == 470081764271063060:
            await  ctx.channel.purge(limit= int(amount))
        else:
            await ctx.send("You're not my Master, how dare you!??")
            return

    @commands.command(aliase=["echo"])
    async def say(self, ctx, *, words):
        if "@everyone" in words:
            await  ctx.send("Stupid Boss. Do that again and I won't love you anymore!")
        else:
            await  ctx.channel.purge(limit=1)
            await  ctx.send(words)

    @commands.command()
    async def heyR(self, ctx, *, question):
        responses = ['I-I-Its not like I like you or anything! B-baka!', 'Huh, Bakaaaaa!', 'I - Love - U!!',
                    'I hate u', 'Become my servant now, he he he', 'Want to drink my new poison?', 'I only love my Master, not you.']

        await ctx.send(f'{random.choice(responses)}')

async def setup(client):
    await client.add_cog(Say(client))