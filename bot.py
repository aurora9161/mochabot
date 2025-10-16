#!/usr/bin/env python3
"""
MochaBot - An Advanced Coffee-Themed Discord Bot for Mental Health & Therapy
Designed for community management, mental wellness, and therapeutic support
Created by: aurora9161

Combining the comfort of coffee culture with mental health resources,
this bot provides a safe, supportive environment for community wellness.
"""

import discord
from discord.ext import commands, tasks
import asyncio
import os
from datetime import datetime, timedelta
import random
import json
from typing import Optional
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_PREFIX = '!'
BOT_VERSION = "2.1.0"  # Updated for mental health features
BOT_COLOR = 0x8B4513  # Coffee brown color

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


class MochaHelpCommand(commands.HelpCommand):
    """Custom help command with beautiful embeds and coffee + mental health theme"""
    
    def __init__(self):
        super().__init__()
        self.verify_checks = False
        self.show_hidden = False
    
    def get_command_signature(self, command):
        """Get the command signature with proper formatting"""
        return f'{self.context.clean_prefix}{command.qualified_name} {command.signature}'
    
    async def send_bot_help(self, mapping):
        """Send the main help page with all categories"""
        embed = discord.Embed(
            title="☕ MochaBot Help Menu",
            description=f"**Welcome to MochaBot v{BOT_VERSION}**\n\n*Your friendly coffee-themed companion for mental wellness and community support!*\n\n**🎯 Purpose:** Combining coffee culture with mental health resources\n**📞 Crisis Support:** Use `{self.context.clean_prefix}crisis` for emergency resources\n**Prefix:** `{self.context.clean_prefix}`\n\n**🔍 Quick Navigation:**\nUse `{self.context.clean_prefix}help <category>` or `{self.context.clean_prefix}help <command>` for detailed information.",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        # Add bot avatar as thumbnail
        if self.context.bot.user.avatar:
            embed.set_thumbnail(url=self.context.bot.user.avatar.url)
        
        # Filter and organize commands by cogs
        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            if not filtered:
                continue
                
            cog_name = getattr(cog, 'qualified_name', 'General')
            cog_emoji = getattr(cog, 'emoji', '📋')
            cog_description = getattr(cog, 'description', 'Various commands')
            
            # Count commands and show preview
            command_count = len(filtered)
            command_preview = ', '.join([cmd.name for cmd in filtered[:3]])
            if command_count > 3:
                command_preview += f" and {command_count - 3} more..."
            
            embed.add_field(
                name=f"{cog_emoji} {cog_name} ({command_count} commands)",
                value=f"{cog_description}\n**Commands:** {command_preview}",
                inline=True
            )
        
        # Add useful information
        embed.add_field(
            name="🔗 Resources",
            value="[Support Server](https://discord.gg/example) | [GitHub](https://github.com/aurora9161/mochabot) | [Mental Health Resources](https://www.nami.org/)",
            inline=False
        )
        
        embed.add_field(
            name="🆘 Need Help?",
            value=f"Mental Health Crisis: `{self.context.clean_prefix}crisis`\nDaily Check-in: `{self.context.clean_prefix}checkin`\nBreathing Exercise: `{self.context.clean_prefix}breathe`",
            inline=False
        )
        
        embed.set_footer(
            text=f"Requested by {self.context.author} | MochaBot v{BOT_VERSION} | You matter 💙",
            icon_url=self.context.author.avatar.url if self.context.author.avatar else None
        )
        
        # Add reaction buttons for navigation
        view = HelpMenuView(self.context, mapping)
        await self.get_destination().send(embed=embed, view=view)
    
    async def send_command_help(self, command):
        """Send help for a specific command"""
        embed = discord.Embed(
            title=f"☕ Command: {command.name}",
            description=command.help or "No description available",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📝 Usage",
            value=f"`{self.get_command_signature(command)}`",
            inline=False
        )
        
        if command.aliases:
            embed.add_field(
                name="🔄 Aliases",
                value=", ".join([f"`{alias}`" for alias in command.aliases]),
                inline=True
            )
        
        if hasattr(command, 'cooldown') and command.cooldown:
            embed.add_field(
                name="⏱️ Cooldown",
                value=f"{command.cooldown.rate} uses per {command.cooldown.per}s",
                inline=True
            )
        
        # Show cog information
        if command.cog:
            embed.add_field(
                name="📂 Category",
                value=command.cog.qualified_name,
                inline=True
            )
        
        # Add mental health note for relevant commands
        if command.cog and hasattr(command.cog, 'emoji') and command.cog.emoji == '🧠':
            embed.add_field(
                name="💙 Note",
                value="This is a mental health support command. Please use it in a safe, private space if needed.",
                inline=False
            )
        
        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help for more commands | Remember: You're not alone 💙",
            icon_url=self.context.bot.user.avatar.url if self.context.bot.user.avatar else None
        )
        
        await self.get_destination().send(embed=embed)
    
    async def send_cog_help(self, cog):
        """Send help for a specific cog/category"""
        embed = discord.Embed(
            title=f"{getattr(cog, 'emoji', '📋')} {cog.qualified_name} Commands",
            description=cog.description or "No description available",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        commands_list = await self.filter_commands(cog.get_commands(), sort=True)
        
        if commands_list:
            for command in commands_list:
                embed.add_field(
                    name=f"`{self.context.clean_prefix}{command.name}`",
                    value=command.short_doc or "No description",
                    inline=True
                )
        else:
            embed.add_field(
                name="❌ No Commands",
                value="This category has no available commands.",
                inline=False
            )
        
        # Add special note for mental health cog
        if hasattr(cog, 'emoji') and cog.emoji == '🧠':
            embed.add_field(
                name="💙 Remember",
                value="These tools support mental wellness but don't replace professional help. If you're in crisis, please reach out to a mental health professional or use `!crisis` for emergency resources.",
                inline=False
            )
        
        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help <command> for detailed info | You matter 💙",
            icon_url=self.context.bot.user.avatar.url if self.context.bot.user.avatar else None
        )
        
        await self.get_destination().send(embed=embed)
    
    async def send_group_help(self, group):
        """Send help for command groups"""
        embed = discord.Embed(
            title=f"☕ Group: {group.name}",
            description=group.help or "No description available",
            color=BOT_COLOR
        )
        
        embed.add_field(
            name="📝 Usage",
            value=f"`{self.get_command_signature(group)}`",
            inline=False
        )
        
        if group.commands:
            subcommands = await self.filter_commands(group.commands, sort=True)
            if subcommands:
                embed.add_field(
                    name="🔧 Subcommands",
                    value="\n".join([f"`{self.context.clean_prefix}{group.name} {cmd.name}` - {cmd.short_doc or 'No description'}" for cmd in subcommands]),
                    inline=False
                )
        
        await self.get_destination().send(embed=embed)


