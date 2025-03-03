import discord
from discord.ext import commands
from discord import app_commands

class HelpDropdown(discord.ui.Select):
    """Dropdown to select a help category and get detailed explanation."""
    
    def __init__(self, bot, ctx, language="English"):
        self.bot = bot
        self.ctx = ctx
        self.language = language  # Store the selected language

        # Get all available categories
        self.categories = self.get_categories()
        
        # Dropdown options
        options = [
            discord.SelectOption(label=category, description=f"View commands for {category}") 
            for category in self.categories
        ]
        
        super().__init__(placeholder="📂 Select a command category...", options=options)

    def get_categories(self):
        """Fetches all command categories dynamically from bot cogs."""
        categories = set()
        for command in self.bot.commands:
            if command.cog_name:
                categories.add(command.cog_name)
        return sorted(categories)

    async def callback(self, interaction: discord.Interaction):
        """Handles category selection and displays detailed help."""
        selected_category = self.values[0]  # Get selected category
        embed = discord.Embed(
            title=f"📂 {selected_category} Commands",
            color=discord.Color.blue()
        )

        commands_list = [cmd for cmd in self.bot.commands if cmd.cog_name == selected_category]
        
        for cmd in commands_list:
            if self.language == "Hindi":
                embed.add_field(name=f"`lx {cmd.name}`", value=f"🔹 {self.translate_help(cmd.help)}", inline=False)
            else:
                embed.add_field(name=f"`lx {cmd.name}`", value=f"🔹 {cmd.help or 'No description available'}", inline=False)

        await interaction.response.edit_message(embed=embed, view=None)  # Update message with selected help

    def translate_help(self, text):
        """Translates command descriptions into Hindi (English font)."""
        translations = {
            "📜 Opens an interactive help menu.": "📜 Ek interactive help menu kholta hai.",
            "🔒 Restrict the VC where the admin is currently in.": "🔒 Admin jis VC me hai, use lock karein.",
            "🔓 Unrestrict the VC where the admin is currently in.": "🔓 VC ka restriction hatayein.",
            "✅ Allow a user to join restricted VCs.": "✅ Kisi user ko restricted VC me enter karne ki permission de.",
            "❌ Remove a user's access to restricted VCs.": "❌ Kisi user ki VC access hatao.",
            "👥 Show a list of users allowed in restricted VCs.": "👥 Restricted VC ke allowed users ki list dekhein."
        }
        return translations.get(text, text)


class LanguageDropdown(discord.ui.Select):
    """Dropdown to select language before help starts."""
    
    def __init__(self, bot, ctx):
        self.bot = bot
        self.ctx = ctx
        
        options = [
            discord.SelectOption(label="English", description="Get help in English"),
            discord.SelectOption(label="Hindi-English", description="Maddad Hindi me (English font)")
        ]
        
        super().__init__(placeholder="🌍 Select a language...", options=options)

    async def callback(self, interaction: discord.Interaction):
        """Handles language selection and starts help session."""
        selected_language = "Hindi" if self.values[0] == "Hindi-English" else "English"
        
        embed = discord.Embed(
            title="📜 Help Menu",
            description="📂 Select a category below to view commands.",
            color=discord.Color.green()
        )

        await interaction.response.edit_message(embed=embed, view=HelpView(self.bot, self.ctx, selected_language))


class HelpView(discord.ui.View):
    """Creates an interactive help menu with a language selector and dropdown."""
    
    def __init__(self, bot, ctx, language="English"):
        super().__init__(timeout=120)  # 2-minute timeout
        self.add_item(HelpDropdown(bot, ctx, language))

    async def on_timeout(self):
        """Closes the interaction if user doesn't respond in 2 minutes."""
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="⏳ Help session timed out!", view=None)


class LanguageView(discord.ui.View):
    """Creates an interactive menu to select language before showing help options."""
    
    def __init__(self, bot, ctx):
        super().__init__(timeout=120)  # 2-minute timeout
        self.add_item(LanguageDropdown(bot, ctx))

    async def on_timeout(self):
        """Closes the interaction if user doesn't respond in 2 minutes."""
        for child in self.children:
            child.disabled = True
        await self.message.edit(content="⏳ Help session timed out!", view=None)


class HelpCog(commands.Cog):
    """📜 Help System - Provides categorized help using an interactive dropdown with language selection."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="📜 Opens an interactive help menu.")
    async def help_command(self, ctx):
        """Sends the help menu with language selection and interactive dropdown for choosing categories."""
        embed = discord.Embed(
            title="🌍 Select a Language",
            description="Please choose your preferred language for help.",
            color=discord.Color.green()
        )

        message = await ctx.send(embed=embed, view=LanguageView(self.bot, ctx))
        LanguageView(self.bot, ctx).message = message  # Store message for timeout edits

    @app_commands.command(name="help", description="📜 Opens an interactive help menu.")
    async def slash_help_command(self, interaction: discord.Interaction):
        """Slash command version of the interactive help menu."""
        embed = discord.Embed(
            title="🌍 Select a Language",
            description="Please choose your preferred language for help.",
            color=discord.Color.green()
        )

        message = await interaction.response.send_message(embed=embed, view=LanguageView(self.bot, interaction), ephemeral=True)
        LanguageView(self.bot, interaction).message = message  # Store message for timeout edits


async def setup(bot):
    await bot.add_cog(HelpCog(bot))
