import discord
from discord.ext import commands
import os
import asyncio


class Error(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if (
            isinstance(error, commands.CommandNotFound)
            or isinstance(error, commands.CommandInvokeError)
            or isinstance(error, commands.errors.BadArgument)
        ):
            pass

        elif isinstance(error, commands.CheckFailure):
            await ctx.send(
                "You don't have the permission to use that command. <:broken:652813264778166278>"
            )

        elif isinstance(error, commands.errors.CommandOnCooldown):
            msg = await ctx.send(f"{error}")
            await ctx.message.delete()
            await asyncio.sleep(5)
            await msg.delete()
        else:
            raise error


async def setup(client):
    await client.add_cog(Error(client))
