import discord
from discord.ext import commands
from discord import app_commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", help="Check bot latency")
    async def ping_prefix(self, ctx):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"🔹 **Latency:** `{latency}ms`",
            color=discord.Color.blue()
        )
        if self.bot.user and self.bot.user.avatar:
            avatar_url = self.bot.user.avatar.url
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text="Bot Latency Checker", icon_url=avatar_url)
        else:
            embed.set_footer(text="Bot Latency Checker")
        
        await ctx.send(embed=embed)

    @app_commands.command(name="ping", description="Check bot latency")
    async def ping_slash(self, interaction: discord.Interaction):
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"🔹 **Latency:** `{latency}ms`",
            color=discord.Color.blue()
        )
        if self.bot.user and self.bot.user.avatar:
            avatar_url = self.bot.user.avatar.url
            embed.set_thumbnail(url=avatar_url)
            embed.set_footer(text="Bot Latency Checker", icon_url=avatar_url)
        else:
            embed.set_footer(text="Bot Latency Checker")
        
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(PingCog(bot))
