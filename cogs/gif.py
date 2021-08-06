import discord
import json
import random
from fuzzywuzzy import process
from discord.ext import commands

client = discord.Client()

class Gif(commands.Cog):

	def __int__(client):
		self.client = client

	@commands.command()
	async def gif(self, ctx, *, gname:str=None):

		with open('./data/gif.json', 'r') as f:
			gif = json.load(f)

		if gname is None:
			gif2 = json.dumps(gif, indent=2)

			embed = discord.Embed(title='List of Gifs',
								  description=f"{str(gif2)[1:][:-1]}")

			await ctx.send(embed=embed)

		else:
			ls = []
			gifn = gname.lower()
			for name in gif:
				ls.append(name)
			ext = process.extractOne(gifn, ls)

			if ext[-1] >= 50:

				name = gif[(str(ext[0]))]
				await ctx.send(f"{str(ext[0])}\n{str(name)}")

			else:
				await ctx.send('No gif found')

	@commands.command(aliases=['random'])
	async def ran(self, ctx):

		with open('./data/gif.json', 'r') as f:
			gif = json.load(f)

		rand = str(random.choice(list(gif.items())))

		await ctx.send(str(rand[1:][:-1].translate({ord(i): None for i in "',"})))

	@commands.command()
	async def gif_add(self, ctx, gname:str=None, gurl:str=None):
		if ctx.author.id == 315724989057990663 or ctx.author.id == 213186434193031168 or ctx.author.id == 470081764271063060:

			with open('./data/gif.json', 'r') as f:
				gif = json.load(f)

			if gname is not None and gurl is not None:
				gif[str(gname)] = str(gurl)

				with open('./data/gif.json', 'w') as f:
					json.dump(gif, f, indent=4)

				await ctx.send('Added Successful')

			elif gname is None and gurl is None:
				await ctx.send('Which gif you want to add ?\nHere is syntax: `r.gif_add [name] [url]`')

			else:
				pass
		else:
			await ctx.send("You don't have enough Permission(s) to use this command.")

	@commands.command()
	async def gif_remove(self, ctx, gname:str=None):
		if ctx.author.id == 315724989057990663 or ctx.author.id == 213186434193031168 or ctx.author.id == 470081764271063060:

			with open('./data/gif.json', 'r') as f:
				gif = json.load(f)

			if gname is not None:
				
				gif.pop(str(gname))

				with open('./data/gif.json', 'w') as f:
					json.dump(gif, f, indent=4)

				await ctx.send('Removed Successful')

			elif gname is None:
				await ctx.send('Which gif you want to remove ?\nHere is syntax: `r.gif_remove [name] [url]`')

			else:
				pass
		else:
			await ctx.send("You don't have enough Permission(s) to use this command.")

	@gif.error
	async def gif_error(self, ctx, error):
		if isinstance(error, commands.CommandInvokeError):
			await ctx.send("No gif found")
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Missing Argument Error")
	@gif_add.error
	async def gif_add_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("You don't have enough Permission(s) to use this command.")
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Missing Argument Error")

	@gif_remove.error
	async def gif_remove_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("You don't have enough Permission(s) to use this command.")
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send("Missing Argument Error")

def setup(client):
	client.add_cog(Gif(client))
