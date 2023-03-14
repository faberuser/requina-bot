import asyncio, os, re, config, discord
from discord.ext import commands
from EdgeGPT import Chatbot, ConversationStyle

os.environ["COOKIE_FILE"] = "./cookies.json"


class BingAI(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.bot = Chatbot()

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.content.lower().startswith("bing "):
            prompt = msg.content.replace("bing ", "")
            if prompt.lower() == "reset":
                async with msg.channel.typing():
                    await self.bot.reset()
                    await msg.reply("The conversation has been reset")
                return
            async with msg.channel.typing():
                embed, button_texts = await self.bingai(prompt)
                view = await self.create_view(button_texts)
                await msg.reply(embed=embed, view=view)

    async def create_view(self, button_texts: list):
        view = discord.ui.View()
        for i in range(len(button_texts)):
            button = await self.create_button(button_texts[i])
            view.add_item(button)
        return view

    async def create_button(self, button_texts):
        button = discord.ui.Button(
            label=button_texts[0], style=discord.ButtonStyle.blurple
        )

        async def button_callback(interaction):
            await interaction.response.defer(thinking=True)
            embed, _button_texts = await self.bingai(button_texts[1])
            view = await self.create_view(_button_texts)
            await interaction.followup.send(embed=embed, view=view)

        button.callback = button_callback
        return button

    async def bingai(self, prompt):
        while True:
            try:
                response = await self.bot.ask(prompt=prompt)
                if response["item"]["firstNewMessageIndex"] == None:
                    await self.bot.reset()
                    continue
                break
            except:
                continue

        capped = False
        if response["item"]["messages"][1]["contentOrigin"] == "TurnLimiter":
            capped = True
            await self.bot.reset()
            response = await self.bot.ask(prompt=prompt)

        try:
            msg_text = self.filter_msg_text(response)
            learn_more, suggested_response, suggested_response_list = self.get_lm_sr(
                response, msg_text
            )
        except KeyError:
            msg_text = response["item"]["messages"][1]["adaptiveCards"][0]["body"][0][
                "text"
            ]
            learn_more = ""
            suggested_response = ""
            suggested_response_list = []

        if capped:
            embed = discord.Embed(
                description="*The max number of messages in the previous conversation has been reached, the response below is in the new conversation:*\n\n"
                + msg_text,
                color=config.embed_color,
            )
        else:
            embed = discord.Embed(
                description=msg_text,
                color=config.embed_color,
            )
        embed.set_author(name=prompt)
        embed.set_footer(text="Select suggested responses:")
        if learn_more != "":
            embed.add_field(name="Learn more:", value=learn_more)
        if suggested_response != "":
            embed.add_field(name="Suggested responses:", value=suggested_response)
        embed.add_field(
            name="Throttling:",
            value="`"
            + str(response["item"]["throttling"]["numUserMessagesInConversation"])
            + "/"
            + str(response["item"]["throttling"]["maxNumUserMessagesInConversation"])
            + "`\nSend `bing reset` to reset the conversation",
        )
        return embed, suggested_response_list

    def filter_msg_text(self, response):
        try:
            msg_text = response["item"]["messages"][1]["text"]
        except KeyError:
            raise KeyError
        mark_matches = re.findall(r"\[([0-9^]+)\]", msg_text, re.DOTALL)
        for match in mark_matches:
            msg_text = msg_text.replace(match, match.replace("^", ""))
        return msg_text

    def get_lm_sr(self, response, msg_text):
        learn_more = ""
        suggested_response = ""
        suggested_response_list = []
        try:
            learn_more = (
                response["item"]["messages"][1]["adaptiveCards"][0]["body"][1]["text"]
                .replace("Learn more: ", "")
                .replace(") [", ")\n[")
            )
        except:
            pass
        try:
            sgt_res = response["item"]["messages"][1]["suggestedResponses"]
            count = 1
            for sgt_re in sgt_res:
                suggested_response += str(count) + ". " + sgt_re["text"] + "\n"
                suggested_response_list.append([str(count), sgt_re["text"]])
                count += 1
        except KeyError:
            pass
        return learn_more, suggested_response, suggested_response_list


async def setup(client):
    await client.add_cog(BingAI(client))
