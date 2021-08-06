import discord, youtube_dl, os, shutil, requests
from discord.ext import commands

client = discord.Client()

class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['yt_music', 'ytm'])
    async def youtube_music(self, ctx, url:str=None, format_:str=None):
        if url is None and format_ is None:
            embed = discord.Embed(title='Youtube Downloader',
                                description='Syntax:\n`?youtube_music <url> <format>`\n\n`url`: str (playlist supported)\n`format`: default is mp3 (can set to wav)')
            await ctx.send(embed=embed)
        else:
            if format_ is not None:
                if format_.lower() == 'wav':
                    ydl_opts = {
                        'outtmpl': './youtube-download/%(title)s.%(ext)s',
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'wav',
                            'preferredquality': '1411',
                            }],
                        }
            else:
                ydl_opts = {
                    'outtmpl': './youtube-download/%(title)s.%(ext)s',
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                        }],
                    }
            msg = await ctx.send('Downloading...')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            for file in os.listdir('./youtube-download'):
                if file.endswith('.mp3') or file.endswith('.wav'):
                    file_dir = discord.File('./youtube-download/'+file)
                    await msg.delete()
                    try:
                        await ctx.send(content='Downloaded.', file=file_dir)
                        os.remove('./youtube-download/'+file)
                    except:
                        await ctx.send(content="File too large, i can't send it. Uploading to...")
                        #download_url = self.instant(file)
                        shutil.move('./youtube-download/'+file, './youtube-download/large')
                    break


    @commands.command(aliases=['yt_video', 'ytv'])
    async def youtube_video(self, ctx, url:str=None, size:str=None):
        if url is None and size is None:
            embed = discord.Embed(title='Youtube Downloader',
                                description='Syntax:\n`?youtube_video <url> <size>`\n\n`url`: str (playlist supported)\n`size`: default is 1080 (can set to 720, 480, 360, 240)')
            await ctx.send(embed=embed)
        else:
            if size is None:
                size = '1080'
            formats = [1080, 720, 480, 360, 240]
            f_ = [7, 6, 5, 4, 3]
            count = 0
            msg = await ctx.send('Downloading...')
            for f in f_:
                if str(formats[count]) == size:
                    with youtube_dl.YoutubeDL({'outtmpl': './youtube-download/%(title)s.%(ext)s', 'format':'13'+str(f)}) as ydl:
                        file = ydl.download([url])
                else:
                    count+=1
                    continue
            for file in os.listdir('./youtube-download'):
                if file.endswith('.mp4'):
                    file_dir = discord.File('./youtube-download/'+file)
                    await msg.delete()
                    try:
                        await ctx.send(content='Downloaded.', file=file_dir)
                        os.remove('./youtube-download/'+file)
                    except:
                        await ctx.send(content="File too large, i can't send it. Uploading to...")
                        download_url = self.instant(file)
                        #shutil.move('./youtube-download/'+file, './youtube-download/large')
                    break

    def instant(self, file):
        url = 'https://jirafeau.net/script.php'
        with open(f'./youtube-download/{file}', 'rb') as f:
            print(f)
            file_ = {'file': f}
            resp = requests.post(url, files=file_)
            print(resp)
            print(resp.content)
            print(resp.text)
        #return download_url

def setup(client):
    client.add_cog(Youtube(client))