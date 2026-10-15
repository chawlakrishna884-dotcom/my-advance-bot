import discord
from discord.ext import commands
import aiohttp

class Server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo")
    async def _serverinfo(self, ctx):
        embed = discord.Embed(title=ctx.guild.name, color=discord.Color.purple())
        embed.add_field(name="Members", value=ctx.guild.member_count)
        embed.add_field(name="Roles", value=len(ctx.guild.roles))
        await ctx.send(embed=embed)

    @commands.command(name="whois", aliases=["w"])
    async def _whois(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        embed = discord.Embed(title=f"User Info - {target}", color=discord.Color.blue())
        embed.add_field(name="ID", value=target.id)
        embed.add_field(name="Joined Discord", value=target.created_at.strftime("%Y-%m-%d"))
        await ctx.send(embed=embed)

    @commands.command(name="steal")
    @commands.has_permissions(manage_emojis=True)
    async def _steal(self, ctx, url: str, name: str = "emoji"):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    emoji = await ctx.guild.create_custom_emoji(name=name, image=data)
                    await ctx.send(f"✅ Steal successful: <:{emoji.name}:{emoji.id}>")

async def setup(bot):
    await bot.add_cog(Server(bot))
