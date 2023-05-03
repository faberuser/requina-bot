import discord, asyncio, aiohttp, config
from discord.ext import commands
from discord import app_commands
from cogs import sauce


class Embed(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(
        name="about", with_app_command=True, description="about myself"
    )
    @app_commands.guilds(*config.guilds)
    async def about(self, ctx):
        embed = discord.Embed(
            title="Requina",
            description="Merchant of Poison",
            color=config.embed_color,
            url="https://www.google.com",
        )

        # embed.set_author(name=self.client.user.name, icon_url=self.client.user.display_avatar.url)
        embed.set_footer(text=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        # embed.set_image(url="https://cdn.discordapp.com/attachments/522649121933230100/525874173940203541/1545425605019.png")
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/620646132124483594/620651554738929665/nqy3eee7abm01.jpg"
        )

        embed.add_field(name="Class", value="Archer")
        embed.add_field(name="Role", value="Sub-dps")

        embed.add_field(name="Attack Type", value="Physical")
        embed.add_field(name="Position", value="Middle")

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name="avatar", with_app_command=True, description="show someone avatar"
    )
    @app_commands.guilds(*config.guilds)
    async def avatar(self, ctx, member: discord.Member = None):
        if member is not None:
            au = member
        if member is None:
            au = ctx.author
        url_ = au.display_avatar.url
        embed = discord.Embed(title=f"{au}")
        embed.set_image(url=url_)
        embed.set_footer(
            text=f"Requested by: {ctx.author} | Hit the below emoji to find sauce of this image.",
            icon_url=ctx.author.display_avatar.url,
        )
        msg = await ctx.send(embed=embed)
        emo = "🇸"
        await msg.add_reaction(emo)

        def check_(reaction, user):
            return user == ctx.author and reaction.emoji in emo

        try:
            reaction, user = await self.client.wait_for(
                "reaction_add", timeout=5.0, check=check_
            )
            if str(reaction.emoji) in emo:
                await msg.clear_reactions()
                await msg.edit(embed=sauce.Sauce(self.client).searching_embed(embed))
                sauce_embed_ = await sauce.Sauce(self.client).sauce_embed(embed)
                await msg.edit(embed=sauce_embed_)
        except asyncio.TimeoutError:
            await msg.clear_reactions()
            timeout_embed_ = sauce.Sauce(self.client).timeout_embed(embed)
            await msg.edit(embed=timeout_embed_)


async def setup(client):
    await client.add_cog(Embed(client))
