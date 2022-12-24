import discord
from discord.ext import commands
import os
import asyncio


class SaucyBot_Handler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 647368715742216193:  # SaucyBot
            if message.reference:
                await message.add_reaction("🗑️")
                rf = await message.channel.fetch_message(message.reference.message_id)

                def check(reaction, user):
                    return user == rf.author and str(reaction.emoji) == "🗑️"

                try:
                    reaction, user = await self.client.wait_for(
                        "reaction_add", timeout=60.0, check=check
                    )
                    await message.delete()
                except asyncio.TimeoutError:
                    await message.clear_reactions()


async def setup(client):
    await client.add_cog(SaucyBot_Handler(client))
