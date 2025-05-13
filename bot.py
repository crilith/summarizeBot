# bot.py
import os
import discord
import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_TOKEN = os.getenv('GEMINI_TOKEN')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Configure Gemini AI
genai.configure(api_key=GEMINI_TOKEN)
#model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')

# Create bot instance with command prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.command()
async def summarize(ctx, hours: int):
    """Summarize channel history using Gemini AI"""
    try:
        # Calculate time threshold
        time_threshold = datetime.datetime.now() - datetime.timedelta(hours=hours)

        # Fetch messages
        messages = []
        async for message in ctx.channel.history(limit=None, after=time_threshold):
            messages.append(f"{message.author.name} ({message.created_at}): {message.content}")

        # Prepare prompt
        prompt = f"Summarize the following chat history from the last {hours} hours:\n\n" + "\n".join(
            messages[-500:])  # Limit to last 500 messages
        prompt += "\n\nCombine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:. Output the 10 most important points of the content as a list with no more than 16 words per point into a section called MAIN POINTS:."

        # Generate summary
        response = model.generate_content(prompt)
        summary = response.text

        # Send response
        await ctx.author.send(f"**Summary of last {hours}h in #{ctx.channel.name}:**\n{summary}")

    except Exception as e:
        await ctx.send(f"Error: {str(e)}")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
