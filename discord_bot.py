import discord
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

# Initialize Discord client
intents = discord.Intents.default()
client = discord.Client(intents=intents)
MESSAGE = ""


async def send_discord_message(message):
    """
    Function to send a message to a Discord channel.
    """
    global MESSAGE
    MESSAGE = message
    await client.start(DISCORD_TOKEN)  # Start the bot


@client.event
async def on_ready():
    """
    Event handler for when the bot is ready.
    """
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(MESSAGE)
        print(f"Message sent: {MESSAGE}")
    else:
        print(f"Channel with ID {DISCORD_CHANNEL_ID} not found!")
    await client.close()  # Close the client after sending the message


if __name__ == "__main__":
    # Use asyncio to run the async function
    asyncio.run(send_discord_message("Bababooey"))
