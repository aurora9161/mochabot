"""General commands cog for MochaBot"""

import discord
from discord.ext import commands
from datetime import datetime
import platform
import psutil
import time

BOT_COLOR = 0x8B4513

class General(commands.Cog):
    """General purpose commands for everyday use"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔧'
        self.start_time = time.time()
    
    @commands.hybrid_command(name='ping', description='Check the bot\'s latency')
    async def ping(self, ctx):
        """Check the bot's latency and response time"""
        start = time.perf_counter()
        message = await ctx.send('⏳ Pinging...')
        end = time.perf_counter()
        
        api_latency = round(self.bot.latency * 1000, 2)
        response_time = round((end - start) * 1000, 2)
        
        embed = discord.Embed(
            title='🏓 Pong!',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name='📡 API Latency', value=f'`{api_latency}ms`', inline=True)
        embed.add_field(name='⏱️ Response Time', value=f'`{response_time}ms`', inline=True)
        
        # Add status indicator
        if api_latency < 100:
            status = '🟢 Excellent'
        elif api_latency < 200:
            status = '🟡 Good'
        elif api_latency < 300:
            status = '🟠 Fair'
        else:
            status = '🔴 Poor'
        
        embed.add_field(name='📊 Status', value=status, inline=True)
        
        await message.edit(content=None, embed=embed)
    
    @commands.hybrid_command(name='info', aliases=['botinfo', 'about'], description='Get information about MochaBot')
    async def info(self, ctx):
        """Display detailed information about the bot"""
        embed = discord.Embed(
            title='☕ MochaBot Information',
            description='Your friendly coffee-themed Discord companion!',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        if self.bot.user.avatar:
            embed.set_thumbnail(url=self.bot.user.avatar.url)
        
        # Bot statistics
        guild_count = len(self.bot.guilds)
        user_count = len(self.bot.users)
        command_count = len([cmd for cmd in self.bot.walk_commands()])
        
        embed.add_field(name='🏠 Servers', value=f'`{guild_count:,}`', inline=True)
        embed.add_field(name='👥 Users', value=f'`{user_count:,}`', inline=True)
        embed.add_field(name='📝 Commands', value=f'`{command_count}`', inline=True)
        
        # System information
        uptime = time.time() - self.start_time
        hours, remainder = divmod(int(uptime), 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_str = f'{hours}h {minutes}m {seconds}s'
        
        embed.add_field(name='⏱️ Uptime', value=f'`{uptime_str}`', inline=True)
        embed.add_field(name='🐍 Python', value=f'`{platform.python_version()}`', inline=True)
        embed.add_field(name='🤖 Discord.py', value=f'`{discord.__version__}`', inline=True)
        
        # Memory and CPU usage
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        embed.add_field(name='💾 Memory Usage', value=f'`{memory.percent}%`', inline=True)
        embed.add_field(name='⚙️ CPU Usage', value=f'`{cpu_percent}%`', inline=True)
        embed.add_field(name='📡 Latency', value=f'`{round(self.bot.latency * 1000)}ms`', inline=True)
        
        embed.add_field(
            name='🔗 Links',
            value='[GitHub](https://github.com/aurora9161/mochabot) • [Invite](https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID) • [Support](https://discord.gg/example)',
            inline=False
        )
        
        embed.set_footer(
            text=f'Created by aurora9161 • Made with ☕ and ❤️',
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='serverinfo', aliases=['guildinfo', 'si'], description='Get information about the current server')
    async def serverinfo(self, ctx):
        """Display information about the current server"""
        if not ctx.guild:
            await ctx.send('❌ This command can only be used in servers!')
            return
        
        guild = ctx.guild
        
        embed = discord.Embed(
            title=f'🏠 {guild.name}',
            description=guild.description or 'No description set',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Basic server information
        embed.add_field(name='🎯 Server ID', value=f'`{guild.id}`', inline=True)
        embed.add_field(name='👑 Owner', value=guild.owner.mention if guild.owner else 'Unknown', inline=True)
        embed.add_field(name='📅 Created', value=f'<t:{int(guild.created_at.timestamp())}:R>', inline=True)
        
        # Member statistics
        total_members = guild.member_count
        online_members = len([m for m in guild.members if m.status != discord.Status.offline])
        bots = len([m for m in guild.members if m.bot])
        humans = total_members - bots
        
        embed.add_field(name='👥 Total Members', value=f'`{total_members:,}`', inline=True)
        embed.add_field(name='🟢 Online', value=f'`{online_members:,}`', inline=True)
        embed.add_field(name='🤖 Bots', value=f'`{bots:,}`', inline=True)
        
        # Channel statistics
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed.add_field(name='💬 Text Channels', value=f'`{text_channels}`', inline=True)
        embed.add_field(name='🔊 Voice Channels', value=f'`{voice_channels}`', inline=True)
        embed.add_field(name='📂 Categories', value=f'`{categories}`', inline=True)
        
        # Server features
        features = guild.features
        if features:
            feature_list = []
            feature_names = {
                'ANIMATED_ICON': 'Animated Icon',
                'BANNER': 'Server Banner',
                'COMMUNITY': 'Community Server',
                'DISCOVERABLE': 'Server Discovery',
                'VERIFIED': 'Verified',
                'PARTNERED': 'Partnered',
                'VANITY_URL': 'Vanity URL',
                'INVITE_SPLASH': 'Invite Splash',
                'VIP_REGIONS': 'VIP Voice Regions',
                'NEWS': 'News Channels'
            }
            
            for feature in features[:5]:  # Show only first 5 features
                feature_list.append(feature_names.get(feature, feature.replace('_', ' ').title()))
            
            if len(features) > 5:
                feature_list.append(f'and {len(features) - 5} more...')
            
            embed.add_field(
                name='✨ Features',
                value='\n'.join([f'• {feature}' for feature in feature_list]) or 'None',
                inline=False
            )
        
        # Boost information
        embed.add_field(name='🚀 Boost Level', value=f'`Level {guild.premium_tier}`', inline=True)
        embed.add_field(name='💪 Boosts', value=f'`{guild.premium_subscription_count}`', inline=True)
        embed.add_field(name='🗺️ Roles', value=f'`{len(guild.roles)}`', inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='userinfo', aliases=['whois', 'ui'], description='Get information about a user')
    async def userinfo(self, ctx, member: discord.Member = None):
        """Display information about a user"""
        if not member:
            member = ctx.author
        
        embed = discord.Embed(
            title=f'👤 {member.display_name}',
            color=member.color if member.color != discord.Color.default() else BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        # Basic user information
        embed.add_field(name='🎯 User ID', value=f'`{member.id}`', inline=True)
        embed.add_field(name='📝 Username', value=f'`{member.name}`', inline=True)
        embed.add_field(name='🤖 Bot', value='Yes' if member.bot else 'No', inline=True)
        
        # Account and join dates
        embed.add_field(name='📅 Account Created', value=f'<t:{int(member.created_at.timestamp())}:R>', inline=True)
        if ctx.guild and member in ctx.guild.members:
            embed.add_field(name='🏠 Joined Server', value=f'<t:{int(member.joined_at.timestamp())}:R>', inline=True)
        
        # Status and activity
        status_emoji = {
            discord.Status.online: '🟢 Online',
            discord.Status.idle: '🟡 Idle',
            discord.Status.dnd: '🔴 Do Not Disturb',
            discord.Status.offline: '⚫ Offline'
        }
        
        embed.add_field(name='📱 Status', value=status_emoji.get(member.status, 'Unknown'), inline=True)
        
        # Activity
        if member.activities:
            activity = member.activities[0]
            activity_text = f'{activity.type.name.title()}: {activity.name}' if hasattr(activity, 'name') else str(activity)
            embed.add_field(name='🎮 Activity', value=activity_text, inline=False)
        
        # Roles (if in a guild)
        if ctx.guild and member in ctx.guild.members:
            roles = [role.mention for role in member.roles[1:]]  # Skip @everyone
            if roles:
                role_list = ', '.join(roles[:10])  # Show first 10 roles
                if len(roles) > 10:
                    role_list += f' and {len(roles) - 10} more...'
                embed.add_field(name=f'🗺️ Roles ({len(roles)})', value=role_list, inline=False)
        
        # Permissions (if in a guild)
        if ctx.guild and member in ctx.guild.members:
            perms = member.guild_permissions
            key_perms = []
            if perms.administrator:
                key_perms.append('Administrator')
            elif perms.manage_guild:
                key_perms.append('Manage Server')
            elif perms.manage_channels:
                key_perms.append('Manage Channels')
            elif perms.manage_messages:
                key_perms.append('Manage Messages')
            elif perms.kick_members:
                key_perms.append('Kick Members')
            elif perms.ban_members:
                key_perms.append('Ban Members')
            
            if key_perms:
                embed.add_field(name='🔑 Key Permissions', value=', '.join(key_perms), inline=False)
        
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='avatar', aliases=['av', 'pfp'], description='Display a user\'s avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Display a user's avatar in full size"""
        if not member:
            member = ctx.author
        
        embed = discord.Embed(
            title=f'🖼️ {member.display_name}\'s Avatar',
            color=member.color if member.color != discord.Color.default() else BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        embed.set_image(url=avatar_url)
        
        # Add download links for different formats
        if member.avatar:
            formats = ['png', 'jpg', 'webp']
            if member.avatar.is_animated():
                formats.append('gif')
            
            links = [f'[{fmt.upper()}]({member.avatar.with_format(fmt).with_size(1024)})' for fmt in formats]
            embed.add_field(name='🔗 Download Links', value=' • '.join(links), inline=False)
        
        embed.set_footer(
            text=f'Requested by {ctx.author}',
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(General(bot))