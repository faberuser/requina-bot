import discord, config
from discord.ext import commands
from discord import app_commands


class Executor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ban(self, ctx, member: discord.Member = None):       
        if member is None:
            await ctx.send("Please provide a member to ban and purge their latest messages")
            return
         
        # check if the user is the guild owner
        if ctx.author != ctx.guild.owner:
            await ctx.send("You do not have permission to ban")
            return
        
        # purge message
        await self.purge_message(ctx, member)
        
        # ban the member
        await member.ban()
        await ctx.send(f"{member} has been banned and their latest messages have been purged")

    @commands.command()
    async def purge(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("Please provide a member to purge their latest messages")
            return
        
        # check if the user is the guild owner
        if ctx.author != ctx.guild.owner:
            await ctx.send("You do not have permission to purge")
            return
        
        # purge message
        await self.purge_message(ctx, member)
    
    async def purge_message(self, ctx, member: discord.Member):
        # loop through the channels in the guild
        for channel in ctx.guild.channels:
            # loop through first 100 msgs in the channel
            async for message in channel.history(limit=100):
                # if the message author is the member to ban
                if message.author == member:
                    # delete the message
                    await message.delete()
                    continue
        await ctx.send(f"Messages from {member} have been purged")

async def setup(client):
    await client.add_cog(Executor(client))
