import requests, os, discord, logging, json, bs4, datetime, time, asyncio, pytz, tweepy, psutil, config, aiohttp
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

from .utils import resource, info_embed

check = None
auth = None
api = None
if (
    config.BEARER_TOKEN == ""
    or config.CONSUMER_KEY == ""
    or config.CONSUMER_SECRET == ""
    or config.ACCESS_TOKEN == ""
    or config.ACCESS_TOKEN_SECRET == ""
):
    check = False
    print("Twitter API Token(s) has been passed. Tweet-checking has been disabled.")
else:
    check = True
    bearer_token = config.BEARER_TOKEN
    consumer_key = config.CONSUMER_KEY
    consumer_secret = config.CONSUMER_SECRET
    access_token = config.ACCESS_TOKEN
    access_token_secret = config.ACCESS_TOKEN_SECRET

    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)
    api = tweepy.Client(
        bearer_token, consumer_key, consumer_secret, access_token, access_token_secret
    )

client = discord.Client()

lg = [
    [
        "EN",
        "https://kr-official.community/en-community/",
        "./data/kr-official.community/en_ids",
        "./data/plug/channels_en.json",
    ]
]


class KingsRaidAnnounce(commands.Cog):
    def __init__(self, client):
        # kr community
        self.client = client
        self.checker_.start()
        self.channels = {}

        # guild war
        self.announce.start()

        # twitter
        self.api = api
        if check == True:
            self.twitter_.start()
        else:
            return
        self.twitter_.add_exception_type(aiohttp.ClientConnectionError)
        self.twitter_.add_exception_type(
            aiohttp.client_exceptions.ClientConnectionError
        )
        self.info_embed_ = info_embed.Info_Embed()
        self.channel_path = "./data/twitter/channels.json"

        try:
            with open(self.channel_path) as f:
                self.channels = json.load(f)
        except FileNotFoundError:
            open(self.channel_path, "a").close()
            self.channels = {}
        except Exception as e:
            raise (e)

    @tasks.loop(minutes=1, reconnect=True)  # loop checking task
    async def checker_(self):
        await self.checker(lg)

    async def checker(self, lg):
        resource.states_("new posts...")
        for lg_ in lg:
            lang = lg_[0]
            url = lg_[1]
            ids_path = lg_[2]
            channel_path = lg_[3]
            try:
                with open(channel_path) as f:
                    self.channels = json.load(f)
            except FileNotFoundError:
                open(channel_path, "a").close()
                self.channels = {}
                print(f"No reregistered channel found, breaking the {lang} loop...")
                break
            except Exception as e:
                raise (e)
            try:
                html_doc = requests.get(url, timeout=10.0).text
            except Exception as e:
                logging.critical(e)
                return
            soup = BeautifulSoup(html_doc, "html.parser")
            try:
                with open(ids_path, "r") as r:
                    ids = r.read()
            except FileNotFoundError:
                open(ids_path, "a").close()
                with open(ids_path, "r") as r:
                    ids = r.read()

            if lang == "EN":  # english page crawl
                soup3 = soup.find_all(
                    "ul",
                    {
                        "class": "wp-block-latest-posts__list has-dates has-author wp-block-latest-posts"
                    },
                )
                posts = BeautifulSoup(str(soup3), "html.parser").find_all("li")
                for post_ in posts:
                    post = BeautifulSoup(str(post_), "html.parser")
                    a = post.find("a")
                    url_ = a.get("href")
                    if url_ is not None:
                        if url_ not in ids:
                            msg = "New " + lang + " post found: " + url_
                            logging.info(msg)
                            print(msg)
                            with open(ids_path, "a", encoding="utf-8") as f:
                                f.write(url_ + "\n")
                            title = a.get_text()
                            author_name = post.find("div").get_text()[3:]
                            time_ = post.find("time").get("datetime").replace("T", " ")
                            time = datetime.datetime.strptime(
                                time_, "%Y-%m-%d %H:%M:%S%z"
                            )
                            try:
                                page = requests.get(url_, timeout=10.0).text
                                page_soup = BeautifulSoup(page, "html.parser")
                                thumbnail = page_soup.find("img").get("src")
                            except Exception as e:
                                thumbnail = None
                                logging.critical(e)
                            if config.parallel_tasks == True:
                                asyncio.create_task(
                                    self.sender(
                                        lang,
                                        title,
                                        url_,
                                        thumbnail,
                                        time,
                                        author_name,
                                        channel_path,
                                        self.channels,
                                    )
                                )
                            else:
                                await self.sender(
                                    lang,
                                    title,
                                    url_,
                                    thumbnail,
                                    time,
                                    author_name,
                                    channel_path,
                                    self.channels,
                                )

    async def sender(
        self, lang, title, url_, thumbnail, time, author_name, channel_path, channels
    ):  # get embed and send to channels
        try:
            chan = self.client.get_channel(config.cache_channel)
            msg = await chan.send(url_)
            await asyncio.sleep(30)
            embed = (await chan.fetch_message(msg.id)).embeds[0]
            embed.colour = discord.Colour.from_rgb(24, 8, 84)
            embed.timestamp = time
            if thumbnail is not None:
                embed.set_image(url=thumbnail)
            else:
                try:
                    embed.set_image(url=embed.thumbnail.url)
                except:
                    pass
            embed.thumbnail.url = None
        except:
            embed = discord.Embed(
                title=title,
                url=url_,
                timestamp=time,
                colour=discord.Colour.from_rgb(24, 8, 84),
            )
            embed.set_author(name=author_name)
            if thumbnail is not None:
                embed.set_thumbnail(url=thumbnail)
        for key in channels:
            if channels[key]:
                chan = self.client.get_channel(int(key))
                try:
                    if isinstance(chan, discord.abc.GuildChannel):
                        attemp = f" | {lang} attempting to send to channel #{key}"
                        logging.info(attemp)
                        print(attemp)
                        await chan.send(embed=embed)
                        success = f" | {lang} successfully sent to #{chan.name} on {chan.guild.name}"
                        logging.info(success)
                        print(success)
                    else:
                        invalid = f" | {lang} channel #{key} is invalid, removing"
                        logging.info(invalid)
                        print(invalid)
                        channels[key] = False
                        write_channels(channel_path, channels)
                except discord.errors.Forbidden as r:
                    forbidden = f" | FORBIDDEN: {str(r)} | Channel: #{chan.name} on {chan.guild.name}"
                    logging.warn(forbidden)
                    print(forbidden)
                except Exception as e:
                    logging.warn(e)
                    print(e)

    @checker_.before_loop
    async def before_checker(self):
        await self.client.wait_until_ready()

    # @commands.command(aliases=["guild_war"])
    async def guildwar(self, ctx, arg: str):
        if ctx.author.id not in config.owners:
            await ctx.send("You don't have enough permission(s) to use this command.")
            return
        elif arg is None:
            await ctx.send("You want the Guild War Announcement on or off?")
        else:
            if arg == "on":
                with open("./data/guildwar.txt", "w") as f:
                    f.write("on")
                await ctx.send("Turned on Guild War Announcement")
            elif arg == "off":
                with open("./data/guildwar.txt", "w") as f:
                    f.write("off")
                await ctx.send("Turned off Guild War Announcement")
            else:
                await ctx.send("???")

    @tasks.loop(minutes=1, reconnect=True)
    async def announce(self):
        hcm = datetime.datetime.now(pytz.timezone("Asia/Ho_Chi_Minh"))
        today = hcm.today().weekday()
        if today == int(0) or today == int(3) or today == int(4) or today == int(6):
            if hcm.hour == int(20) and hcm.minute == int(0):
                # if hcm.hour == int(20) and hcm.minute == int(0):
                with open("./data/guildwar.txt", "r") as f:
                    re = f.read()
                if re == "on":
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
                        first = [
                            f"Guild War nào các huynh đài {role.mention} {lilia}, còn 1 ngày 2 giờ nữa nhé. Iu Neko <:WorryKiss:614684041085583384>",
                            f"Vào đánh Guild War nào {role.mention}, còn 1 ngày 2 giờ nữa nhé {erze} Love Neko <:WorryKiss:614684041085583384>",
                            f"Guild War nào {role.mention}, còn 1 ngày 2 giờ nữa nhé {lucias} Hôn Neko <:WorryKiss:614684041085583384>",
                        ]
                        await chan.send(random.choice(first))
                    else:
                        sec = [
                            f"Guild War nào các huynh đài {role.mention} {lilia}, còn 2 giờ nữa nhé. Iu Neko <:WorryKiss:614684041085583384>",
                            f"Vào đánh Guild War nào {role.mention}, còn 2 giờ nữa nhé {erze} Love Neko <:WorryKiss:614684041085583384>",
                            f"Guild War nào {role.mention}, còn 2 giờ nữa nhé {lucias} Hôn Neko <:WorryKiss:614684041085583384>",
                        ]
                        await chan.send(random.choice(sec))
                    print(datetime.datetime.now().strftime("%c") + " | sent")
                except Exception as e:
                    print(e)
                    pass

    @announce.before_loop
    async def before_annoucne(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes=1, reconnect=True)  # twitter task checking
    async def twitter_(self):
        resource.states_("Tweets")
        try:
            tweets = self.api.get_users_tweets(
                1248518690535923712, max_results=10, exclude="replies"
            )
        except Exception as e:
            logging.warn(e)
            return
        try:
            with open("./data/twitter/tweets", "r+") as f:
                tws = f.readlines()
                for tweet in tweets.data:
                    if f"{tweet.id}\n" not in tws:
                        f.write(str(tweet.id) + "\n")
                        message = "https://twitter.com/Play_KINGsRAID/status/" + str(
                            tweet.id
                        )
                        msg = "New tweet found: " + message
                        logging.info(msg)
                        print(msg)
                        try:
                            tweet = self.api.get_tweet(
                                tweet.id,
                                tweet_fields=["created_at"],
                                media_fields=["url"],
                                expansions="attachments.media_keys",
                            )
                            embed = discord.Embed(
                                title="Tweet",
                                url=message,
                                description=tweet.data.text,
                                colour=discord.Colour.from_rgb(29, 161, 242),
                            )
                            embed.set_footer(
                                text="Twitter",
                                icon_url="https://cdn.discordapp.com/attachments/865652402706972682/978702740786151424/Twitter-logo.svg.png",
                            )
                            embed.set_author(
                                name="KING's RAID OFFICIAL (@Play_KINGsRAID)",
                                url="https://twitter.com/Play_KINGsRAID",
                                icon_url="https://pbs.twimg.com/profile_images/1452700303845781504/BBNcSveS.jpg",
                            )
                            if tweet.includes["media"][0].url:
                                embed.set_image(url=tweet.includes["media"][0].url)
                            if tweet.data.created_at:
                                embed.timestamp = tweet.data.created_at
                        except:
                            traceback.print_exc()
                            pass
                        for key in self.channels:
                            if self.channels[key]:
                                chan = self.client.get_channel(int(key))
                                try:
                                    if isinstance(chan, discord.abc.GuildChannel):
                                        attemp = f" | TWITTER attempting to send to channel #{key}"
                                        logging.info(attemp)
                                        print(attemp)
                                        try:
                                            await chan.send(embed=embed)
                                        except:
                                            await chan.send(message)
                                        success = f" | TWITTER successfully sent to #{chan.name} on {chan.guild.name}"
                                        logging.info(success)
                                        print(success)
                                    else:
                                        invalid = f" | TWITTER channel #{key} is invalid, removing"
                                        logging.info(invalid)
                                        print(invalid)
                                        self.channels[key] = False
                                        self.write_channels()
                                except discord.errors.Forbidden as r:
                                    forbidden = f" | FORBIDDEN: {str(r)} | Channel: #{chan.name} on {chan.guild.name}"
                                    logging.warn(forbidden)
                                    print(forbidden)
                                except Exception as e:
                                    logging.warn(e)
        except FileNotFoundError:
            with open("./data/twitter/tweets", "a") as r:
                for id_ in tweets_id:
                    r.write(str(id_) + "\n")
        except Exception as e:
            logging.warn(e)

    @twitter_.before_loop
    async def before_twitter_(self):
        await self.client.wait_until_ready()

    def write_channels(self):
        with open(self.channel_path, "w") as f:
            f.write(json.dumps(self.channels))


def write_channels(channel_path, channels):
    with open(channel_path, "w", encoding="utf-8") as json_data:
        json_data.write(json.dumps(channels))


def setup(client):
    client.add_cog(KingsRaidAnnounce(client))
