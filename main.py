import discord, os, config, logging, asyncio
from discord.ext import commands

client = discord.Client()
client = commands.Bot(command_prefix=config.prefix, case_insensitive=True)
client.remove_command("help")

logging.basicConfig(
    handlers=[logging.FileHandler("./data/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


@client.command()
async def load(ctx, extension):
    if ctx.author.id in config.owners:
        try:
            client.load_extension(f"cogs.{extension}")
            await ctx.send("Loaded `" + extension + ".py`")
        except:
            await ctx.send("I can't find `" + extension + "`")


@client.command()
async def unload(ctx, extension):
    if ctx.author.id in config.owners:
        try:
            client.unload_extension(f"cogs.{extension}")
            await ctx.send("Unloaded `" + extension + ".py`")
        except:
            await ctx.send("I can't find `" + extension + "`")


@client.command()
async def reload(ctx, extension):
    if ctx.author.id in config.owners:
        try:
            client.reload_extension(f"cogs.{extension}")
            await ctx.send("Reloaded `" + extension + ".py`")
        except:
            await ctx.send("I can't find `" + extension + "`")


def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded {filename}")


load_cogs()


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game("Hi Boss!")
    )
    print("Logged in as {0} ({0.id})\nWelcome my Lord.".format(client.user))


# help command
class MinimalHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=config.embed_color)
            await destination.send(embed=emby)


client.help_command = MinimalHelpCommand()

client.run(config.token, reconnect=True, bot=True)
