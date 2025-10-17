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

# =========================
# Token Configuration
# =========================
# You can hardcode your token here to avoid environment variables.
# IMPORTANT: Do NOT commit your real token publicly. Keep your repo private
# or remove the token before pushing. Using env is still recommended.
#
# Option 1 (preferred): leave BOT_TOKEN empty to use environment variable DISCORD_TOKEN
# Option 2: paste your token string into BOT_TOKEN below, e.g.
# BOT_TOKEN = "MTEyMzQ1Njc4OTA.xxxxxx.yyyyyy"
BOT_TOKEN: str = os.getenv("DISCORD_TOKEN", "")

# =========================
# Basic Bot configuration
# =========================
BOT_PREFIX = '!'
BOT_VERSION = "2.1.1"  # Bumped version for token-inline support
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
            description=(
                f"**Welcome to MochaBot v{BOT_VERSION}**\n\n"
                f"*Your friendly coffee-themed companion for mental wellness and community support!*\n\n"
                f"**🎯 Purpose:** Combining coffee culture with mental health resources\n"
                f"**📞 Crisis Support:** Use `{self.context.clean_prefix}crisis` for emergency resources\n"
                f"**Prefix:** `{self.context.clean_prefix}`\n\n"
                f"**🔍 Quick Navigation:**\nUse `{self.context.clean_prefix}help <category>` or `{self.context.clean_prefix}help <command>` for detailed information."
            ),
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        if self.context.bot.user and self.context.bot.user.avatar:
            embed.set_thumbnail(url=self.context.bot.user.avatar.url)
        
        for cog, commands_list in mapping.items():
            filtered = await self.filter_commands(commands_list, sort=True)
            if not filtered:
                continue
            cog_name = getattr(cog, 'qualified_name', 'General')
            cog_emoji = getattr(cog, 'emoji', '📋')
            cog_description = getattr(cog, 'description', 'Various commands')
            command_count = len(filtered)
            command_preview = ', '.join([cmd.name for cmd in filtered[:3]])
            if command_count > 3:
                command_preview += f" and {command_count - 3} more..."
            embed.add_field(
                name=f"{cog_emoji} {cog_name} ({command_count} commands)",
                value=f"{cog_description}\n**Commands:** {command_preview}",
                inline=True
            )
        
        embed.add_field(
            name="🔗 Resources",
            value="[Support Server](https://discord.gg/example) | [GitHub](https://github.com/aurora9161/mochabot) | Mental Health: nami.org",
            inline=False
        )
        embed.add_field(
            name="🆘 Need Help?",
            value=(
                f"Mental Health Crisis: `{self.context.clean_prefix}crisis`\n"
                f"Daily Check-in: `{self.context.clean_prefix}checkin`\n"
                f"Breathing Exercise: `{self.context.clean_prefix}breathe`"
            ),
            inline=False
        )
        embed.set_footer(
            text=f"Requested by {self.context.author} | MochaBot v{BOT_VERSION} | You matter 💙",
            icon_url=self.context.author.avatar.url if self.context.author.avatar else None
        )
        view = HelpMenuView(self.context, mapping)
        await self.get_destination().send(embed=embed, view=view)
    
    async def send_command_help(self, command):
        embed = discord.Embed(
            title=f"☕ Command: {command.name}",
            description=command.help or "No description available",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        embed.add_field(name="📝 Usage", value=f"`{self.get_command_signature(command)}`", inline=False)
        if command.aliases:
            embed.add_field(name="🔄 Aliases", value=", ".join([f"`{a}`" for a in command.aliases]), inline=True)
        if hasattr(command, 'cooldown') and command.cooldown:
            embed.add_field(name="⏱️ Cooldown", value=f"{command.cooldown.rate} uses per {command.cooldown.per}s", inline=True)
        if command.cog:
            embed.add_field(name="📂 Category", value=command.cog.qualified_name, inline=True)
        if command.cog and getattr(command.cog, 'emoji', '') == '🧠':
            embed.add_field(name="💙 Note", value="This is a mental health support command.", inline=False)
        embed.set_footer(text=f"Use {self.context.clean_prefix}help for more commands | You're not alone 💙",
                         icon_url=self.context.bot.user.avatar.url if self.context.bot.user and self.context.bot.user.avatar else None)
        await self.get_destination().send(embed=embed)
    
    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f"{getattr(cog, 'emoji', '📋')} {cog.qualified_name} Commands",
            description=cog.description or "No description available",
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        commands_list = await self.filter_commands(cog.get_commands(), sort=True)
        if commands_list:
            for command in commands_list:
                embed.add_field(name=f"`{self.context.clean_prefix}{command.name}`",
                                value=command.short_doc or "No description",
                                inline=True)
        else:
            embed.add_field(name="❌ No Commands", value="This category has no available commands.", inline=False)
        if getattr(cog, 'emoji', '') == '🧠':
            embed.add_field(name="💙 Remember", value=(
                "These tools support mental wellness but don't replace professional help. "
                "If you're in crisis, please reach out to a professional or use `!crisis`."
            ), inline=False)
        embed.set_footer(text=f"Use {self.context.clean_prefix}help <command> for detailed info | You matter 💙",
                         icon_url=self.context.bot.user.avatar.url if self.context.bot.user and self.context.bot.user.avatar else None)
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=f"☕ Group: {group.name}",
            description=group.help or "No description available",
            color=BOT_COLOR
        )
        embed.add_field(name="📝 Usage", value=f"`{self.get_command_signature(group)}`", inline=False)
        if group.commands:
            subs = await self.filter_commands(group.commands, sort=True)
            if subs:
                embed.add_field(name="🔧 Subcommands",
                                value="\n".join([f"`{self.context.clean_prefix}{group.name} {c.name}` - {c.short_doc or 'No description'}" for c in subs]),
                                inline=False)
        await self.get_destination().send(embed=embed)


