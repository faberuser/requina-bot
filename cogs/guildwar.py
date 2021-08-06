import discord
import datetime
import time
import random
from discord.ext import commands, tasks

client = discord.Client()

class GuildWar(commands.Cog):

	def __init__(self, client):
		self.client = client
		self.announce.start()

	@commands.command()
	async def guildwar(self, ctx, arg: str):
		mans = [315724989057990663, 213186434193031168, 470081764271063060]
		if ctx.author.id not in mans:
			await ctx.send("You don't have enough permission(s) to use this command.")
			return
		elif arg is None:
			await ctx.send('You want the Guild War Announcement on or off?')
		else:
			if arg == 'on':
				with open('./data/guildwar.txt', 'w') as f:
					f.write('on')
				await ctx.send('Turned on Guild War Announcement')
			elif arg == 'off':
				with open('./data/guildwar.txt', 'w') as f:
					f.write('off')
				await ctx.send('Turned off Guild War Announcement')
			else:
				await ctx.send('???')

	@tasks.loop(minutes=1, reconnect=True)
	async def announce(self):
		today = datetime.date.today().weekday()
		timenow = time.localtime()
		if today == int(0) or today == int(3) or today == int(4) or today == int(6):
			if timenow.tm_hour == int(20) and timenow.tm_min == int(0):
				with open('./data/guildwar.txt', 'r') as f:
					re = f.read()
				if re == 'on':
					pass
				else:
					return
				try:
					serv = self.client.get_guild(213557352782233601)
					role = serv.get_role(700715274470686761)
					chan = self.client.get_channel(521919527391330315)
					lilia = self.client.get_emoji(700769141753249795)
					erze = self.client.get_emoji(700769141203927190)
					lucias = self.client.get_emoji(700769141350727680)
					if today == int(6) or today == int(3):
						first = [f'Guild War nào các huynh đài {role.mention} {lilia}, còn 1 ngày 2 giờ nữa nhé. Iu Neko <:WorryKiss:614684041085583384>',\
							f'Vào đánh Guild War nào {role.mention}, còn 1 ngày 2 giờ nữa nhé {erze} Love Neko <:WorryKiss:614684041085583384>',\
							f'Guild War nào {role.mention}, còn 1 ngày 2 giờ nữa nhé {lucias} Hôn Neko <:WorryKiss:614684041085583384>']
						await chan.send(random.choice(first))
					else:
						sec = [f'Guild War nào các huynh đài {role.mention} {lilia}, còn 2 giờ nữa nhé. Iu Neko <:WorryKiss:614684041085583384>',\
							f'Vào đánh Guild War nào {role.mention}, còn 2 giờ nữa nhé {erze} Love Neko <:WorryKiss:614684041085583384>',\
							f'Guild War nào {role.mention}, còn 2 giờ nữa nhé {lucias} Hôn Neko <:WorryKiss:614684041085583384>']
						await chan.send(random.choice(sec))
					print(datetime.datetime.now().strftime("%c") + ' | sent')
				except Exception as e:
					print(e)
					pass

	@announce.before_loop
	async def before_annoucne(self):
		await self.client.wait_until_ready()

def setup(client):
	client.add_cog(GuildWar(client))