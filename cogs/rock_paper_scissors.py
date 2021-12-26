import discord, asyncio
from discord.ext import commands
from random import choice

from discord_slash.utils.manage_components import create_button, wait_for_component, create_actionrow, spread_to_rows
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext, SlashContext


class Rock_Paper_Scissors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @cog_ext.cog_slash(name='rpc',
                    description="Play Rock Paper Scissors with another member",
                    guild_ids=[652813007981772801, 213557352782233601],
                    options=[
                        create_option(name='member', description='Inpput a member', option_type=6, required=True)
                    ]) # slash ut 4 command
    async def rpc_(self, ctx: SlashContext, *, member: discord.Member):
        author_re = None
        member_re = None
        embed = discord.Embed(title='waiting for reaction...', description=f"{ctx.author.name}: ???\n{member.name}: ???")
        if ctx.author == member:
            embed = discord.Embed(title='oops, you played yourself', description=f"so it's a draw right ?")
            msg = await ctx.send(embed=embed)
            return
        elif member.bot == True:
            embed = discord.Embed(title='can bot even play rock paper scissors ?')
            if member.id == self.client.user.id:
                lst = [
                    discord.Embed(title='i always win', description=f"{ctx.author.name}: rock\n{self.client.user.name}: paper"),
                    discord.Embed(title='i always win', description=f"{ctx.author.name}: paper\n{self.client.user.name}: scissors"),
                    discord.Embed(title='i always win', description=f"{ctx.author.name}: scissors\n{self.client.user.name}: rock"),
                ]
                embed = choice(lst)
            await ctx.send(embed=embed)
            return

        buttons = [
            create_button(style=ButtonStyle.blue, label="\u270A"), # rock
            create_button(style=ButtonStyle.red, label="\u270B"), # paper
            create_button(style=ButtonStyle.green, label="\u270C"), # scissors
            ]
        button_row = create_actionrow(*buttons)
        action_rows = [button_row]

        msg = await ctx.send(embed=embed, components=action_rows)

        def all_reacted():
            re = None
            if author_re != None and member_re != None:
                if author_re == 'rock': # author: rock
                    if member_re == 'rock':
                        re = 'draw'
                    elif member_re == 'paper':
                        re = 'member'
                    else:
                        re = 'author'
                elif author_re == 'paper': # author: paper
                    if member_re == 'rock':
                        re = 'author'
                    elif member_re == 'paper':
                        re = 'draw'
                    else:
                        re = 'member'
                else: # author: scissors
                    if member_re == 'rock':
                        re = 'member'
                    elif member_re == 'paper':
                        re = 'author'
                    else:
                        re = 'draw'
            return re

        break_ = False
        while True:
            try:
                interactions: ComponentContext = await wait_for_component(self.client, components=action_rows, timeout=120.0, check=lambda x: x.author_id == ctx.author.id or x.author_id == member.id)
                if interactions.author_id == ctx.author.id:
                    if interactions.component['label'] == '\u270A': # rock
                        author_re = 'rock'
                    elif interactions.component['label'] == '\u270B': # paper
                        author_re = 'paper'
                    else: # scissors
                        author_re = 'scissors'
                elif interactions.author_id == member.id:
                    if interactions.component['label'] == '\u270A': # rock
                        member_re = 'rock'
                    elif interactions.component['label'] == '\u270B': # paper
                        member_re = 'paper'
                    else: # scissors
                        member_re = 'scissors'
                if author_re != None:
                    embed_ = discord.Embed(title='waiting for reaction...', description=f"{ctx.author.name}: reacted\n{member.name}: ???")
                elif member_re != None:
                    embed_ = discord.Embed(title='waiting for reaction...', description=f"{ctx.author.name}: ???\n{member.name}: reacted")
                re = all_reacted()
                if re != None:
                    break_ = True
                    if re == 'author':
                        embed_ = discord.Embed(title=f"{ctx.author.name} win", description=f"{ctx.author.name}: {author_re}\n{member.name}: {member_re}")
                    elif re == 'member':
                        embed_ = discord.Embed(title=f"{member.name} win", description=f"{ctx.author.name}: {author_re}\n{member.name}: {member_re}")
                    else:
                        embed_ = discord.Embed(title="draw", description=f"{ctx.author.name}: {author_re}\n{member.name}: {member_re}")
                await interactions.edit_origin(embed=embed_)
                if break_ == True:
                    buttons = []
                    for row in msg.components:
                        for button in row['components']:
                            button['disabled'] = True
                            buttons.append(button)
                    action_row = spread_to_rows(*buttons, max_in_row=5)
                    await msg.edit(components=action_row)
                    break
            except asyncio.TimeoutError:
                embed_ = discord.Embed(title='timeout', description=embed.description)
                buttons = []
                for row in msg.components:
                    for button in row['components']:
                        button['disabled'] = True
                        buttons.append(button)
                action_row = spread_to_rows(*buttons, max_in_row=5)
                await msg.edit(embed=embed_, components=action_row)
                break


def setup(client):
    client.add_cog(Rock_Paper_Scissors(client))