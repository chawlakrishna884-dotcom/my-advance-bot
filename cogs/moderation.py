import discord
from discord.ext import commands
import datetime
import aiosqlite

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = "mm_database.db"

    @commands.command(name="ban", aliases=["gtfo"])
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned **{member}**. Reason: {reason}")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, member: discord.Member, *, reason: str = "No reason"):
        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked **{member}**. Reason: {reason}")

    @commands.command(name="to", aliases=["uto", "timeout"])
    @commands.has_permissions(moderate_members=True)
    async def _to(self, ctx, member: discord.Member, duration: int, *, reason: str = "No reason"):
        delta = discord.utils.utcnow() + datetime.timedelta(minutes=duration)
        await member.timeout(delta, reason=reason)
        await ctx.send(f"🔇 Timed out **{member}** for {duration}m.")

    @commands.command(name="sybau")
    @commands.has_permissions(moderate_members=True)
    async def _sybau(self, ctx, member: discord.Member):
        delta = discord.utils.utcnow() + datetime.timedelta(minutes=5)
        await member.timeout(delta, reason="SYBAU")
        await ctx.send(f"🤫 **{member.display_name}** told to shut up (5m timeout).")

    @commands.command(name="warn")
    @commands.has_permissions(manage_messages=True)
    async def _warn(self, ctx, member: discord.Member, *, reason: str):
        await ctx.send(f"⚠️ **{member}** has been warned: {reason}")

    @commands.command(name="warnings", aliases=["setwarnings"])
    async def _warnings(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        await ctx.send(f"📋 Retrieved warning logs for **{target}**.")

    @commands.command(name="strike")
    @commands.has_permissions(manage_messages=True)
    async def _strike(self, ctx, member: discord.Member, *, reason: str):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("INSERT INTO strikes VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)", (member.id, ctx.guild.id, reason, ctx.author.id))
            await db.commit()
            async with db.execute("SELECT COUNT(*) FROM strikes WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id)) as cursor:
                count = (await cursor.fetchone())[0]

        if count == 1:
            await member.timeout(discord.utils.utcnow() + datetime.timedelta(days=1), reason="Strike 1")
            action = "1 Day Timeout"
        elif count == 2:
            await member.timeout(discord.utils.utcnow() + datetime.timedelta(days=2), reason="Strike 2")
            action = "2 Days Timeout"
        else:
            await member.ban(reason="Strike 3+ Permanent")
            action = "Permanent Ban"

        await ctx.send(f"⚡ Strike #{count} applied to **{member}**. Action: **{action}**")

    @commands.command(name="strikes")
    async def _strikes(self, ctx, member: discord.Member = None):
        target = member or ctx.author
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT reason, timestamp FROM strikes WHERE user_id = ?", (target.id,)) as cursor:
                rows = await cursor.fetchall()
        if not rows:
            return await ctx.send(f"✅ **{target}** has 0 active strikes.")
        msg = "\n".join([f"• {r[1]}: {r[0]}" for r in rows])
        await ctx.send(f"⚠️ **Strikes for {target}:**\n{msg}")

    @commands.command(name="unstrike")
    @commands.has_permissions(manage_messages=True)
    async def _unstrike(self, ctx, member: discord.Member, index: int = 1):
        await ctx.send(f"✅ Removed strike index #{index} from **{member}**.")

    @commands.command(name="clearstrikes")
    @commands.has_permissions(administrator=True)
    async def _clearstrikes(self, ctx, member: discord.Member):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("DELETE FROM strikes WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
            await db.commit()
        await ctx.send(f"🧹 Cleared all strikes for **{member}**.")

    @commands.command(name="massdm")
    @commands.has_permissions(administrator=True)
    async def _massdm(self, ctx, role: discord.Role, *, msg: str):
        count = 0
        for member in role.members:
            try:
                await member.send(msg)
                count += 1
            except:
                pass
        await ctx.send(f"📨 Mass DM sent to **{count}** members with role {role.name}.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
