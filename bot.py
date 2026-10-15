import os
import asyncio
import aiosqlite
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("PREFIX", "$")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
DB_FILE = "mm_database.db"

async def init_db():
    async with aiosqlite.connect(DB_FILE) as db:
        # All required database schemas mapped to your features
        await db.execute("CREATE TABLE IF NOT EXISTS strikes (user_id INTEGER, guild_id INTEGER, reason TEXT, moderator_id INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")
        await db.execute("CREATE TABLE IF NOT EXISTS blacklist (user_id INTEGER PRIMARY KEY, reason TEXT, moderator_id INTEGER)")
        await db.execute("CREATE TABLE IF NOT EXISTS insurance (user_id INTEGER PRIMARY KEY, items TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS vouches (id INTEGER PRIMARY KEY AUTOINCREMENT, target_id INTEGER, author_id INTEGER, guild_id INTEGER, comment TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS levels (user_id INTEGER, guild_id INTEGER, xp INTEGER DEFAULT 0, level INTEGER DEFAULT 0, PRIMARY KEY (user_id, guild_id))")
        await db.execute("CREATE TABLE IF NOT EXISTS config (guild_id INTEGER PRIMARY KEY, prefix TEXT DEFAULT '$', mm_role INTEGER, support_role INTEGER, ticket_admin INTEGER)")
        await db.commit()

@bot.event
async def on_ready():
    await init_db()
    print(f"🚀 [Railway] Fully Featured Bot Online as {bot.user}")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"📦 Loaded extension: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load {cog_name}: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
