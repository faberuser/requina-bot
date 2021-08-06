import discord , random
from discord import message
from discord.ext import commands

class Costume(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        one = self.client.get_emoji(652815844967055401)
        two = self.client.get_emoji(652815844598087701)
        three = self.client.get_emoji(652815845025906728)
        four = self.client.get_emoji(652815845000609792)
        five = self.client.get_emoji(652815844929437696)

        if message.content.lower().capitalize().startswith('R.costume requina') or message.content.lower().capitalize().startswith('R.costume'):

            msg = await message.channel.send(f'{one}. Beach Costume\n{two}. School Costume\n{three}. World Costume\n{four}. Halloween Costume\n{five}. Dessert Costume')

            await msg.add_reaction(emoji=f'{one}')
            await msg.add_reaction(emoji=f'{two}')
            await msg.add_reaction(emoji=f'{three}')
            await msg.add_reaction(emoji=f'{four}')
            await msg.add_reaction(emoji=f'{five}')

            def check(reaction, user):
                return user == message.author and str(reaction.emoji) in [f'{one}', f'{two}', f'{three}',f'{four}',f'{five}']

            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=10.0, check=check)
            except asyncio.TimeoutError:
                await msg.delete()
                await message.channel.send("Timeout! Please try again.")

            beach = discord.Embed(title='Requina - Beach Costume', colour=discord.Colour.red())
            beach.set_image(
                url='https://cdn.discordapp.com/attachments/620646132124483594/623914794285531142/Requina_swimsuit.png')

            school = discord.Embed(title='Requina - School Costume', colour=discord.Colour.red())
            school.set_image(
                url="https://cdn.discordapp.com/attachments/620646132124483594/623912922774765579/Requina_school.png")

            world = discord.Embed(title='Requina - World Costume', colour=discord.Colour.red())
            world.set_image(
                url="https://cdn.discordapp.com/attachments/620646132124483594/623914914410528798/Requina_World.png")

            hlw = discord.Embed(title='Requina - World Costume', colour=discord.Colour.red())
            hlw.set_image(
                url="https://cdn.discordapp.com/attachments/620646132124483594/648161907207045120/Requina_halloween.png")    

            dessert = discord.Embed(title='Requina - Dessert Costume', colour=discord.Colour.red())
            dessert.set_image(
                url="https://cdn.discordapp.com/attachments/608764800566165534/669821622806511627/Requina_Dessert.png")   

            if str(reaction.emoji) in f'{one}':
                await msg.delete()
                await message.channel.send(embed=beach)
            if str(reaction.emoji) in f'{two}':
                await msg.delete()
                await message.channel.send(embed=school)
            if str(reaction.emoji) in f'{three}':
                await msg.delete()
                await message.channel.send(embed=world)
            if str(reaction.emoji) in f'{four}':
                await msg.delete()
                await message.channel.send(embed=hlw)
            if str(reaction.emoji) in f'{five}':
                await msg.delete()
                await message.channel.send(embed=dessert)


    @commands.command()
    async def randomart(self, ctx):
        embed = discord.Embed(title="Random", clour=discord.Color.red())

        raart = ['https://cdn.discordapp.com/attachments/522649121933230100/533635120565846026/image0.jpg',
                 'https://cdn.discordapp.com/attachments/522649121933230100/533635135145508864/image0.jpg'
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
        
def setup(client):
    client.add_cog(Costume(client))

