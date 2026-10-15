import discord
from discord.ext import commands
import aiosqlite

class Leveling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "mm_database.db"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id)) as cursor:
                row = await cursor.fetchone()
            if row:
                xp, level = row[0] + 10, row[1]
                if xp >= (level + 1) * 100:
                    level += 1
                    await message.channel.send(f"🎉 Congrats {message.author.mention}, you leveled up to **Level {level}**!")
                await db.execute("UPDATE levels SET xp = ?, level = ? WHERE user_id = ? AND guild_id = ?", (xp, level, message.author.id, message.guild.id))
            else:
                await db.execute("INSERT INTO levels VALUES (?, ?, 10, 0)", (message.author.id, message.guild.id))
            await db.commit()

    @commands.command(name="level")
    async def _level(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT xp, level FROM levels WHERE user_id = ? AND guild_id = ?", (target.id, ctx.guild.id)) as cursor:
                row = await cursor.fetchone()
        if not row:
            return await ctx.send(f"📊 **{target}** is Level 0 (0 XP).")
        await ctx.send(f"📊 **{target} Stats:** Level **{row[1]}** | XP **{row[0]}**")

    @commands.command(name="lb", aliases=["leaderboard"])
    async def _lb(self, ctx):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT user_id, level FROM levels WHERE guild_id = ? ORDER BY level DESC LIMIT 10", (ctx.guild.id,)) as cursor:
                rows = await cursor.fetchall()
        msg = "\n".join([f"{i+1}. <@{r[0]}> — Level **{r[1]}**" for i, r in enumerate(rows)])
        await ctx.send(f"🏆 **Server Leaderboard:**\n{msg}")

    @commands.command(name="roleadd")
    @commands.has_permissions(manage_roles=True)
    async def _roleadd(self, ctx, member: discord.Member, role: discord.Role):
        await member.add_roles(role)
        await ctx.send(f"✅ Added role `{role.name}` to **{member}**.")

    @commands.command(name="removerole")
    @commands.has_permissions(manage_roles=True)
    async def _removerole(self, ctx, member: discord.Member, role: discord.Role):
        await member.remove_roles(role)
        await ctx.send(f"🗑️ Removed role `{role.name}` from **{member}**.")

async def setup(bot):
    await bot.add_cog(Leveling(bot))
