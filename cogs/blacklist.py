import discord
from discord.ext import commands
import aiosqlite

class Blacklist(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "mm_database.db"

    @commands.command(name="blacklist")
    @commands.has_permissions(administrator=True)
    async def _blacklist(self, ctx, member: discord.Member, *, reason: str = "Scammer"):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("INSERT OR REPLACE INTO blacklist VALUES (?, ?, ?)", (member.id, reason, ctx.author.id))
            await db.commit()
        await ctx.send(f"🚫 **{member}** added to blacklist. Reason: {reason}")

    @commands.command(name="unblacklist")
    @commands.has_permissions(administrator=True)
    async def _unblacklist(self, ctx, user_id: int):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("DELETE FROM blacklist WHERE user_id = ?", (user_id,))
            await db.commit()
        await ctx.send(f"✅ User ID `{user_id}` unblacklisted.")

    @commands.command(name="blacklisted")
    async def _blacklisted(self, ctx):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT user_id, reason FROM blacklist") as cursor:
                rows = await cursor.fetchall()
        if not rows:
            return await ctx.send("ℹ️ Blacklist is currently empty.")
        msg = "\n".join([f"• <@{r[0]}>: {r[1]}" for r in rows])
        await ctx.send(f"🚫 **Global Blacklist:**\n{msg}")

async def setup(bot):
    await bot.add_cog(Blacklist(bot))
