import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="Requina", clour=discord.Color.red())

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/620646132124483594/620651554738929665/nqy3eee7abm01.jpg"
        )

        embed.add_field(
            name="r.help", value="See some commands in general", inline=False
        )
        embed.add_field(name="r.ping", value="Just a funny poke", inline=False)
        embed.add_field(name="r.avatar", value="Show your avatar", inline=False)
        embed.add_field(
            name="r.[emoji]",
            value="Show emoji. You can see the list by using r.emolist",
            inline=False,
        )
        embed.add_field(
            name="r.say [context]", value="Just one sentence, okey?", inline=False
        )
        embed.add_field(
            name="r.maid", value="Show you the perfect world <3", inline=False
        )
        embed.add_field(
            name="r.yuri",
            value="Welcome to the world of mystery :extreme_sexy_girl: ",
            inline=False,
        )
        embed.add_field(
            name="r.pic [tag 1],[tag 2]",
            value="Make MM do his/her job :))",
            inline=False,
        )
        embed.add_field(
            name="r.costume Requina", value="Am I kute, Master?", inline=False
        )
        embed.add_field(name="r.gif [name]", value="Shows a gif")
        embed.add_field(name="r.gif_add [name] [url]", value="Adds a gif")
        embed.add_field(name="r.gif_remove [name]", value="Removes a gif")
        embed.add_field(name="r.ran", value="Random a gif from list")

        await ctx.send(embed=embed)

    @commands.command()
    async def emolist(self, ctx):
        embed = discord.Embed(title="Requina", clour=discord.Color.red())

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/620646132124483594/620651554738929665/nqy3eee7abm01.jpg"
        )

        # embed.add_field(name="", value="", inline=False)
        embed.add_field(name="Emoji-Pepe", value="doubt, rope, whrope", inline=False)
        embed.add_field(name="Emoji-Requina", value="heh, hehe, wow", inline=False)
        embed.add_field(name="Emoji-KR", value="letsgo", inline=False)
        embed.add_field(
            name="Worry",
            value="<:WorryBuffLuck:697834453275377705> buffluck, <:WorryTachTachTach:697835039987073114> tach, <:WorryRip:697835039697666088> rip",
        )

        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Help(client))
