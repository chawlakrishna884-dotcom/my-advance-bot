import discord
from discord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serversetup")
    @commands.has_permissions(administrator=True)
    async def _serversetup(self, ctx):
        await ctx.send("⚙️ Initializing automated server roles & channels setup...")

    @commands.command(name="setprefix")
    @commands.has_permissions(administrator=True)
    async def _setprefix(self, ctx, prefix: str):
        await ctx.send(f"✅ Bot prefix updated to `{prefix}`.")

async def setup(bot):
    await bot.add_cog(Config(bot))
