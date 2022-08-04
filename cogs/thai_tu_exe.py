import discord, random, re
from discord.ext import commands

client = discord.Client()

class Thai_Tu(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.thai_tu = ['thái tử thúi', 'dăm ba thái tử']

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id == 213557352782233601 or message.channel.id == 718434254832402474:
            if message.author.id == 388809395812696065 or message.author.id == 315724989057990663:
                if 'http' in message.content:
                    if 'google' in message.content:
                        return
                    elif 'youtube' in message.content:
                        if message.content.endswith('.com/') or message.content.endswith('.com'):
                            return
                    elif 'bing' in message.content:
                        return
                    url = message.content
                    content = f'{random.choice(self.thai_tu)}: {url}'
                    if ' ' in message.content:
                        url = 'http'+re.search(f"{'http'}(.*?){' '}", url).group(1)
                        msg = message.content.replace(url, '')
                        content = f'{random.choice(self.thai_tu)}: {url} {msg}'
                    with open('./data/thai_tu', 'r+') as f:
                        re_ = f.read()
                        if url not in re_:
                            f.write(url+'\n')
                            #await message.channel.send(content)

def setup(client):
    client.add_cog(Thai_Tu(client))