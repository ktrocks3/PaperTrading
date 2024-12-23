import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # Add your bot token to .env
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # Add your channel ID to .env

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# Function to send a message to a specific channel
async def send_discord_message(channel_id, message):
    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)
    else:
        print("Channel not found!")


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

    # Example message
    message = "Trade Bot is online and ready to send notifications!"
    await send_discord_message(DISCORD_CHANNEL_ID, message)


# Run the bot
bot.run(DISCORD_TOKEN)
