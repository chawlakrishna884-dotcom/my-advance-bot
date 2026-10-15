import discord
from discord.ext import commands
import aiosqlite

class Vouches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "mm_database.db"

    @commands.command(name="vouch")
    async def _vouch(self, ctx, member: discord.Member):
        if member.id == ctx.author.id:
            return await ctx.send("❌ You cannot vouch yourself.")
        async with aiosqlite.connect(self.db) as db:
            await db.execute("INSERT INTO vouches (target_id, author_id, guild_id, comment) VALUES (?, ?, ?, 'Trusted MM')", (member.id, ctx.author.id, ctx.guild.id))
            await db.commit()
        await ctx.send(f"⭐ Successfully vouched for **{member}**!")

    @commands.command(name="vouches")
    async def _vouches(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT COUNT(*) FROM vouches WHERE target_id = ?", (target.id,)) as cursor:
                count = (await cursor.fetchone())[0]
        await ctx.send(f"⭐ **{target}** has **{count}** vouches.")

    @commands.command(name="topvouches")
    async def _topvouches(self, ctx):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT target_id, COUNT(*) as c FROM vouches GROUP BY target_id ORDER BY c DESC LIMIT 5") as cursor:
                rows = await cursor.fetchall()
        msg = "\n".join([f"{i+1}. <@{r[0]}> — **{r[1]}** vouches" for i, r in enumerate(rows)])
        await ctx.send(f"🏆 **Top Middlemen Leaderboard:**\n{msg}")

    @commands.command(name="autovouch")
    @commands.has_permissions(administrator=True)
    async def _autovouch(self, ctx):
        await ctx.send("✅ Auto-vouch system enabled.")

    @commands.command(name="autovouchstop")
    @commands.has_permissions(administrator=True)
    async def _autovouchstop(self, ctx):
        await ctx.send("❌ Auto-vouch system disabled.")

async def setup(bot):
    await bot.add_cog(Vouches(bot))
