# SETUP
# Config emoji (format: <:<emoji_name>:<emoji_id>>)
import concurrent, asyncio, aiohttp, pickle, time, re, os, random, discord, config
from discord.ext import tasks, commands
from datetime import datetime
emoji = '<:party:652813264614326313>'
# Giveaway channel
channel_ids = [641996130262974474, 718434254832402474, 825591043831234580]
# Decreased won users rate (>1)
rate = 2


client = discord.Client()


class Giveaway(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.check_ga_loop.start()
        if os.path.exists('./data/ga_end') == False:
            os.mkdir('./data/ga_end')

    @tasks.loop(count=1)
    async def check_ga_loop(self):
        asyncio.create_task(self.check_ga())
    
    @check_ga_loop.before_loop
    async def before_check_ga_loop(self):
        await self.client.wait_until_ready()

    def tasks_(self, file, msg, decrease_rate: bool, no_won: bool):
        while True:
            try:
                with open(f'./data/ga_end/{file}', 'r') as f:
                    re = f.read()
                    re_ = re.splitlines()
                    end_time = datetime.strptime(re_[2], '%H:%M-%d/%m/%Y')
                print(
                    f"Checking for Give Away '{file}': '{re_[2]}' at {datetime.now().strftime('%H:%M-%d/%m/%Y')}")
            except ValueError:
                print('Error. Time data does not match format `HH:mm-dd/MM/yyyy` or `%H:%M-%d/%m/%Y`. This task has been canceled.')
                break
            current_time = datetime.now()
            if current_time >= end_time:
                print(f"'{file}' Matched!")
                return [file, msg, decrease_rate, no_won]
            else:
                print(f"'{file}' Not match.")
                time.sleep(60)

    async def check_ga(self):
        ga_s = []
        for file in os.listdir('./data/ga_end'):
            with open(f'./data/ga_end/{file}') as f:
                lines = f.readlines()
            if lines[5] == 'not':
                try:
                    channel = self.client.get_channel(int(lines[0]))
                    msg = await channel.fetch_message(int(lines[1]))
                except Exception as e:
                    print("Failed to check_ga.")
                    print(e)
                decrease_rate, no_won, nitroed = False, False, False
                if lines[3] == 'True':
                    decrease_rate = True
                if lines[4] == 'True':
                    no_won = True
                if lines[5] == 'True':
                    nitroed = True
                ga_s.append([file, msg, decrease_rate, no_won, nitroed])
        if ga_s != []:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                exc = self.tasks_
                for ga in ga_s:
                    futures.append(executor.submit(
                        exc, ga[0], ga[1], ga[2], ga[3], ga[4]))
                await asyncio.sleep(5)
                while True:
                    if futures == []:
                        print('No GA left!')
                        break
                    else:
                        for future in futures:
                            if future._state == 'FINISHED':
                                re = future.result()
                                print(f"'{re[0]}' FINISHED")
                                try:
                                    users = await self.users(msg, re[3], re[4], re[0])
                                    if users == []:
                                        return
                                    embed, content = await self.roll_(users, re[1], re[2])
                                    await re[1].edit(embed=embed)
                                    await re[1].channel.send(content)
                                    with open(f'./data/ga_end/{re[0]}', 'r') as f:
                                        re_ = f.read()
                                    with open(f'./data/ga_end/{re[0]}', 'w') as r:
                                        r.write(re_.replace('not', 'done'))
                                except Exception as e:
                                    print("Failed to result.")
                                    print(e)
                                    pass
                                futures.remove(future)
                            else:
                                pass
                        await asyncio.sleep(60)
        else:
            print('No GA left!')


    # Gievaway embed command
    @commands.command(pass_context=True)
    async def ga(self, ctx, *, text=None):
        if text is None:
            embed = discord.Embed(
                title='Give Away Command',
                description='''Syntax:\n`r.ga title=<title>, description=<description>, role=<@role>/leave_blank, time=<end_time>/leave_blank, no_won=False, nitroed=False, decrease_rate=False`\n
				Time format: `HH:mm-dd/MM/yyyy` (24 hour based hour with 0 prefix, minute without 0 prefix, day with 0 prefix, month with 0 prefix, represents full year)
				Time format example: `02:30-19/09/2019` or `20:00-20/02/2020`.
				`no_won`: Excludes won users from the GA. Default sets to False.
                `nitroed`: Excludes users alreading having nitro from the GA. Default sets to False.
				`decrease_rate`: Decreases winning rate of the won users. Default sets to False.\n
				Example: `r.ga title=Nitro, description=1 Month, role= @Nitro , time=20:00-20/02/2020`''',
                colour=discord.Colour.from_rgb(
                    223, 165, 210),  # A gei embed color
            )
            await ctx.send(embed=embed)
        if text is not None:
            tit, des, role, author, time, decrease_rate, no_won, nitroed = None, None, None, None, None, None, None, None
            text = f'{text},'
            # Remove 5 lines below to remove giveaway channel
            if ctx.channel.id not in channel_ids:
                await ctx.send("I don't giveaway anything outside Giveaway channel.")
                return
            else:
                pass

            ###
            try:  # embed title aka prize
                if 'title=' in text:
                    tit = self.find(text, 'title=', ',')
                elif 'title =' in text:
                    tit = self.find(text, 'title =', ',')
                if '<nitro>' in tit:
                    # replace nitro emoji in embed title
                    tit = tit.replace('<nitro>', '<:nitro:652813266493374484>')
            except:
                pass

            try:  # embed description
                if 'description=' in text:
                    des = self.find(text, 'description=', ',')
                elif 'description =' in text:
                    des = self.find(text, 'description =', ',')
            except:
                pass

            try:  # given role
                if 'role=' in text:
                    role_ = self.find(text, 'role=', ',')
                    if ' ' in role_:
                        role_ = role_.replace(' ', '')
                    role__ = discord.utils.get(
                        ctx.guild.roles, id=int(role_[3:][:-1]))  # get role
                elif 'role =' in text:
                    role_ = self.find(text, 'role =', ',')
                    if ' ' in role_:
                        role_ = role_.replace(' ', '')
                    role__ = discord.utils.get(
                        ctx.guild.roles, id=int(role_[3:][:-1]))  # get role
                role = role__.mention
            except:
                pass

            try:  # get time
                if 'time=' in text:
                    time = self.find(text, 'time=', ',')
                elif 'time =' in text:
                    time = self.find(text, 'time =', ',')
                if time is not None:
                    if ' ' in time:
                        time = time.replace(' ', '')
                    datetime.strptime(time, '%H:%M-%d/%m/%Y')
            except ValueError:
                await ctx.message.delete()
                msg = await ctx.send(f'Error. Time data does not match format:\n`HH:mm-dd/MM/yyyy` or\n`full_hour:full_minute-full_day/full_month/full_year`\nPlease try again. This message will last for 10 seconds.')
                time.sleep(10)
                await msg.delete()
                return

            try:  # get author
                if 'author=' in text:
                    author_ = self.find(text, 'author=', ',')
                    if ' ' in author_:
                        author_ = author_.replace(' ', '')
                elif 'author =' in text:
                    author_ = self.find(text, 'author =', ',')
                    if ' ' in author_:
                        author_ = author_.replace(' ', '')
                author = self.client.get_user(int(author_))
            except:
                pass

            try:  # get no_won bool
                if 'no_won=' in text:
                    no_won = self.find(text, 'no_won=', ',')
                    if ' ' in no_won:
                        no_won = no_won.replace(' ', '')
                elif 'no_won =' in text:
                    no_won = self.find(text, 'no_won =', ',')
                    if ' ' in no_won:
                        no_won = no_won.replace(' ', '')
                if no_won == 'True':
                    no_won = True
                else:
                    no_won = False
            except:
                no_won = False

            try:  # get no_won bool
                if 'nitroed=' in text:
                    nitroed = self.find(text, 'nitroed=', ',')
                    if ' ' in nitroed:
                        nitroed = nitroed.replace(' ', '')
                elif 'nitroed =' in text:
                    nitroed = self.find(text, 'nitroed =', ',')
                    if ' ' in nitroed:
                        nitroed = nitroed.replace(' ', '')
                if nitroed == 'True':
                    nitroed = True
                else:
                    nitroed = False
            except:
                nitroed = False

            try:  # get decrease_rate bool
                if 'decrease_rate=' in text:
                    decrease_rate = self.find(text, 'decrease_rate=', ',')
                    if ' ' in decrease_rate:
                        decrease_rate = decrease_rate.replace(' ', '')
                elif 'decrease_rate =' in text:
                    decrease_rate = self.find(text, 'decrease_rate =', ',')
                    if ' ' in decrease_rate:
                        decrease_rate = decrease_rate.replace(' ', '')
                if decrease_rate == 'True':
                    decrease_rate = True
                else:
                    decrease_rate = False
            except:
                decrease_rate = False
            if role is not None:
                req = f'\n*Yêu cầu role {role}.*'  # role
            else:
                req = '\n*Không yêu cầu role.*'
            if time is not None:
                time_ = f'\nKết thúc lúc {time}.'  # time
            else:
                time_ = ''

            embed = discord.Embed(
                title=f'{tit}',
                description=des+req,
                colour=discord.Colour.from_rgb(
                    223, 165, 210),  # A gei embed color
            )
            if author:
                embed.set_author(
                    name=author,
                    icon_url=author.avatar_url,
                )
            else:
                embed.set_author(
                    name=ctx.author,
                    icon_url=ctx.author.avatar_url,
                )
            embed.set_footer(text=time_)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction(emoji)
            await ctx.message.delete()
            if time is not None:
                file = self.create_file(
                    msg.channel.id, msg.id, time, decrease_rate, no_won, nitroed)
                re = await self.task(file, decrease_rate, no_won, nitroed)
                await ctx.send(re)

    # Roll command
    @commands.command(pass_context=True)
    async def roll(self, ctx, msg_id: int = None, no_won: bool = False, nitroed: bool = False, decrease_rate: bool = False, *, time: str = None):
        if msg_id is None:
            embed = discord.Embed(
                title='Roll Commad',
                description='''Syntax:\n`r.roll <message_id> no_won=False nitroed=False decrease_rate=False <end_time>/leave_blank`\n
				Time format same as `/ga`. This command must be used in the same channel with the Giveaway embed message.''',
                colour=discord.Colour.from_rgb(
                    223, 165, 210),  # A gei embed color
            )
            await ctx.send(embed=embed)
        else:
            msg = await ctx.channel.fetch_message(msg_id)
            users = await self.users(msg, no_won, nitroed)
            if users == []:
                await ctx.message.delete()
                return
            else:
                pass
            if time is None:  # end the giveaway with message's id if time isn't given
                await ctx.message.delete()
                re = await self.roll_(users, msg, decrease_rate)
                await msg.edit(embed=re[0])
                await ctx.send(re[1])
            else:  # create timer for giveaway and given time
                await ctx.message.delete()
                file = self.create_file(
                    ctx.channel.id, msg_id, time, decrease_rate, no_won, nitroed)
                msg_ = await ctx.send('ok')
                await asyncio.sleep(1)
                await msg_.delete()
                re = await self.task(file, decrease_rate, no_won, nitroed)
                await ctx.send(re)

    # Loop checking time
    async def task(self, file, decrease_rate: bool, no_won: bool, nitroed: bool):
        while True:
            try:
                with open(f'./data/ga_end/{file}', 'r') as f:
                    re = f.read()
                    re_ = re.splitlines()
                    end_time = datetime.strptime(re_[2], '%H:%M-%d/%m/%Y')
                print(
                    f"Checking for Give Away '{file}': '{re_[2]}' at {datetime.now().strftime('%H:%M-%d/%m/%Y')}")
            except ValueError:
                print(
                    'Error. Time data does not match format `HH:mm-dd/MM/yyyy` or `%H:%M-%d/%m/%Y`. This task has been canceled.')
                break
            current_time = datetime.now()
            if current_time >= end_time:
                print(f"'{file}' Matched!")
                chan = self.client.get_channel(int(re_[0]))
                msg = await chan.fetch_message(int(re_[1]))
                users = await self.users(msg, no_won, nitroed, file)
                if users == []:
                    return
                embed, content = await self.roll_(users, msg, decrease_rate)
                await msg.edit(embed=embed)
                with open(f'./data/ga_end/{file}', 'w') as r:
                    r.write(re.replace('not', 'done'))
                return content
            else:
                print(f"'{file}' Not match.")
                pass
            await asyncio.sleep(60)

    async def users(self, msg, no_won: bool, nitroed: bool, file=None):
        users = []
        try:
            for reaction in msg.reactions:
                if str(reaction.emoji) == emoji:
                    async for user in reaction.users():
                        if user.bot is True:
                            pass
                        else:
                            # apppend all reacted user's ids into a list
                            users.append(user)
                else:
                    pass
        except Exception as e:
            return

        if no_won is True:  # removes won user from the list
            users_ = users
            users = []
            for user in users_:
                with open('./data/winners.txt', 'r') as f:
                    winners = f.read()
                    if str(user.id) in winners:
                        continue
                    users.append(user)

        if nitroed is True: # removes users already having nitro from the list
            users_ = users
            users = []
            for user in users_:
                try:
                    if await self.guess_user_nitro_status(user) == False:
                        users.append(user)
                except:
                    users.append(user)

        if users == [] or users == None:
            print('No user reacted, passed GA.')
            if file is not None:
                if file is False or file is True:
                    return
                with open(f'./data/ga_end/{file}', 'r') as f:
                    re = f.read()
                with open(f'./data/ga_end/{file}', 'w') as r:
                    r.write(re.replace('not', 'done'))
        return users

    async def guess_user_nitro_status(self, user: discord.User or discord.Member):
        if isinstance(user, discord.Member):
            has_emote_status = any([a.emoji.is_custom_emoji() for a in user.activities if getattr(a, 'emoji', None)])
            return any([user.is_avatar_animated(), has_emote_status, user.premium_since, await self.banner_s(user)])
        return any([user.is_avatar_animated(), await self.banner_s(user)])

    async def banner_s(self, user):
        user_id = user.id
        au = user

        resolution = 1024
        endpoints = (
            "https://cdn.discordapp.com/banners/",
            "https://discord.com/api/v9/users/{}".format(user_id)
        )
        headers = {
            "Authorization": f"Bot {config.token}"
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(endpoints[1]) as response:
                data = await response.json()
                try:
                    url = endpoints[0] + str(user_id) + "/" + data["banner"] + "?size={0}".format(resolution)
                    return True
                except:
                    return False

    async def roll_(self, users, msg, decrease_rate: bool):
        guild = msg.channel.guild
        winners = self.decreased_winners()
        count = 0
        if '<@&' in msg.embeds[0].description:
            role = f"<@&{self.find(msg.embeds[0].description, '<@&', '>')}>"
            role = discord.utils.get(guild.roles, id=int(role[3:][:-1]))
            while True:  # random user's ids in loop until match the user has the given role
                winner = random.choice(users)
                if decrease_rate is True:
                    if winner.id in winners:
                        count += 1
                        if count >= rate:
                            pass
                        else:
                            continue
                roles = await self.get_member_roles(guild.id, winner.id)
                val = False
                for role_ in roles:
                    if role.id == role_:
                        val = True
                        break
                    else:
                        count = 0
                        continue
                if val == False:
                    continue
                else:
                    break
        else:
            while True:
                # random user's ids if there is no given role
                winner = random.choice(users)
                if decrease_rate is True:
                    if winner.id in winners:
                        count += 1
                        if count >= rate:
                            break
                        else:
                            continue
                break

        embed = discord.Embed(
            title=msg.embeds[0].title, description=f'{msg.embeds[0].description}\nNgười húp: {winner.mention}', colour=msg.embeds[0].colour)
        embed.set_author(
            name=msg.embeds[0].author.name, icon_url=msg.embeds[0].author.icon_url)
        embed.set_footer(text=msg.embeds[0].footer.text)
        # if custom_msg:
        # await msg.channel.send(f'{custom_msg} {winner.mention} {emoji}')
        content = f'Chúc mừng {winner.mention} đã húp được `{msg.embeds[0].title}`! {emoji}'
        with open('./data/winners.txt', 'a') as f:
            f.write(str(winner.id)+'\n')
        return [embed, content]

    async def get_member_roles(self, guild_id, winner_id):
        try:
            guild = self.client.get_guild(guild_id)
            member = await guild.fetch_member(winner_id)
            roles_ = []
            for role in member.roles:
                roles_.append(role.id)
            return roles_
        except Exception as e:
            print('Failed to fetch member\n')
            print(e)

    def decreased_winners(self):
        winners = []
        try:
            with open('./data/winners.txt', 'r') as f:
                re = f.readlines()
                for winner in re:
                    winners.append(int(winner))
        except FileNotFoundError:
            open('./data/winners.txt', 'a').close()
            with open('./data/winners.txt', 'r') as f:
                re = f.readlines()
                for winner in re:
                    winners.append(int(winner))
        return winners

    def find(self, txt, start, end):
        #cn = txt[txt.find(start)+len(start):txt.rfind(end)]
        cn = re.search(f"{start}(.*?){end}", txt).group(1)
        return cn

    # generate files for task-checking
    def create_file(self, channel_id, msg_id, time, decrease_rate, no_won, nitroed):
        files = []
        num = 0
        for file in os.listdir('./data/ga_end'):
            files.append(int(file))
        if files == []:
            with open(f'./data/ga_end/0', 'a') as r:
                r.write(str(channel_id)+'\n'+str(msg_id)+'\n'+time +
                        '\n'+str(decrease_rate)+'\n'+str(no_won)+'\n'+str(nitroed)+'\nnot')
            files.append('0')
        else:
            num = max(files)
            num = int(num) + 1
            with open(f'./data/ga_end/{num}', 'a') as f:
                f.write(str(channel_id)+'\n'+str(msg_id)+'\n'+time +
                        '\n'+str(decrease_rate)+'\n'+str(no_won)+'\n'+str(nitroed)+'\nnot')
        return num


def setup(client):
    client.add_cog(Giveaway(client))
