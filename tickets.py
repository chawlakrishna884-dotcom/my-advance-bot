import discord
from discord.ext import commands
import asyncio

class TicketControls(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Close Ticket", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Closing channel in 3 seconds...", ephemeral=True)
        await asyncio.sleep(3)
        await interaction.channel.delete()

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="panel", aliases=["support"])
    @commands.has_permissions(administrator=True)
    async def _panel(self, ctx):
        embed = discord.Embed(title="Roblox MiddleMan Support Panel", description="Click below to open a secure transaction ticket.", color=discord.Color.blue())
        view = discord.ui.View(timeout=None)
        
        async def callback(interaction: discord.Interaction):
            ch = await interaction.guild.create_text_channel(f"mm-{interaction.user.name}")
            await ch.set_permissions(interaction.guild.default_role, read_messages=False)
            await ch.set_permissions(interaction.user, read_messages=True, send_messages=True)
            await ch.send(f"Welcome {interaction.user.mention}! Staff will assist shortly.", view=TicketControls())
            await interaction.response.send_message(f"✅ Ticket created: {ch.mention}", ephemeral=True)

        btn = discord.ui.Button(label="🎫 Open MM Ticket", style=discord.ButtonStyle.success)
        btn.callback = callback
        view.add_item(btn)
        await ctx.send(embed=embed, view=view)

    @commands.command(name="claim")
    async def _claim(self, ctx):
        await ctx.send(f"📌 Ticket claimed by **{ctx.author.mention}**.")

    @commands.command(name="unclaim")
    async def _unclaim(self, ctx):
        await ctx.send(f"📌 Ticket unclaimed by **{ctx.author.mention}**.")

    @commands.command(name="close", aliases=["resolve"])
    async def _close(self, ctx):
        await ctx.send("🔒 Closing ticket...")
        await asyncio.sleep(2)
        await ctx.channel.delete()

    @commands.command(name="hold")
    async def _hold(self, ctx):
        await ctx.send("⏳ Ticket placed on HOLD (Auto-close timer paused).")

    @commands.command(name="rename")
    async def _rename(self, ctx, *, name: str):
        await ctx.channel.edit(name=name)
        await ctx.send(f"✏️ Ticket renamed to `{name}`.")

    @commands.command(name="adduser")
    async def _adduser(self, ctx, member: discord.Member):
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"👤 Added **{member}** to ticket.")

    @commands.command(name="removeuser")
    async def _removeuser(self, ctx, member: discord.Member):
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(f"👤 Removed **{member}** from ticket.")

    @commands.command(name="askuser")
    async def _askuser(self, ctx, user1: discord.Member, user2: discord.Member):
        await ctx.send(f"❓ {user1.mention} & {user2.mention}: Please state the agreed terms of your trade.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
