import discord
from discord.ext import commands

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="fakelog")
    @commands.has_permissions(administrator=True)
    async def _fakelog(self, ctx):
        await ctx.send("🧪 Triggering fake logging test simulation...")

    @commands.command(name="anwhitelist")
    @commands.has_permissions(administrator=True)
    async def _anwhitelist(self, ctx, member: discord.Member):
        await ctx.send(f"🛡️ **{member}** added to anti-nuke whitelist.")

async def setup(bot):
    await bot.add_cog(Logs(bot))
