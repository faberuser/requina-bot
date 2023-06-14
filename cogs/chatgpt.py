import os
from dotenv import load_dotenv
import config
from discord.ext import commands
from revChatGPT.V1 import Chatbot

load_dotenv()
chatbot = Chatbot(config={
    "access_token": os.getenv('CHATGPT_TOKEN'),
    "model": "gpt-4",
})


class ChatGPT(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower().startswith(("chatgpt ", "gpt ")):
            async with message.channel.typing():
                response = ""
                for data in chatbot.ask(message.content, conversation_id=config.chatgpt_conversation):
                    response = data["message"]
                await message.reply(response)


async def setup(client):
    await client.add_cog(ChatGPT(client))