class HelpMenuView(discord.ui.View):
    """Interactive view for the help menu with mental health focus"""
    
    def __init__(self, ctx, mapping):
        super().__init__(timeout=180.0)
        self.ctx = ctx
        self.mapping = mapping
        self.current_page = 0
    
    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author
    
    @discord.ui.button(label='🏠 Home', style=discord.ButtonStyle.blurple)
    async def home_button(self, interaction, button):
        await interaction.response.defer()
        help_command = MochaHelpCommand()
        help_command.context = self.ctx
        await help_command.send_bot_help(self.mapping)
    
    @discord.ui.button(label='🧠 Mental Health', style=discord.ButtonStyle.green)
    async def mental_health_button(self, interaction, button):
        embed = discord.Embed(
            title="🧠 Mental Health Quick Access",
            description="Immediate access to mental health and wellness resources",
            color=0x87CEEB,  # Sky blue for calm
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="🆘 Crisis Resources",
            value=f"`{self.ctx.clean_prefix}crisis` - Emergency helplines\n`{self.ctx.clean_prefix}therapy` - Find professional help",
            inline=False
        )
        
        embed.add_field(
            name="🌸 Daily Wellness",
            value=f"`{self.ctx.clean_prefix}checkin` - Daily mental health check\n`{self.ctx.clean_prefix}mood <1-10>` - Track your mood\n`{self.ctx.clean_prefix}affirmation` - Positive affirmations",
            inline=False
        )
        
        embed.add_field(
            name="🫁 Coping Tools",
            value=f"`{self.ctx.clean_prefix}breathe` - Breathing exercises\n`{self.ctx.clean_prefix}ground` - Grounding techniques\n`{self.ctx.clean_prefix}selfcare` - Self-care suggestions",
            inline=False
        )
        
        embed.add_field(
            name="💙 Remember",
            value="You're not alone. These tools are here to support you, but please reach out to professionals when needed.",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label='📋 Commands List', style=discord.ButtonStyle.secondary)
    async def commands_list_button(self, interaction, button):
        embed = discord.Embed(
            title="📋 All Commands Quick Reference",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        all_commands = []
        for cog, commands_list in self.mapping.items():
            for cmd in commands_list:
                all_commands.append(f"`{self.ctx.clean_prefix}{cmd.name}`")
        
        command_chunks = [all_commands[i:i+15] for i in range(0, len(all_commands), 15)]
        
        for i, chunk in enumerate(command_chunks[:3]):
            embed.add_field(
                name=f"Commands {i*15+1}-{min((i+1)*15, len(all_commands))}",
                value="\n".join(chunk),
                inline=True
            )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label='ℹ️ Bot Info', style=discord.ButtonStyle.gray)
    async def bot_info_button(self, interaction, button):
        embed = discord.Embed(
            title="ℹ️ MochaBot Information",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name="🤖 Bot Version", value=f"v{BOT_VERSION}", inline=True)
        embed.add_field(name="🐍 Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="⏱️ Uptime", value="Coming Soon", inline=True)
        
        embed.add_field(name="🏠 Servers", value=str(len(self.ctx.bot.guilds)), inline=True)
        embed.add_field(name="👥 Users", value=str(len(self.ctx.bot.users)), inline=True)
        embed.add_field(name="📡 Ping", value=f"{round(self.ctx.bot.latency * 1000)}ms", inline=True)
        
        embed.add_field(
            name="☕ About MochaBot",
            value="A coffee-themed Discord bot designed for community management and mental health support. Combining the comfort of coffee culture with wellness resources and therapeutic tools. Created with love, caffeine, and care for mental health.",
            inline=False
        )
        
        embed.add_field(
            name="🎯 Mission",
            value="To provide a safe, supportive environment where coffee culture meets mental wellness, offering both community engagement and therapeutic resources.",
            inline=False
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    async def on_timeout(self):
        for item in self.children:
            item.disabled = True
        try:
            await self.message.edit(view=self)
        except:
            pass


# Create bot instance with custom help command
bot = commands.Bot(
    command_prefix=BOT_PREFIX,
    intents=intents,
    help_command=MochaHelpCommand(),
    case_insensitive=True,
    strip_after_prefix=True
)


@bot.event
async def on_ready():
    """Bot startup event"""
    logger.info(f'☕ {bot.user} has brewed up and is ready to support your community!')
    logger.info(f'Connected to {len(bot.guilds)} servers with {len(bot.users)} users')
    logger.info('🧠 Mental health resources loaded and ready to help')
    
    # Set bot activity with mental health focus
    activity = discord.Activity(
        type=discord.ActivityType.listening,
        name=f"your mental wellness in {len(bot.guilds)} servers | {BOT_PREFIX}help"
    )
    await bot.change_presence(activity=activity, status=discord.Status.online)
    
    # Start background tasks
    if not daily_wellness_check.is_running():
        daily_wellness_check.start()


@bot.event
async def on_member_join(member):
    """Welcome new members with coffee theme and mental health support info"""
    welcome_messages = [
        f"☕ Welcome to our supportive coffee house, {member.mention}! This is a safe space for community and wellness.",
        f"🌟 {member.mention} just joined our mental wellness café! We're here to support each other.",
        f"☕ A new member has arrived at our wellness community! Welcome, {member.mention}!",
        f"🎉 Welcome {member.mention}! Our community values mental health, coffee culture, and mutual support."
    ]
    
    # Try to find a welcome channel
    welcome_channels = ['welcome', 'general', 'lobby', 'café', 'coffee-house', 'wellness', 'support']
    for channel_name in welcome_channels:
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            embed = discord.Embed(
                title="☕ Welcome to Our Wellness Community!",
                description=random.choice(welcome_messages),
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(
                name="🎯 Get Started",
                value=f"Use `{BOT_PREFIX}help` to see all features\nTry `{BOT_PREFIX}checkin` for daily wellness\nUse `{BOT_PREFIX}crisis` if you need immediate support",
                inline=False
            )
            embed.add_field(
                name="💙 Remember",
                value="This is a supportive community. You matter, and you're not alone here.",
                inline=False
            )
            embed.set_footer(text=f"Member #{len(member.guild.members)} | Your wellbeing matters")
            await channel.send(embed=embed)
            break


@bot.event
async def on_message(message):
    """Process messages and respond to coffee/mental health keywords"""
    if message.author == bot.user:
        return
    
    # Mental health keywords for supportive responses
    mental_health_keywords = ['stress', 'anxiety', 'depression', 'sad', 'worried', 'panic', 'overwhelmed', 'tired', 'exhausted']
    coffee_keywords = ['coffee', 'café', 'espresso', 'latte', 'cappuccino', 'mocha', 'brew']
    
    message_content = message.content.lower()
    
    # Respond to mental health keywords with support
    if any(keyword in message_content for keyword in mental_health_keywords):
        if random.randint(1, 15) == 1:  # 6.7% chance to respond
            supportive_responses = [
                "💙 I notice you might be going through something difficult. Remember, you're not alone.",
                "🫂 Take care of yourself. Try `!breathe` for a calming exercise or `!affirmation` for positivity.",
                "🌸 Your feelings are valid. Consider `!checkin` for reflection or `!crisis` if you need immediate support.",
                "💚 Be gentle with yourself today. Mental health matters just as much as physical health."
            ]
            await message.add_reaction('💙')
            if random.randint(1, 3) == 1:  # 33% of that 6.7%
                await message.reply(random.choice(supportive_responses))
    
    # Respond to coffee keywords
    elif any(keyword in message_content for keyword in coffee_keywords):
        if random.randint(1, 20) == 1:  # 5% chance to respond
            responses = [
                "☕ Coffee and conversation - two of life's simple pleasures!",
                "☕ Nothing like a good cup of coffee to bring people together!",
                "☕ Coffee break = mental health break. Both are important!",
                "☕ The perfect blend: coffee culture meets community support!"
            ]
            await message.add_reaction('☕')
            if random.randint(1, 4) == 1:  # 25% of that 5%
                await message.reply(random.choice(responses))
    
    await bot.process_commands(message)


# Daily Wellness Check Background Task (renamed from coffee_facts)
@tasks.loop(hours=12)  # Every 12 hours
async def daily_wellness_check():
    """Send wellness reminders and mental health tips"""
    wellness_tips = [
        "💙 Remember to check in with yourself today. How are you feeling?",
        "🌸 Take a moment to breathe deeply. Your mental health matters.",
        "☕ Coffee tastes better when you're taking care of your mental wellness too.",
        "🫂 You're not alone. This community is here to support each other.",
        "🌱 Small acts of self-care add up to big improvements in wellbeing.",
        "💚 It's okay to have difficult days. Tomorrow is a new opportunity.",
        "✨ You matter, your feelings are valid, and you deserve support.",
        "🫁 When life feels overwhelming, try a breathing exercise with `!breathe`"
    ]
    
    tip = random.choice(wellness_tips)
    
    # Send to wellness channels
    for guild in bot.guilds:
        wellness_channel_names = ['wellness', 'mental-health', 'support', 'daily-wellness', 'self-care']
        for channel_name in wellness_channel_names:
            channel = discord.utils.get(guild.text_channels, name=channel_name)
            if channel:
                embed = discord.Embed(
                    title="🌸 Daily Wellness Reminder",
                    description=tip,
                    color=0x87CEEB,  # Calming sky blue
                    timestamp=datetime.utcnow()
                )
                embed.add_field(
                    name="🛠️ Quick Tools",
                    value=f"`{BOT_PREFIX}checkin` | `{BOT_PREFIX}breathe` | `{BOT_PREFIX}affirmation` | `{BOT_PREFIX}selfcare`",
                    inline=False
                )
                embed.set_footer(text="MochaBot Wellness • Your mental health matters 💙")
                try:
                    await channel.send(embed=embed)
                    break  # Only send to first matching channel per guild
                except:
                    pass


# Load all cogs including mental health
async def load_cogs():
    """Load all cog files including mental health support"""
    cogs = [
        'cogs.general',
        'cogs.coffee',
        'cogs.mentalhealth',  # New mental health cog
        'cogs.moderation',
        'cogs.fun',
        'cogs.utility'
    ]
    
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logger.info(f'✅ Loaded cog: {cog}')
        except Exception as e:
            logger.error(f'❌ Failed to load cog {cog}: {e}')


async def main():
    """Main bot startup function"""
    async with bot:
        await load_cogs()
        
        # Get token from environment variable
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            logger.error("❌ DISCORD_TOKEN environment variable not found!")
            logger.error("💡 Make sure you have created a .env file with your bot token")
            return
        
        try:
            logger.info("🚀 Starting MochaBot with mental health support...")
            await bot.start(token)
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")


if __name__ == '__main__':
    # Run the bot
    print("☕ MochaBot - Mental Health & Coffee Community Support")
    print("🧠 Loading mental wellness resources...")
    print("💙 Remember: You matter and you're not alone\n")
    
    asyncio.run(main())