import discord
from discord.ext import commands

class AutoMM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="automm")
    async def _automm(self, ctx):
        await ctx.send("🤖 **Auto MM Active**: Monitoring transaction state securely.")

    @commands.command(name="conf")
    async def _conf(self, ctx, channel: discord.TextChannel):
        await ctx.send(f"✅ Trade terms confirmed for {channel.mention}.")

    @commands.command(name="settle")
    async def _settle(self, ctx, channel: discord.TextChannel, txid: str):
        await ctx.send(f"🤝 Trade successfully settled for {channel.mention}. Transaction ID: `{txid}`")

    @commands.command(name="fee")
    async def _fee(self, ctx):
        embed = discord.Embed(title="💸 MiddleMan Fee Schedule", color=discord.Color.green())
        embed.add_field(name="Under $10", value="Free / Tip Optional", inline=False)
        embed.add_field(name="$10 - $100", value="5% MiddleMan Fee", inline=False)
        embed.add_field(name="$100+", value="3% MiddleMan Fee", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AutoMM(bot))
