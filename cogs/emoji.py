import discord, random, json, asyncio
from datetime import datetime
import datetime as dt
from discord.ext import commands

client = discord.Client()

class Emoji(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def fk(self, ctx):
        await ctx.channel.purge(limit=1)
        await ctx.send("<:fk:628969759182028800> ")
        await ctx.send("\"phắc du!!\"")

    @commands.command()
    async def letsgo(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:letsgo:525666754626715688> ")

    @commands.command()
    async def doubt(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:doubt:623894511621505034> ")

    @commands.command()
    async def whrope(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:whrope:624886064393355264> ")

    @commands.command()
    async def rope(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:rope:624885593024757801> ")

    @commands.command()
    async def heh(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:heh:624905856483328002> ")

    @commands.command()
    async def hehe(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:hehe:624905967749955595> ")

    @commands.command()
    async def wow(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:wow:624906006496804904> ")

    @commands.command()
    async def stare(self, ctx):
        await  ctx.channel.purge(limit=1)
        member = ctx.author
        await ctx.send('**{0.display_name}**'.format(member))
        await ctx.send("<:stare:624993223420542976> ")

    @commands.command(aliases=['buff'])
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def buffluck(self, ctx, *, guy):
        re = self.limit_check('./data/buff_limit.json', ctx.author.id, 'buff')
        if re == True:
            if guy:
                await ctx.send(f"{guy} <:WorryBuffLuck:697834453275377705> *Luck is increased by {random.choice(['', '-'])}{random.randrange(1,100,1)}%*")
            else:
                await ctx.send('Who ?')
        else:
            msg = await ctx.send(re)
            await ctx.message.delete()
            await asyncio.sleep(10)
            await msg.delete()

    @commands.command(aliases=['debuff', 'tach', 'neft', 'neftluck', 'nerf', 'nerfluck'])
    # @commands.cooldown(1, 60, commands.BucketType.user)
    async def debuffluck(self, ctx, *, guy):
        re = self.limit_check('./data/nerf_limit.json', ctx.author.id, 'nerf')
        if re == True:
            if guy:
                await ctx.send(f'<:WorryTachTachTach:697835039987073114> {guy} *Luck is decreased by {random.randrange(1,101,1)}%*')
            else:
                await ctx.send('Who ?')
        else:
            msg = await ctx.send(re)
            await ctx.message.delete()
            await asyncio.sleep(10)
            await msg.delete()

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rip(self, ctx, *, guy):
        re = self.limit_check('./data/rip_limit.json', ctx.author.id, 'rip')
        if re == True:
            if guy:
                await ctx.send(f'<:WorryRip:697835039697666088> {guy}')
            else:
                await ctx.send('Who ?')
        else:
            msg = await ctx.send(re)
            await ctx.message.delete()
            await asyncio.sleep(10)
            await msg.delete()

    def limit_check(self, file, id, act):
        with open(file) as r:
            re = json.load(r)
        had = False
        for user in re:
            if str(id) == user:
                had = True
        if had == False:
            re[str(id)] = {
                'times': 0,
                'time': None
            }
            with open(file, 'w') as w:
                json.dump(re, w, indent=4)
        with open(file) as f:
            re = json.load(f)
        for user in re:
            if str(id) == user:
                if re[user]['time'] is not None:
                    limit_time = datetime.strptime(re[user]['time'], "%d/%m/%y %H:%M:%S")
                    if limit_time > datetime.now():
                        return f"You have used 3 times {act} limited today (you can use again after {re[user]['time']})."
                    else:
                        re[user]['time'] = None
                        re[user]['times'] = 1
                        with open(file, 'w') as w:
                            json.dump(re, w, indent=4)
                else:
                    re[user]['times'] += 1
                    if re[user]['times'] > 2:
                        re[user]['time'] = (datetime.now()+dt.timedelta(days=1)).strftime("%d/%m/%y %H:%M:%S")
                    with open(file, 'w') as w:
                        json.dump(re, w, indent=4)
        return True


def setup(client):
    client.add_cog(Emoji(client))