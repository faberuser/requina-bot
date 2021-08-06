import discord, requests, json, os, urllib.parse, urllib.request
from bs4 import BeautifulSoup
#from PIL import Image
from discord.ext import commands
from discord import Webhook, RequestsWebhookAdapter
from os import chdir, getcwd, mkdir

client = discord.Client()

class Tenor_Gif(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        guilds = [213557352782233601, 652813007981772801]
        if message.channel.guild.id not in guilds:
            return
        try:
            with open('./data/tenor', 'r') as f:
                users = f.read()
        except:
            open('./data/tenor', 'a').close()
            users = []
        if str(message.author.id) in users:
            return
        if message.content.startswith('https://tenor.com/view/'):
            count = 0
            while True:
                if count>=5:
                    break
                try:
                    encoded_url = urllib.parse.unquote(message.content)
                    r = requests.get(encoded_url, timeout=2.0)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.content, 'html.parser').find('div', {'class': 'Gif'})
                        url = BeautifulSoup(str(soup), 'html.parser').find('img').get('src')
                        resp = requests.get(url, timeout=2.0)
                        if resp.status_code == 200:
                            with open(f'./data/tenor_media/{message.content[23:]}.gif', 'wb') as r:
                                r.write(resp.content)
                                break
                        else:
                            continue
                    else:
                        continue
                except:
                    r = urllib.request.urlopen(message.content)
                    soup = BeautifulSoup(r.read(), 'html.parser').find('div', {'class': 'Gif'})
                    url = BeautifulSoup(str(soup), 'html.parser').find('img').get('src')
                    resp = requests.get(url, timeout=2.0)
                    if resp.status_code == 200:
                        with open(f'./data/tenor_media/{message.content[23:]}.gif', 'wb') as r:
                            r.write(resp.content)
                            break
                    else:
                        continue
                count+=1
            if count>=5:
                return
            for file in os.listdir('./data/tenor_media'):
                if file.endswith('.gif'):
                    discord_file = discord.File(f'./data/tenor_media/{file}')
                    img = await message.author.avatar_url_as(format='png', static_format='png', size=1024).read()
                    webhook = await message.channel.create_webhook(name=message.author.display_name, avatar=img, reason='Tenor Gif create')
                    webhook = Webhook.partial(webhook.id, webhook.token, adapter=RequestsWebhookAdapter())
                    try:
                        webhook.send(file=discord_file)
                        await message.delete()
                    except Exception as e:
                        print(e)
                        pass
                    webhook.delete(reason='Tenor Gif delete')
                    os.remove(f'./data/tenor_media/{file}')
                    
    @commands.command(aliases=['tenor', 'tenorgif', 'giftenor'])
    async def tenor_gif(self, ctx):
        try:
            with open('./data/tenor', 'r') as f:
                users = f.read()
            with open('./data/tenor', 'w') as r:
                if str(ctx.author.id) not in users:
                    r.write(str(ctx.author.id)+'\n')
                    await ctx.send('Unregistered')
                else:
                    r.write(users.replace(str(ctx.author.id)+'\n', ''))
                    await ctx.send('Registered')
        except:
            with open('./data/tenor', 'a') as r:
                r.write(str(ctx.author.id)+'\n')
                await ctx.send('Unregistered')

def setup(client):
    client.add_cog(Tenor_Gif(client))