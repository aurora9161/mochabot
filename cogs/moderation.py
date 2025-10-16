"""Moderation commands cog for MochaBot"""

import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

BOT_COLOR = 0x8B4513

class Moderation(commands.Cog):
    """Moderation commands for server management and safety"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔒'
        self.muted_members = {}  # Simple in-memory storage for muted members
    
    def has_permissions(**permissions):
        """Custom check for permissions"""
        def predicate(ctx):
            if not ctx.guild:
                return False
            
            member_perms = ctx.author.guild_permissions
            return all(getattr(member_perms, perm, False) for perm in permissions)
        return commands.check(predicate)
    
    @commands.hybrid_command(name='kick', description='Kick a member from the server')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Kick a member from the server"""
        if member == ctx.author:
            await ctx.send('❌ You cannot kick yourself!')
            return
        
        if member == ctx.bot.user:
            await ctx.send('❌ I cannot kick myself!')
            return
        
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send('❌ You cannot kick someone with a higher or equal role!')
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send('❌ I cannot kick someone with a higher or equal role than me!')
            return
        
        try:
            # Try to DM the member first
            try:
                dm_embed = discord.Embed(
                    title='📄 You have been kicked',
                    description=f'You were kicked from **{ctx.guild.name}**',
                    color=0xFF6B00,
                    timestamp=datetime.utcnow()
                )
                dm_embed.add_field(name='Reason', value=reason, inline=False)
                dm_embed.add_field(name='Moderator', value=str(ctx.author), inline=False)
                await member.send(embed=dm_embed)
            except:
                pass  # User has DMs disabled
            
            await member.kick(reason=f'{ctx.author}: {reason}')
            
            embed = discord.Embed(
                title='✅ Member Kicked',
                description=f'**{member}** has been kicked from the server',
                color=0xFF6B00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to kick this member!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='ban', description='Ban a member from the server')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, delete_days: int = 0, *, reason: str = "No reason provided"):
        """Ban a member from the server"""
        if member == ctx.author:
            await ctx.send('❌ You cannot ban yourself!')
            return
        
        if member == ctx.bot.user:
            await ctx.send('❌ I cannot ban myself!')
            return
        
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send('❌ You cannot ban someone with a higher or equal role!')
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send('❌ I cannot ban someone with a higher or equal role than me!')
            return
        
        if delete_days < 0 or delete_days > 7:
            await ctx.send('❌ Delete days must be between 0 and 7!')
            return
        
        try:
            # Try to DM the member first
            try:
                dm_embed = discord.Embed(
                    title='🚫 You have been banned',
                    description=f'You were banned from **{ctx.guild.name}**',
                    color=0xFF0000,
                    timestamp=datetime.utcnow()
                )
                dm_embed.add_field(name='Reason', value=reason, inline=False)
                dm_embed.add_field(name='Moderator', value=str(ctx.author), inline=False)
                await member.send(embed=dm_embed)
            except:
                pass  # User has DMs disabled
            
            await member.ban(reason=f'{ctx.author}: {reason}', delete_message_days=delete_days)
            
            embed = discord.Embed(
                title='✅ Member Banned',
                description=f'**{member}** has been banned from the server',
                color=0xFF0000,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            embed.add_field(name='Messages Deleted', value=f'{delete_days} days', inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to ban this member!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='unban', description='Unban a user from the server')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user_id: str, *, reason: str = "No reason provided"):
        """Unban a user from the server using their ID"""
        try:
            user_id = int(user_id)
            user = await self.bot.fetch_user(user_id)
        except (ValueError, discord.NotFound):
            await ctx.send('❌ Invalid user ID or user not found!')
            return
        
        try:
            await ctx.guild.unban(user, reason=f'{ctx.author}: {reason}')
            
            embed = discord.Embed(
                title='✅ User Unbanned',
                description=f'**{user}** has been unbanned from the server',
                color=0x00FF00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.NotFound:
            await ctx.send('❌ This user is not banned!')
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to unban users!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='timeout', aliases=['mute'], description='Timeout a member')
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str, *, reason: str = "No reason provided"):
        """Timeout a member (format: 5m, 1h, 2d)"""
        if member == ctx.author:
            await ctx.send('❌ You cannot timeout yourself!')
            return
        
        if member == ctx.bot.user:
            await ctx.send('❌ I cannot timeout myself!')
            return
        
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            await ctx.send('❌ You cannot timeout someone with a higher or equal role!')
            return
        
        if member.top_role >= ctx.guild.me.top_role:
            await ctx.send('❌ I cannot timeout someone with a higher or equal role than me!')
            return
        
        # Parse duration
        time_units = {'m': 60, 'h': 3600, 'd': 86400}
        
        try:
            if duration[-1].lower() in time_units:
                time_value = int(duration[:-1])
                time_unit = duration[-1].lower()
                seconds = time_value * time_units[time_unit]
            else:
                raise ValueError
        except (ValueError, IndexError):
            await ctx.send('❌ Invalid duration format! Use format like: 5m, 1h, 2d')
            return
        
        if seconds < 60:  # Minimum 1 minute
            await ctx.send('❌ Minimum timeout duration is 1 minute!')
            return
        
        if seconds > 2419200:  # Maximum 28 days
            await ctx.send('❌ Maximum timeout duration is 28 days!')
            return
        
        try:
            until = datetime.utcnow() + timedelta(seconds=seconds)
            await member.timeout(until, reason=f'{ctx.author}: {reason}')
            
            embed = discord.Embed(
                title='✅ Member Timed Out',
                description=f'**{member}** has been timed out',
                color=0xFFA500,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Duration', value=duration, inline=True)
            embed.add_field(name='Until', value=f'<t:{int(until.timestamp())}:R>', inline=True)
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to timeout this member!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='untimeout', aliases=['unmute'], description='Remove timeout from a member')
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Remove timeout from a member"""
        try:
            await member.timeout(None, reason=f'{ctx.author}: {reason}')
            
            embed = discord.Embed(
                title='✅ Timeout Removed',
                description=f'**{member}** is no longer timed out',
                color=0x00FF00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to remove timeouts!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='clear', aliases=['purge'], description='Clear messages from the channel')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 10):
        """Clear messages from the channel (max 100)"""
        if amount < 1:
            await ctx.send('❌ Amount must be at least 1!')
            return
        
        if amount > 100:
            await ctx.send('❌ Maximum amount is 100 messages!')
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount + 1)  # +1 to include the command message
            
            embed = discord.Embed(
                title='✅ Messages Cleared',
                description=f'Deleted **{len(deleted) - 1}** messages',  # -1 to exclude the command message
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            embed.add_field(name='Channel', value=ctx.channel.mention, inline=True)
            
            # Send a temporary message that deletes itself
            temp_message = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            try:
                await temp_message.delete()
            except:
                pass
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to delete messages!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='slowmode', description='Set channel slowmode')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int = 0):
        """Set slowmode for the current channel (0 to disable, max 21600)"""
        if seconds < 0 or seconds > 21600:
            await ctx.send('❌ Slowmode must be between 0 and 21600 seconds (6 hours)!')
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                description = 'Slowmode has been **disabled**'
                color = 0x00FF00
            else:
                description = f'Slowmode set to **{seconds} seconds**'
                color = 0xFFA500
            
            embed = discord.Embed(
                title='✅ Slowmode Updated',
                description=description,
                color=color,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            embed.add_field(name='Channel', value=ctx.channel.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to manage this channel!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='warn', description='Warn a member')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str = "No reason provided"):
        """Warn a member (sends them a DM)"""
        if member == ctx.author:
            await ctx.send('❌ You cannot warn yourself!')
            return
        
        if member == ctx.bot.user:
            await ctx.send('❌ I cannot warn myself!')
            return
        
        try:
            # Send DM to the member
            dm_embed = discord.Embed(
                title='⚠️ Warning Received',
                description=f'You have received a warning in **{ctx.guild.name}**',
                color=0xFFFF00,
                timestamp=datetime.utcnow()
            )
            dm_embed.add_field(name='Reason', value=reason, inline=False)
            dm_embed.add_field(name='Moderator', value=str(ctx.author), inline=False)
            dm_embed.set_footer(text='Please follow the server rules to avoid further action')
            
            await member.send(embed=dm_embed)
            
            # Confirmation in channel
            embed = discord.Embed(
                title='✅ Warning Sent',
                description=f'**{member}** has been warned',
                color=0xFFFF00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            # If DM fails, still show the warning in channel
            embed = discord.Embed(
                title='⚠️ Warning Issued (DM Failed)',
                description=f'**{member}** has been warned (could not send DM)',
                color=0xFFFF00,
                timestamp=datetime.utcnow()
            )
            embed.add_field(name='Reason', value=reason, inline=False)
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')
    
    @commands.hybrid_command(name='lockdown', description='Lock/unlock the current channel')
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    async def lockdown(self, ctx, action: str = "toggle"):
        """Lock or unlock the current channel (actions: lock, unlock, toggle)"""
        action = action.lower()
        
        if action not in ['lock', 'unlock', 'toggle']:
            await ctx.send('❌ Invalid action! Use: lock, unlock, or toggle')
            return
        
        try:
            everyone_role = ctx.guild.default_role
            overwrite = ctx.channel.overwrites_for(everyone_role)
            
            if action == 'toggle':
                action = 'unlock' if overwrite.send_messages is False else 'lock'
            
            if action == 'lock':
                overwrite.send_messages = False
                await ctx.channel.set_permissions(everyone_role, overwrite=overwrite)
                
                embed = discord.Embed(
                    title='🔒 Channel Locked',
                    description='This channel has been locked. Only moderators can send messages.',
                    color=0xFF0000,
                    timestamp=datetime.utcnow()
                )
            
            else:  # unlock
                overwrite.send_messages = None
                await ctx.channel.set_permissions(everyone_role, overwrite=overwrite)
                
                embed = discord.Embed(
                    title='🔓 Channel Unlocked',
                    description='This channel has been unlocked. Everyone can send messages again.',
                    color=0x00FF00,
                    timestamp=datetime.utcnow()
                )
            
            embed.add_field(name='Moderator', value=ctx.author.mention, inline=True)
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            await ctx.send('❌ I don\'t have permission to manage this channel!')
        except Exception as e:
            await ctx.send(f'❌ An error occurred: {str(e)}')


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(Moderation(bot))