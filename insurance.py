import discord
from discord.ext import commands
import aiosqlite

class Insurance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "mm_database.db"

    @commands.command(name="insurance")
    async def _insurance(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT items FROM insurance WHERE user_id = ?", (target.id,)) as cursor:
                row = await cursor.fetchone()
        if not row:
            return await ctx.send(f"🛡️ **{target}** has no active insurance.")
        await ctx.send(f"🛡️ **Insurance Items for {target}:**\n{row[0]}")

    @commands.command(name="setinsurance")
    @commands.has_permissions(manage_roles=True)
    async def _setinsurance(self, ctx, member: discord.Member, *, items: str):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("INSERT OR REPLACE INTO insurance VALUES (?, ?)", (member.id, items))
            await db.commit()
        await ctx.send(f"🛡️ Set insurance items for **{member}**.")

    @commands.command(name="removeinsurance")
    @commands.has_permissions(manage_roles=True)
    async def _removeinsurance(self, ctx, member: discord.Member):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("DELETE FROM insurance WHERE user_id = ?", (member.id,))
            await db.commit()
        await ctx.send(f"🗑️ Removed insurance from **{member}**.")

async def setup(bot):
    await bot.add_cog(Insurance(bot))