class HelpMenuView(discord.ui.View):
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
        embed = discord.Embed(title="🧠 Mental Health Quick Access",
                              description="Immediate access to mental health and wellness resources",
                              color=0x87CEEB, timestamp=datetime.utcnow())
        embed.add_field(name="🆘 Crisis Resources",
                        value=f"`{self.ctx.clean_prefix}crisis` • `{self.ctx.clean_prefix}therapy`",
                        inline=False)
        embed.add_field(name="🌸 Daily Wellness",
                        value=(f"`{self.ctx.clean_prefix}checkin` • `{self.ctx.clean_prefix}mood <1-10>` • "
                               f"`{self.ctx.clean_prefix}affirmation`"), inline=False)
        embed.add_field(name="🫁 Coping Tools",
                        value=(f"`{self.ctx.clean_prefix}breathe` • `{self.ctx.clean_prefix}ground` • "
                               f"`{self.ctx.clean_prefix}selfcare`"), inline=False)
        embed.add_field(name="💙 Remember",
                        value="These tools support you, but please reach out to professionals when needed.", inline=False)
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label='📋 Commands List', style=discord.ButtonStyle.secondary)
    async def commands_list_button(self, interaction, button):
        embed = discord.Embed(title="📋 All Commands Quick Reference", color=BOT_COLOR, timestamp=datetime.utcnow())
        all_cmds = []
        for _, cmds in self.mapping.items():
            for cmd in cmds:
                all_cmds.append(f"`{self.ctx.clean_prefix}{cmd.name}`")
        chunks = [all_cmds[i:i+15] for i in range(0, len(all_cmds), 15)]
        for i, chunk in enumerate(chunks[:3]):
            embed.add_field(name=f"Commands {i*15+1}-{min((i+1)*15, len(all_cmds))}", value="\n".join(chunk), inline=True)
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label='ℹ️ Bot Info', style=discord.ButtonStyle.gray)
    async def bot_info_button(self, interaction, button):
        embed = discord.Embed(title="ℹ️ MochaBot Information", color=BOT_COLOR, timestamp=datetime.utcnow())
        embed.add_field(name="🤖 Bot Version", value=f"v{BOT_VERSION}", inline=True)
        embed.add_field(name="🐍 Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="🏠 Servers", value=str(len(self.ctx.bot.guilds)), inline=True)
        embed.add_field(name="👥 Users", value=str(len(self.ctx.bot.users)), inline=True)
        embed.add_field(name="📡 Ping", value=f"{round(self.ctx.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="☕ About MochaBot",
                        value=("Coffee-themed community bot with mental health support: wellness tools, "
                               "crisis resources, and supportive features."), inline=False)
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
    logger.info(f'☕ {bot.user} is online and ready!')
    activity = discord.Activity(type=discord.ActivityType.listening,
                                name=f"your mental wellness • {BOT_PREFIX}help")
    await bot.change_presence(activity=activity, status=discord.Status.online)
    if not daily_wellness_check.is_running():
        daily_wellness_check.start()

@bot.event
async def on_member_join(member):
    welcome_messages = [
        f"☕ Welcome {member.mention}! This is a safe space for community and wellness.",
        f"🌟 {member.mention} joined our wellness café! We're here to support each other.",
    ]
    welcome_channels = ['welcome', 'general', 'lobby', 'café', 'coffee-house', 'wellness', 'support']
    for name in welcome_channels:
        channel = discord.utils.get(member.guild.text_channels, name=name)
        if channel:
            embed = discord.Embed(title="☕ Welcome to Our Wellness Community!",
                                  description=random.choice(welcome_messages),
                                  color=BOT_COLOR, timestamp=datetime.utcnow())
            embed.add_field(name="🎯 Get Started",
                            value=(f"`{BOT_PREFIX}help` for all features\n"
                                   f"`{BOT_PREFIX}checkin` for daily wellness\n"
                                   f"`{BOT_PREFIX}crisis` for immediate support"), inline=False)
            await channel.send(embed=embed)
            break

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    mental_keywords = ['stress', 'anxiety', 'depression', 'sad', 'worried', 'panic', 'overwhelmed', 'tired', 'exhausted']
    coffee_keywords = ['coffee', 'café', 'espresso', 'latte', 'cappuccino', 'mocha', 'brew']
    content = message.content.lower()
    if any(k in content for k in mental_keywords):
        if random.randint(1, 15) == 1:
            await message.add_reaction('💙')
    elif any(k in content for k in coffee_keywords):
        if random.randint(1, 20) == 1:
            await message.add_reaction('☕')
    await bot.process_commands(message)

@tasks.loop(hours=12)
async def daily_wellness_check():
    tips = [
        "💙 Check in with yourself today.",
        "🌸 Take a slow, deep breath.",
        "🫁 Try `!breathe` if you feel overwhelmed.",
        "🌱 Small acts of self-care matter.",
    ]
    tip = random.choice(tips)
    for guild in bot.guilds:
        for name in ['wellness', 'mental-health', 'support', 'daily-wellness', 'self-care']:
            channel = discord.utils.get(guild.text_channels, name=name)
            if channel:
                embed = discord.Embed(title="🌸 Daily Wellness Reminder", description=tip,
                                      color=0x87CEEB, timestamp=datetime.utcnow())
                embed.add_field(name="🛠️ Quick Tools",
                                value=f"`{BOT_PREFIX}checkin` • `{BOT_PREFIX}breathe` • `{BOT_PREFIX}affirmation` • `{BOT_PREFIX}selfcare`",
                                inline=False)
                try:
                    await channel.send(embed=embed)
                    break
                except:
                    pass

# Load all cogs including mental health
async def load_cogs():
    cogs = [
        'cogs.general',
        'cogs.coffee',
        'cogs.mentalhealth',
        'cogs.moderation',
        'cogs.fun',
        'cogs.utility'
    ]
    for cog in cogs:
        try:
            await bot.load_extension(cog)
            logging.info(f'✅ Loaded cog: {cog}')
        except Exception as e:
            logging.error(f'❌ Failed to load cog {cog}: {e}')

async def main():
    async with bot:
        await load_cogs()
        # Determine token source: prefer inline BOT_TOKEN; fallback to env
        token = BOT_TOKEN or os.getenv('DISCORD_TOKEN') or ""
        if not token:
            logging.error("❌ No bot token found. Set BOT_TOKEN in bot.py or DISCORD_TOKEN env var.")
            return
        try:
            logging.info("🚀 Starting MochaBot...")
            await bot.start(token)
        except Exception as e:
            logging.error(f"❌ Failed to start bot: {e}")

if __name__ == '__main__':
    # To use inline token: paste it into BOT_TOKEN above. Cogs will still load.
    # To use env: set DISCORD_TOKEN on your host/panel.
    asyncio.run(main())
