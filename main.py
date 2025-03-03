import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv  # Load environment variables

# Load the .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  # Fetch token from .env

# Enable Required Intents
intents = discord.Intents.default()
intents.message_content = True  # Required for text commands
intents.voice_states = True  # Required for music commands
intents.guilds = True  # Ensures the bot can see servers

# Set Up Bot
bot = commands.Bot(command_prefix="lx ", intents=intents, help_command=None)

# Event: When Bot is Ready
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    await bot.tree.sync()  # Ensure slash commands are synced

# Load Cogs Dynamically
async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"✅ Loaded {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load {cog_name}: {e}")

# Sync Slash Commands
@bot.command()
@commands.is_owner()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("✅ Slash commands synced!")

# Proper Async Handling
async def main():
    async with bot:
        await load_extensions()
        await bot.start(DISCORD_TOKEN)

# Start Bot with Proper Async Handling
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        print("⚠ Event loop already running. Switching to alternative method.")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("🛑 Bot shutdown initiated.")
