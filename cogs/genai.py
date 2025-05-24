import discord
import os
import config
from dotenv import load_dotenv
from google import genai
from discord.ext import commands

load_dotenv()
client = genai.Client(api_key=os.getenv('GENAI_KEY'))

class GenAI(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def summarize(self, ctx, history_length: int = 100):
        bot_msg = await ctx.reply("Summarizing the conversation...")
        try:
            messages = [message async for message in ctx.channel.history(limit=history_length)]
            text = "\n".join([msg.author.display_name + ": " + msg.content for msg in messages if not msg.author.bot])
            if not text:
                await bot_msg.edit(content="No messages to summarize.")
                return
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents="Tóm tắt cuộc trò chuyện này:" + "\n\n" + text
            )
            embed = discord.Embed(title=f"Summary for Last {str(history_length)} Messages", description=response.text, color=config.embed_color)
            await bot_msg.edit(content="", embed=embed)
        except Exception as e:
            await bot_msg.edit(content=f"An error occurred: {e}")

async def setup(client):
    await client.add_cog(GenAI(client))