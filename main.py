import os
import logging
from dotenv import load_dotenv
import config
import discord
from discord.ext import commands
from discord import app_commands

load_dotenv()
logging.basicConfig(
    handlers=[logging.FileHandler("./data/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)


class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=config.prefix, case_insensitive=True, intents=intents
        )

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                await client.load_extension(f"cogs.{filename[:-3]}")
                print(f"Loaded {filename}")
        for guild in config.guilds:
            try:
                await self.tree.sync(guild=discord.Object(id=guild))
            except:
                print(str(guild) + " is not synced")
        print(f"Synced slash commands for {self.user}.")


client = Client()
client.remove_command("help")
# help command
class MinimalHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, colour=config.embed_color)
            await destination.send(embed=embed)


client.help_command = MinimalHelpCommand()


@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle, activity=discord.Game("Hi Boss!")
    )
    print("Logged in as {0} ({0.id})\nWelcome my Lord.".format(client.user))


client.run(os.getenv('DISCORD_TOKEN'), reconnect=True)
