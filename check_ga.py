import discord, os, time, asyncio, config, sys
from datetime import datetime
import concurrent.futures
from cogs import give_away

client = discord.Client()

async def check_ga():
    ga_s = []
    for file in os.listdir('./data/ga_end'):
        with open(f'./data/ga_end/{file}') as f:
            lines = f.readlines()
        if lines[5] == 'not':
            try:
                channel = client.get_channel(int(lines[0]))
                msg = await channel.fetch_message(int(lines[1]))
            except Exception as e:
                print("Failed to 'check_ga'.")
                print(e)
            decrease_rate, no_won = False, False
            if lines[3] == 'True':
                decrease_rate=True
            if lines[4] == 'True':
                no_won=True
            ga_s.append([file, msg, decrease_rate, no_won])
    if ga_s != []:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            exc = tasks
            for ga in ga_s:
                futures.append(executor.submit(exc, ga[0], ga[1], ga[2], ga[3]))
            await asyncio.sleep(5)
            while True:
                if futures == []:
                    print('No GA left!')
                    await client.logout()
                    break
                else:
                    for future in futures:
                        if future._state == 'FINISHED':
                            re = future.result()
                            print(f"'{re[0]}' FINISHED")
                            try:
                                users = await give_away.Giveaway(client).users(msg, re[3], re[0])
                                if users == []:
                                    return
                                embed, content = give_away.Giveaway(client).roll_(users, re[1], re[2])
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
            sys.exit()
    else:
        print('No GA left!')
        await client.logout()
        sys.exit()

def tasks(file, msg, decrease_rate:bool, no_won:bool):
    while True:
        try:
            with open(f'./data/ga_end/{file}', 'r') as f:
                re = f.read()
                re_ = re.splitlines()
                end_time = datetime.strptime(re_[2], '%H:%M-%d/%m/%Y')
            print(f"Checking for Give Away '{file}': '{re_[2]}' at {datetime.now().strftime('%H:%M-%d/%m/%Y')}")
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

@client.event
async def on_ready():
    print('[check_ga.py] Logged in as {0} ({0.id})\nChecking for not finished GA.'.format(client.user))
    await check_ga()

client.run(config.token, reconnect=True, bot=True)