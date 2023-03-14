import random
import discord
from discord.ext import commands
from discord import app_commands


class Picture(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["picture"])
    async def pic(self, ctx, tags: str):
        try:
            tag1, tag2 = map(str, tags.split(","))
        except Exception:
            tag3 = tags
            await ctx.send("m.danbooru --tags= {}".format(tag3))

            # await ctx.send("Pls type ',' between tags.")
            # return
        if tag1 == "e":
            await ctx.send("m.danbooru --tags= {} --rating= e".format(tag2))
        elif tag2 == "e":
            await ctx.send("m.danbooru --tags= {} --rating= e".format(tag1))
        else:
            await ctx.send("m.danbooru --tags= {} {}".format(tag1, tag2))

    @commands.command()
    async def maid(self, ctx, file: str = None):
        if file is not None:
            if file == "file":
                await ctx.send(file=discord.File(fp="./data/maid.txt"))
        else:
            with open("./data/maid.txt", "r") as f:
                re = f.readlines()
                embed = discord.Embed(title="Maid")
                embed.set_image(url=str(random.choice(re)))
                await ctx.send(embed=embed)

    @commands.command()
    async def yuri(self, ctx, file: str = None):
        if file is not None:
            if file == "file":
                await ctx.send(file=discord.File(fp="./data/yuri.txt"))
        else:
            with open("./data/yuri.txt", "r") as f:
                re = f.readlines()
                embed = discord.Embed(title="Yuri")
                embed.set_image(url=str(random.choice(re)))
                await ctx.send(embed=embed)

    @commands.command()
    async def remilia(self, ctx, file: str = None):
        if file is not None:
            if file == "file":
                await ctx.send(file=discord.File(fp="./data/remilia.txt"))
        else:
            with open("./data/remilia.txt", "r") as f:
                re = f.readlines()
                embed = discord.Embed(title="Remilia")
                embed.set_image(url=str(random.choice(re)))
                await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx, *, option=None):
        if option is not None:
            if str(option) == "file":
                await ctx.send(file=discord.File(fp="./data/kiss.txt"))
            else:
                if option.startswith("<@"):
                    user = (
                        (option.replace("<", "").replace(">", "")).replace("@", "")
                    ).replace("!", "")
                    usr = await self.client.fetch_user(int(user))
                    name = usr.name
                else:
                    name = option
                with open("./data/kiss.txt", "r") as f:
                    re = f.readlines()
                    if str(option).endswith(" last"):
                        embed = discord.Embed(
                            title=f"`{name[:-5]}` you have been kissed by `{ctx.author.name}`"
                        )
                        embed.set_image(url=re[-1])
                    else:
                        embed = discord.Embed(
                            title=f"`{name}` you have been kissed by `{ctx.author.name}`"
                        )
                        embed.set_image(url=str(random.choice(re)))
                    await ctx.send(embed=embed)
        else:
            await ctx.send("Who do you want to kiss?")

    @commands.command()
    async def randomart(self, ctx):
        embed = discord.Embed(title="Random", color=config.embed_color)

        raart = [
            "https://cdn.discordapp.com/attachments/522649121933230100/533635120565846026/image0.jpg",
            "https://cdn.discordapp.com/attachments/522649121933230100/533635135145508864/image0.jpg",
        ]
        utl = random.choice(raart)
        embed.set_image(url=utl)
        await ctx.send(embed=embed)

    @commands.command()
    async def mmyuri(self, ctx):
        await ctx.send("m.danbooru --tags= yuri")

    @commands.command()
    async def mmyuri18(self, ctx):
        await ctx.send("m.danbooru --tags= yuri --rating= e")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.client.user.id:
            return
        chan = msg.channel
        if str(chan.name.lower()) == "maid":
            await self.add(msg, "maid")
        elif str(chan.name.lower()) == "yuri":
            await self.add(msg, "yuri")
        elif str(chan.name.lower()) == "remilia":
            await self.add(msg, "remilia")
        elif str(chan.name.lower()) == "kiss":
            await self.add(msg, "kiss")
        else:
            pass

    async def add(self, msg, gen: str):
        chan = msg.channel
        with open(f"./data/{gen}.txt", "r+") as f:
            re = f.read()
            count = 0
            if msg.attachments:
                attachments = msg.attachments
                for img in attachments:
                    count += 1
                    pt = img.url
                    if pt not in re:
                        f.write(pt + "\n")
                await chan.send(f"added {count} pic(s)")
            elif msg.content.startswith("http"):
                attachments = msg.content
                if attachments not in re:
                    f.write(attachments + "\n")
                await chan.send("added")
            else:
                pass


async def setup(client):
    await client.add_cog(Picture(client))
