import discord
from discord.ext import commands

client = discord.Client()

class Clear(commands.Cog):

	def __init__(self, client):
		self.client = client

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def clear(self, ctx, amount:int):
		def bot_msg(m):
			return m.author == client.user

		await ctx.channel.purge(limit=amount, check=bot_msg)

def setup(client):
	client.add_cog(Clear(client))