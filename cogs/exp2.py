import discord, config
from discord.ext import commands

class Hello(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith('yêu mều'):
            channel = message.channel
            await channel.send('Huh, really...?!')

            def check(m):
                return m.content.lower().startswith() == str('um') and m.channel == channel or \
                    m.content.lower().startswith() == str('uhm') and m.channel == channel or \
                        m.content.lower().startswith() == str('yes') and m.channel == channel

            msg = await self.client.wait_for('message', check=check)
            if message.author.id in config.owners:

                await channel.send('Master, I love you! Huh'.format(msg))
                #print('{.author.name},{.author.id}'.format(msg,msg))

            else:
                await channel.send("I only love my Master, not you!!")
                
        if message.content.lower().startswith('weitei mều'):
            channel = message.channel
            if message.author.id == 213186434193031168:
                await channel.send('Huh, who are you??')
            elif message.author.id == 470081764271063060:
                await channel.send("Master, don't put it too hard, neh")
            else:
                await channel.send('Ero Baka hentaiiiii')

def setup(client):
    client.add_cog(Hello(client))