import discord
from discord.ext import commands

class Mercy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="vacation")
    async def _vacation(self, ctx, duration: str):
        await ctx.send(f"🌴 Staff member **{ctx.author.mention}** is now on vacation for `{duration}`.")

    @commands.command(name="cancelvacation")
    async def _cancelvacation(self, ctx):
        await ctx.send(f"☀️ Staff member **{ctx.author.mention}** is back from vacation.")

async def setup(bot):
    await bot.add_cog(Mercy(bot))
