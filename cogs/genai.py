import discord, os, config
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
        """Summarize the conversation using GenAI."""
        try:
            bot_msg = await ctx.reply("Summarizing the conversation...")
            messages = [message async for message in ctx.channel.history(limit=history_length)]
            text = "\n".join([msg.author.display_name + ": " + msg.content for msg in messages if not msg.author.bot])
            if not text:
                await ctx.reply("No messages to summarize.")
                return
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents="Tóm tắt cuộc trò chuyện này:" + "\n\n" + text
            )
            embed = discord.Embed(title=f"Conversation Summary for {str(history_length)} Last Messages", description=response.text, color=config.embed_color)
            await bot_msg.edit(content="", embed=embed)
        except Exception as e:
            await ctx.reply(f"An error occurred: {e}")

async def setup(client):
    await client.add_cog(GenAI(client))