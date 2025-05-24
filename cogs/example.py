import config
from discord.ext import commands
from discord import app_commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name="ping", with_app_command=True, description="pong")
    @app_commands.guilds(*config.guilds)
    async def ping(self, ctx):
        await ctx.send(f"Pong! {round(self.client.latency * 1000)}ms")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith("yêu mều"):
            channel = message.channel
            await channel.send("Huh, really...?!")

            def check(m):
                return (
                    m.content == str("um")
                    and m.channel == channel
                    or m.content == str("Um")
                    and m.channel == channel
                    or m.content == str("Umm")
                    and m.channel == channel
                    or m.content == str("umm")
                    and m.channel == channel
                    or m.content == str("Uhm")
                    and m.channel == channel
                    or m.content == str("uhm")
                    and m.channel == channel
                    or m.content == str("yes")
                    and m.channel == channel
                    or m.content == str("Yes")
                    and m.channel == channel
                )

            msg = await self.client.wait_for("message", check=check)
            if (
                message.author.id == 470081764271063060
                or message.author.id == 315724989057990663
                or message.author.id == 213186434193031168
            ):

                await channel.send("Master, I love you! Huh".format(msg))
                # print('{.author.name},{.author.id}'.format(msg,msg))

            else:
                await channel.send("I only love my Master, not you!!")

        if message.content.lower().startswith("weitei mều"):
            channel = message.channel
            if message.author.id == 213186434193031168:
                await channel.send("Huh, who are you??")
            elif message.author.id == 470081764271063060:
                await channel.send("Master, don't put it too hard, neh")
            else:
                await channel.send("Ero Baka hentaiiiii")


async def setup(client):
    await client.add_cog(Example(client))
