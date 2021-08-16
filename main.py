import discord, os, threading, config, logging, asyncio
from discord.ext import commands
from cogs import give_away
from discord_slash import SlashCommand

client = commands.Bot(command_prefix=config.prefix, case_insensitive=True)
client.remove_command('help')
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True, delete_from_unused_guilds=True)

logging.basicConfig(
    handlers=[logging.FileHandler("./data/log.log", "a", "utf-8")],
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
)

@client.command()
async def load(ctx, extension):
    if ctx.author.id == 470081764271063060 or ctx.author.id == 315724989057990663:
        try:
            client.load_extension(f'cogs.{extension}')
            await ctx.send('Loaded `' + extension + '.py`')
        except:
            await ctx.send("I can't find `" + extension + '`')

@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 470081764271063060 or ctx.author.id == 315724989057990663:
        try:
            client.unload_extension(f'cogs.{extension}')
            await ctx.send('Unloaded `' + extension + '.py`')
        except:
            await ctx.send("I can't find `" + extension + '`')

@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 470081764271063060 or ctx.author.id == 315724989057990663:
        try:
            client.reload_extension(f'cogs.{extension}')
            await ctx.send('Reloaded `' + extension + '.py`')
        except:
            await ctx.send("I can't find `" + extension + '`')

def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename == '__init__.py':
            continue
        elif filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded {filename}')

load_cogs()

@client.event
async def on_ready():
    load_cogs()
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Hi Boss!"))
    print('[main.py] Logged in as {0} ({0.id})\nWelcome my Lord.'.format(client.user))
    asyncio.create_task(hololive_playper.Hololive(client).hololive_())

check_ga = give_away.Giveaway(discord.Client()).execute
thread = threading.Thread(target=check_ga, args=('check_ga', ))
thread.name = 'check_ga'
thread.daemon = True
thread.start()

client.run(config.token, reconnect=True, bot=True)
