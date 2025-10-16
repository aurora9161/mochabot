#!/usr/bin/env python3
"""
MochaBot - An Advanced Coffee-Themed Discord Bot
Designed for community management and engagement
Created by: aurora9161
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
BOT_VERSION = "2.0.0"
BOT_COLOR = 0x8B4513  # Coffee brown color

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True


class MochaHelpCommand(commands.HelpCommand):
    """Custom help command with beautiful embeds and coffee theme"""
    
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
            description=f"**Welcome to MochaBot v{BOT_VERSION}**\n\n*Your friendly coffee-themed Discord companion!*\n\n**Prefix:** `{self.context.clean_prefix}`\n\n**🔍 Quick Navigation:**\nUse `{self.context.clean_prefix}help <category>` or `{self.context.clean_prefix}help <command>` for detailed information.",
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
            name="🔗 Useful Links",
            value="[Support Server](https://discord.gg/example) | [GitHub](https://github.com/aurora9161/mochabot) | [Invite Bot](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID)",
            inline=False
        )
        
        embed.set_footer(
            text=f"Requested by {self.context.author} | MochaBot v{BOT_VERSION}",
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
        
        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help for more commands",
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
        
        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help <command> for detailed info",
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
    """Interactive view for the help menu"""
    
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
        # Recreate the main help embed
        help_command = MochaHelpCommand()
        help_command.context = self.ctx
        await help_command.send_bot_help(self.mapping)
    
    @discord.ui.button(label='📋 Commands List', style=discord.ButtonStyle.green)
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
        
        # Split into chunks for better display
        command_chunks = [all_commands[i:i+15] for i in range(0, len(all_commands), 15)]
        
        for i, chunk in enumerate(command_chunks[:3]):  # Limit to 3 fields
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
            value="A coffee-themed Discord bot designed for community management and engagement. Created with love and lots of caffeine!",
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
    logger.info(f'☕ {bot.user} has brewed up and is ready to serve!')
    logger.info(f'Connected to {len(bot.guilds)} servers with {len(bot.users)} users')
    
    # Set bot activity
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"coffee brewing in {len(bot.guilds)} servers | {BOT_PREFIX}help"
    )
    await bot.change_presence(activity=activity)
    
    # Start background tasks
    if not coffee_facts.is_running():
        coffee_facts.start()


@bot.event
async def on_member_join(member):
    """Welcome new members with coffee theme"""
    welcome_messages = [
        f"☕ Welcome to the coffee house, {member.mention}! Grab a cup and stay awhile!",
        f"🌟 {member.mention} just joined our café! Welcome aboard!",
        f"☕ A new coffee enthusiast has arrived! Welcome, {member.mention}!",
        f"🎉 Welcome {member.mention}! The coffee is fresh and the community is warm!"
    ]
    
    # Try to find a welcome channel
    welcome_channels = ['welcome', 'general', 'lobby', 'café', 'coffee-house']
    for channel_name in welcome_channels:
        channel = discord.utils.get(member.guild.text_channels, name=channel_name)
        if channel:
            embed = discord.Embed(
                title="☕ Welcome to the Coffee House!",
                description=random.choice(welcome_messages),
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            embed.add_field(
                name="🎯 Get Started",
                value=f"Use `{BOT_PREFIX}help` to see what I can do!",
                inline=False
            )
            embed.set_footer(text=f"Member #{len(member.guild.members)}")
            await channel.send(embed=embed)
            break


@bot.event
async def on_message(message):
    """Process messages and respond to coffee mentions"""
    if message.author == bot.user:
        return
    
    # Coffee keyword responses
    coffee_keywords = ['coffee', 'café', 'espresso', 'latte', 'cappuccino', 'mocha', 'brew']
    if any(keyword in message.content.lower() for keyword in coffee_keywords):
        if random.randint(1, 20) == 1:  # 5% chance to respond
            responses = [
                "☕ Did someone mention coffee? I'm all ears!",
                "☕ Mmm, coffee talk! My favorite topic!",
                "☕ Nothing beats a good cup of joe!",
                "☕ Coffee is the fuel of productivity!"
            ]
            await message.add_reaction('☕')
            if random.randint(1, 5) == 1:  # 20% of that 5%
                await message.reply(random.choice(responses))
    
    await bot.process_commands(message)


# Coffee Facts Background Task
@tasks.loop(hours=6)
async def coffee_facts():
    """Send coffee facts to channels that opted in"""
    coffee_facts_list = [
        "☕ Coffee is the world's second-most traded commodity after oil!",
        "☕ The word 'coffee' comes from the Arabic word 'qahwah'!",
        "☕ Finland consumes the most coffee per capita in the world!",
        "☕ Coffee beans are actually seeds of coffee cherries!",
        "☕ The most expensive coffee in the world comes from civet droppings!",
        "☕ Coffee was originally discovered by goats in Ethiopia!",
        "☕ Instant coffee was invented in 1901!",
        "☕ A coffee tree can live for over 100 years!"
    ]
    
    fact = random.choice(coffee_facts_list)
    
    # Send to channels that have opted in (you can implement this feature)
    for guild in bot.guilds:
        # Look for a coffee-facts channel or similar
        channel = discord.utils.get(guild.text_channels, name='coffee-facts')
        if channel:
            embed = discord.Embed(
                title="☕ Daily Coffee Fact",
                description=fact,
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            embed.set_footer(text="MochaBot Coffee Facts")
            try:
                await channel.send(embed=embed)
            except:
                pass  # Ignore errors if we can't send to the channel


# Load all cogs
async def load_cogs():
    """Load all cog files"""
    cogs = [
        'cogs.general',
        'cogs.coffee',
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
            return
        
        try:
            await bot.start(token)
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")


if __name__ == '__main__':
    # Run the bot
    asyncio.run(main())