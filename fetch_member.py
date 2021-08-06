import discord, pickle, config, sys

client = discord.Client()

@client.event
async def on_ready():
    print('[fetch_member] Logged in as {0} ({0.id})'.format(client.user))
    await get_member()
    print('[fetch_member] Fetched member successfully.')
    await client.close()
    sys.exit()

async def get_member():
    with open('./data/winner', 'r') as f:
        re_ = f.read()
    re = re_.splitlines()
    try:
        guild = await client.fetch_guild(re[0])
        member = await guild.fetch_member(re[1])
        roles_ = []
        for role in member.roles:
            roles_.append(role.id)
        with open('./data/winner', 'wb') as r:
            pickle.dump(roles_, r)
    except Exception as e:
        print('Failed to fetch member\n')
        print(e)
        await client.close()
        sys.exit()

client.run(config.token, reconnect=True, bot=True)