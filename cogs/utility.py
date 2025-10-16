"""Utility commands cog for MochaBot"""

import discord
from discord.ext import commands
import asyncio
import aiohttp
from datetime import datetime, timedelta
import json
import time

BOT_COLOR = 0x8B4513

class Utility(commands.Cog):
    """Utility commands for productivity and server management"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔧'
        self.reminders = {}  # Simple in-memory storage
    
    @commands.hybrid_command(name='poll', description='Create a poll with multiple options')
    async def poll(self, ctx, question: str, *options):
        """Create a poll with up to 10 options"""
        if len(options) < 2:
            await ctx.send('❌ Please provide at least 2 options for the poll!')
            return
        
        if len(options) > 10:
            await ctx.send('❌ Maximum 10 options allowed!')
            return
        
        # Create embed
        embed = discord.Embed(
            title='📏 Poll',
            description=f'**{question}**',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        # Add options with emojis
        emojis = ['🅰️', '🅱️', '🄲️', '🄳️', '🄴️', '🄵️', '🄶️', '🄷️', '🄸️', '🄹️']
        
        option_text = ''
        for i, option in enumerate(options):
            option_text += f'{emojis[i]} {option}\n'
        
        embed.add_field(name='Options', value=option_text, inline=False)
        embed.set_footer(text=f'Poll created by {ctx.author.display_name}')
        
        message = await ctx.send(embed=embed)
        
        # Add reactions
        for i in range(len(options)):
            await message.add_reaction(emojis[i])
    
    @commands.hybrid_command(name='remind', aliases=['reminder'], description='Set a reminder')
    async def remind(self, ctx, time_str: str, *, message: str):
        """Set a reminder (format: 5m, 1h, 2d)"""
        # Parse time
        time_units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
        
        try:
            if time_str[-1].lower() in time_units:
                time_value = int(time_str[:-1])
                time_unit = time_str[-1].lower()
                seconds = time_value * time_units[time_unit]
            else:
                raise ValueError
        except (ValueError, IndexError):
            await ctx.send('❌ Invalid time format! Use format like: 5m, 1h, 2d')
            return
        
        if seconds < 10:  # Minimum 10 seconds
            await ctx.send('❌ Minimum reminder time is 10 seconds!')
            return
        
        if seconds > 7776000:  # Maximum 90 days
            await ctx.send('❌ Maximum reminder time is 90 days!')
            return
        
        # Calculate end time
        end_time = datetime.utcnow() + timedelta(seconds=seconds)
        
        embed = discord.Embed(
            title='⏰ Reminder Set',
            description=f'I\'ll remind you about: **{message}**\n\nTime: <t:{int(end_time.timestamp())}:R>',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
        
        # Wait and send reminder
        await asyncio.sleep(seconds)
        
        reminder_embed = discord.Embed(
            title='⏰ Reminder!',
            description=f'{ctx.author.mention}, you asked me to remind you about:\n\n**{message}**',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        try:
            await ctx.send(embed=reminder_embed)
        except:
            # If we can't send in the original channel, try DM
            try:
                await ctx.author.send(embed=reminder_embed)
            except:
                pass  # User has DMs disabled
    
    @commands.hybrid_command(name='weather', description='Get weather information for a city')
    async def weather(self, ctx, *, city: str):
        """Get current weather information for a city"""
        # Note: You'll need to get an API key from OpenWeatherMap
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with actual API key
        
        if api_key == "YOUR_OPENWEATHER_API_KEY":
            embed = discord.Embed(
                title='⛅ Weather Service Unavailable',
                description='Weather API key not configured. Please contact the bot owner.',
                color=BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title=f'⛅ Weather in {data["name"]}, {data["sys"]["country"]}',
                            color=BOT_COLOR,
                            timestamp=datetime.utcnow()
                        )
                        
                        # Main weather info
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        humidity = data['main']['humidity']
                        pressure = data['main']['pressure']
                        
                        weather_desc = data['weather'][0]['description'].title()
                        
                        embed.add_field(name='🌡️ Temperature', value=f'{temp}°C', inline=True)
                        embed.add_field(name='🤔 Feels Like', value=f'{feels_like}°C', inline=True)
                        embed.add_field(name='💧 Humidity', value=f'{humidity}%', inline=True)
                        
                        embed.add_field(name='☁️ Condition', value=weather_desc, inline=True)
                        embed.add_field(name='🌬️ Pressure', value=f'{pressure} hPa', inline=True)
                        
                        if 'wind' in data:
                            wind_speed = data['wind']['speed']
                            embed.add_field(name='💨 Wind Speed', value=f'{wind_speed} m/s', inline=True)
                        
                        await ctx.send(embed=embed)
                    
                    elif response.status == 404:
                        await ctx.send('❌ City not found! Please check the spelling.')
                    else:
                        await ctx.send('❌ Weather service is currently unavailable.')
            
            except Exception as e:
                await ctx.send('❌ An error occurred while fetching weather data.')
    
    @commands.hybrid_command(name='translate', description='Translate text to another language')
    async def translate(self, ctx, target_lang: str, *, text: str):
        """Translate text to another language (e.g., !translate es Hello world)"""
        # Note: This is a simplified example. For production, use a proper translation API
        common_languages = {
            'es': 'Spanish', 'fr': 'French', 'de': 'German', 'it': 'Italian',
            'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese', 'ko': 'Korean',
            'zh': 'Chinese', 'ar': 'Arabic', 'hi': 'Hindi', 'nl': 'Dutch'
        }
        
        if target_lang.lower() not in common_languages:
            lang_list = ', '.join(common_languages.keys())
            await ctx.send(f'❌ Unsupported language! Available: {lang_list}')
            return
        
        # Placeholder - in a real implementation, you'd use a translation API
        embed = discord.Embed(
            title='🌍 Translation Service',
            description='Translation service not configured. Please use an online translator.',
            color=BOT_COLOR
        )
        
        embed.add_field(name='Original Text', value=text, inline=False)
        embed.add_field(name='Target Language', value=common_languages[target_lang.lower()], inline=False)
        embed.add_field(name='Recommendation', value='Try Google Translate or DeepL for accurate translations', inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='qr', description='Generate a QR code for text or URL')
    async def qr_code(self, ctx, *, text: str):
        """Generate a QR code for the provided text"""
        # Using qr-server API for QR code generation
        try:
            # URL encode the text
            import urllib.parse
            encoded_text = urllib.parse.quote(text)
            qr_url = f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}'
            
            embed = discord.Embed(
                title='📱 QR Code Generated',
                description=f'QR Code for: **{text[:100]}**{"..." if len(text) > 100 else ""}',
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            embed.set_image(url=qr_url)
            embed.set_footer(text='Scan with your phone camera or QR code app')
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            await ctx.send('❌ Failed to generate QR code. Please try again.')
    
    @commands.hybrid_command(name='shorten', description='Shorten a long URL')
    async def shorten_url(self, ctx, url: str):
        """Shorten a URL using a URL shortening service"""
        # Check if it's a valid URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Placeholder for URL shortening service
        # In a real implementation, you'd use a service like bit.ly, tinyurl, etc.
        
        embed = discord.Embed(
            title='🔗 URL Shortener',
            description='URL shortening service not configured.',
            color=BOT_COLOR
        )
        
        embed.add_field(name='Original URL', value=url, inline=False)
        embed.add_field(
            name='Suggestion', 
            value='Try online services like bit.ly, tinyurl.com, or t.co', 
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='base64', description='Encode or decode base64 text')
    async def base64_converter(self, ctx, action: str, *, text: str):
        """Encode or decode base64 text (actions: encode, decode)"""
        import base64
        
        action = action.lower()
        
        try:
            if action == 'encode':
                encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                result = encoded
                title = 'Base64 Encoded'
            elif action == 'decode':
                decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                result = decoded
                title = 'Base64 Decoded'
            else:
                await ctx.send('❌ Invalid action! Use `encode` or `decode`')
                return
            
            embed = discord.Embed(
                title=f'🔐 {title}',
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name='Input', value=f'```{text[:500]}```', inline=False)
            embed.add_field(name='Output', value=f'```{result[:500]}```', inline=False)
            
            if len(result) > 500:
                embed.set_footer(text='Output truncated due to length')
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            await ctx.send('❌ Invalid base64 string or encoding error!')
    
    @commands.hybrid_command(name='hash', description='Generate hash of text')
    async def hash_text(self, ctx, algorithm: str, *, text: str):
        """Generate hash of text (algorithms: md5, sha1, sha256)"""
        import hashlib
        
        algorithm = algorithm.lower()
        supported_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
        
        if algorithm not in supported_algorithms:
            await ctx.send(f'❌ Unsupported algorithm! Available: {"`, `".join(supported_algorithms)}')
            return
        
        try:
            # Generate hash
            hash_obj = hashlib.new(algorithm)
            hash_obj.update(text.encode('utf-8'))
            hash_result = hash_obj.hexdigest()
            
            embed = discord.Embed(
                title=f'🔒 {algorithm.upper()} Hash',
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name='Input', value=f'```{text[:200]}```', inline=False)
            embed.add_field(name='Hash', value=f'```{hash_result}```', inline=False)
            
            await ctx.send(embed=embed)
        
        except Exception as e:
            await ctx.send('❌ An error occurred while generating the hash.')
    
    @commands.hybrid_command(name='timestamp', aliases=['time'], description='Get current timestamp or convert time')
    async def timestamp(self, ctx, unix_timestamp: int = None):
        """Get current timestamp or convert Unix timestamp to readable time"""
        
        if unix_timestamp:
            try:
                dt = datetime.fromtimestamp(unix_timestamp)
                
                embed = discord.Embed(
                    title='🕒 Timestamp Converter',
                    color=BOT_COLOR,
                    timestamp=datetime.utcnow()
                )
                
                embed.add_field(name='Unix Timestamp', value=str(unix_timestamp), inline=False)
                embed.add_field(name='Readable Time', value=dt.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)
                embed.add_field(name='Discord Format', value=f'<t:{unix_timestamp}>', inline=False)
                embed.add_field(name='Relative Format', value=f'<t:{unix_timestamp}:R>', inline=False)
                
                await ctx.send(embed=embed)
            
            except (ValueError, OSError):
                await ctx.send('❌ Invalid timestamp! Please provide a valid Unix timestamp.')
        
        else:
            # Get current timestamp
            current_time = datetime.utcnow()
            unix_time = int(current_time.timestamp())
            
            embed = discord.Embed(
                title='🕒 Current Timestamp',
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name='Unix Timestamp', value=str(unix_time), inline=False)
            embed.add_field(name='Readable Time', value=current_time.strftime('%Y-%m-%d %H:%M:%S UTC'), inline=False)
            embed.add_field(name='Discord Format', value=f'<t:{unix_time}>', inline=False)
            embed.add_field(name='Relative Format', value=f'<t:{unix_time}:R>', inline=False)
            
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='color', description='Display information about a color')
    async def color_info(self, ctx, color_code: str):
        """Display information about a hex color code"""
        # Remove # if present
        if color_code.startswith('#'):
            color_code = color_code[1:]
        
        # Validate hex color
        if len(color_code) != 6 or not all(c in '0123456789abcdefABCDEF' for c in color_code):
            await ctx.send('❌ Invalid hex color code! Use format: #RRGGBB or RRGGBB')
            return
        
        try:
            # Convert to RGB
            rgb = tuple(int(color_code[i:i+2], 16) for i in (0, 2, 4))
            
            # Convert to Discord color
            color_int = int(color_code, 16)
            
            embed = discord.Embed(
                title=f'🎨 Color: #{color_code.upper()}',
                color=color_int,
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(name='Hex', value=f'#{color_code.upper()}', inline=True)
            embed.add_field(name='RGB', value=f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})', inline=True)
            embed.add_field(name='Decimal', value=str(color_int), inline=True)
            
            # Create a color preview using a color API
            color_url = f'https://singlecolorimage.com/get/{color_code}/400x100'
            embed.set_thumbnail(url=color_url)
            
            await ctx.send(embed=embed)
        
        except ValueError:
            await ctx.send('❌ Invalid color code!')


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(Utility(bot))