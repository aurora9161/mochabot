"""Coffee-themed commands cog for MochaBot"""

import discord
from discord.ext import commands
import random
import aiohttp
import json
from datetime import datetime

BOT_COLOR = 0x8B4513

class Coffee(commands.Cog):
    """All things coffee! From brewing tips to random coffee facts"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '☕'
        
        # Coffee data
        self.coffee_types = [
            'Espresso', 'Americano', 'Latte', 'Cappuccino', 'Macchiato', 
            'Mocha', 'Flat White', 'Cortado', 'Gibraltar', 'Breve',
            'Affogato', 'Red Eye', 'Black Eye', 'Dripped Eye', 'Gibraltar',
            'Romano', 'Con Panna', 'Frappé', 'Cold Brew', 'Nitro Coffee'
        ]
        
        self.coffee_facts = [
            "Coffee is the world's second-most traded commodity after oil!",
            "The word 'coffee' comes from the Arabic word 'qahwah'!",
            "Finland consumes the most coffee per capita in the world!",
            "Coffee beans are actually seeds of coffee cherries!",
            "The most expensive coffee in the world comes from civet droppings!",
            "Coffee was originally discovered by goats in Ethiopia!",
            "Instant coffee was invented in 1901!",
            "A coffee tree can live for over 100 years!",
            "Brazil produces about 40% of the world's coffee!",
            "The first webcam was created to monitor a coffee pot at Cambridge University!",
            "Coffee can help you burn fat and boost your metabolism!",
            "Dark roast coffee has less caffeine than light roast!",
            "Espresso means 'pressed out' in Italian!",
            "The French press was actually invented by an Italian designer!",
            "Coffee grounds can be used as fertilizer for plants!"
        ]
        
        self.brewing_tips = [
            "Use a 1:15 to 1:17 ratio of coffee to water for pour-over methods.",
            "Water temperature should be between 195-205°F (90-96°C) for optimal extraction.",
            "Grind your coffee beans just before brewing for maximum freshness.",
            "Use filtered water to avoid off-flavors from chlorine or minerals.",
            "Pre-heat your brewing equipment to maintain consistent temperature.",
            "Bloom your coffee for 30-45 seconds when using pour-over methods.",
            "Store coffee beans in an airtight container away from light and heat.",
            "Clean your coffee equipment regularly to prevent oil buildup.",
            "Experiment with different grind sizes to find your perfect cup.",
            "Don't over-extract - brewing time affects taste significantly!"
        ]
    
    @commands.hybrid_command(name='coffee', description='Get a random coffee type suggestion')
    async def coffee_command(self, ctx):
        """Get a random coffee suggestion with description"""
        coffee_descriptions = {
            'Espresso': 'A concentrated coffee served in small, strong shots.',
            'Americano': 'Espresso diluted with hot water, similar to drip coffee.',
            'Latte': 'Espresso with steamed milk and a small amount of foam.',
            'Cappuccino': 'Equal parts espresso, steamed milk, and milk foam.',
            'Macchiato': 'Espresso "marked" with a dollop of foamed milk.',
            'Mocha': 'Espresso with chocolate syrup and steamed milk.',
            'Flat White': 'Espresso with steamed milk and minimal foam.',
            'Cortado': 'Equal parts espresso and warm milk with no foam.',
            'Cold Brew': 'Coffee steeped in cold water for 12-24 hours.',
            'Affogato': 'A shot of espresso poured over vanilla ice cream.'
        }
        
        coffee_type = random.choice(self.coffee_types)
        description = coffee_descriptions.get(coffee_type, "A delicious coffee variety!")
        
        embed = discord.Embed(
            title=f'☕ Today\'s Coffee Suggestion: {coffee_type}',
            description=description,
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        # Add brewing difficulty and strength
        difficulty = random.choice(['Beginner', 'Intermediate', 'Advanced'])
        strength = random.choice(['🟢 Mild', '🟡 Medium', '🟠 Strong', '🔴 Very Strong'])
        
        embed.add_field(name='🎯 Difficulty', value=difficulty, inline=True)
        embed.add_field(name='💪 Strength', value=strength, inline=True)
        embed.add_field(name='✨ Rating', value='⭐' * random.randint(4, 5), inline=True)
        
        # Add coffee emoji reactions
        coffee_emojis = ['☕', '🥤', '🍫']
        
        embed.set_footer(text="Enjoy your coffee! ☕")
        
        message = await ctx.send(embed=embed)
        
        # Add reactions
        for emoji in coffee_emojis:
            await message.add_reaction(emoji)
    
    @commands.hybrid_command(name='brew', description='Get brewing tips and instructions')
    async def brew(self, ctx, method: str = None):
        """Get coffee brewing tips for different methods"""
        
        if method:
            method = method.lower()
            
            brewing_methods = {
                'espresso': {
                    'title': 'Espresso Brewing Guide',
                    'steps': [
                        '1. Use finely ground coffee (18-20g)',
                        '2. Tamp evenly with 30lbs of pressure',
                        '3. Extract for 25-30 seconds',
                        '4. Aim for 1:2 ratio (coffee to liquid)'
                    ],
                    'tips': 'Look for honey-colored crema on top!'
                },
                'pourover': {
                    'title': 'Pour-Over Brewing Guide',
                    'steps': [
                        '1. Use medium-fine grind (22-25g)',
                        '2. Rinse filter with hot water',
                        '3. Bloom coffee for 30-45 seconds',
                        '4. Pour in circular motions over 3-4 minutes'
                    ],
                    'tips': 'Keep water temperature at 200°F (93°C)'
                },
                'french': {
                    'title': 'French Press Brewing Guide',
                    'steps': [
                        '1. Use coarse grind (30g coffee)',
                        '2. Add hot water (500ml)',
                        '3. Stir gently and steep for 4 minutes',
                        '4. Press plunger down slowly'
                    ],
                    'tips': 'Don\'t over-steep or it will become bitter!'
                },
                'coldbrew': {
                    'title': 'Cold Brew Brewing Guide',
                    'steps': [
                        '1. Use coarse grind (1:4 ratio)',
                        '2. Mix coffee with cold water',
                        '3. Steep for 12-24 hours',
                        '4. Strain through fine filter'
                    ],
                    'tips': 'Concentrate can be stored for up to 2 weeks!'
                }
            }
            
            if method in brewing_methods:
                method_info = brewing_methods[method]
                embed = discord.Embed(
                    title=f'☕ {method_info["title"]}',
                    color=BOT_COLOR,
                    timestamp=datetime.utcnow()
                )
                
                embed.add_field(
                    name='📄 Steps',
                    value='\n'.join(method_info['steps']),
                    inline=False
                )
                
                embed.add_field(
                    name='💡 Pro Tip',
                    value=method_info['tips'],
                    inline=False
                )
                
                await ctx.send(embed=embed)
            else:
                available_methods = ', '.join(brewing_methods.keys())
                await ctx.send(f'❌ Unknown brewing method! Available methods: `{available_methods}`')
        else:
            # Send random brewing tip
            tip = random.choice(self.brewing_tips)
            embed = discord.Embed(
                title='☕ Coffee Brewing Tip',
                description=tip,
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            embed.set_footer(text="Use !brew <method> for specific guides (espresso, pourover, french, coldbrew)")
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='coffeefact', aliases=['fact'], description='Get a random coffee fact')
    async def coffee_fact(self, ctx):
        """Learn something new about coffee!"""
        fact = random.choice(self.coffee_facts)
        
        embed = discord.Embed(
            title='☕ Coffee Fact',
            description=fact,
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.set_footer(text=f"Coffee fact #{random.randint(1, 100)}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('☕')
    
    @commands.hybrid_command(name='coffeeapi', description='Get a random coffee image from API')
    async def coffee_api(self, ctx):
        """Get a random coffee image from Coffee API"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://coffee.alexflipnote.dev/random.json') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title='☕ Random Coffee Image',
                            color=BOT_COLOR,
                            timestamp=datetime.utcnow()
                        )
                        
                        embed.set_image(url=data['file'])
                        embed.set_footer(text="Powered by Coffee API")
                        
                        await ctx.send(embed=embed)
                    else:
                        await ctx.send('❌ Failed to fetch coffee image. The API might be down.')
            except Exception as e:
                await ctx.send('❌ An error occurred while fetching the coffee image.')
    
    @commands.hybrid_command(name='coffeequote', aliases=['quote'], description='Get an inspirational coffee quote')
    async def coffee_quote(self, ctx):
        """Get an inspirational coffee quote"""
        quotes = [
            ("Coffee is a language in itself.", "Jackie Chan"),
            ("I have measured out my life with coffee spoons.", "T.S. Eliot"),
            ("Coffee first. Schemes later.", "Leanna Renee Hieber"),
            ("Life is too short for bad coffee.", "Unknown"),
            ("Coffee is the fuel of the apocalypse.", "Kurt Cobain"),
            ("Behind every successful person is a substantial amount of coffee.", "Unknown"),
            ("Coffee smells like freshly ground heaven.", "Jessi Lane Adams"),
            ("I'd rather take coffee than compliments right now.", "Louisa May Alcott"),
            ("Coffee is my love language.", "Unknown"),
            ("Espresso yourself!", "Unknown")
        ]
        
        quote, author = random.choice(quotes)
        
        embed = discord.Embed(
            title='☕ Coffee Quote of the Moment',
            description=f'*"{quote}"*\n\n— {author}',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='caffeine', description='Calculate caffeine content in different drinks')
    async def caffeine(self, ctx, drink: str = None):
        """Check caffeine content in various drinks"""
        
        caffeine_content = {
            'espresso': {'amount': '63mg', 'serving': '1 shot (1 oz)', 'description': 'The base for many coffee drinks'},
            'americano': {'amount': '63mg', 'serving': '8 oz', 'description': 'Espresso with hot water'},
            'latte': {'amount': '63mg', 'serving': '12 oz', 'description': 'Espresso with steamed milk'},
            'cappuccino': {'amount': '63mg', 'serving': '6 oz', 'description': 'Equal parts espresso, milk, and foam'},
            'drip': {'amount': '95mg', 'serving': '8 oz', 'description': 'Regular brewed coffee'},
            'coldbrew': {'amount': '100-200mg', 'serving': '8 oz', 'description': 'Cold-steeped concentrate'},
            'frappuccino': {'amount': '95mg', 'serving': '12 oz', 'description': 'Blended coffee drink'},
            'tea': {'amount': '25-50mg', 'serving': '8 oz', 'description': 'Black tea'},
            'greentea': {'amount': '25-35mg', 'serving': '8 oz', 'description': 'Green tea'},
            'cola': {'amount': '34mg', 'serving': '12 oz', 'description': 'Coca-Cola'},
            'energydrink': {'amount': '80-150mg', 'serving': '8 oz', 'description': 'Typical energy drink'}
        }
        
        if drink:
            drink = drink.lower().replace(' ', '').replace('_', '')
            
            if drink in caffeine_content:
                info = caffeine_content[drink]
                embed = discord.Embed(
                    title=f'☕ Caffeine Content: {drink.title()}',
                    color=BOT_COLOR,
                    timestamp=datetime.utcnow()
                )
                
                embed.add_field(name='⚡ Caffeine Amount', value=info['amount'], inline=True)
                embed.add_field(name='🥤 Serving Size', value=info['serving'], inline=True)
                embed.add_field(name='📝 Description', value=info['description'], inline=False)
                
                # Add safety information
                embed.add_field(
                    name='⚠️ Daily Limit',
                    value='FDA recommends max 400mg caffeine per day for healthy adults',
                    inline=False
                )
                
                await ctx.send(embed=embed)
            else:
                available_drinks = ', '.join([d.replace('greentea', 'green tea').replace('coldbrew', 'cold brew').replace('energydrink', 'energy drink') for d in caffeine_content.keys()])
                await ctx.send(f'❌ Unknown drink! Available options: `{available_drinks}`')
        else:
            # Show all caffeine contents
            embed = discord.Embed(
                title='⚡ Caffeine Content Guide',
                description='Approximate caffeine content in popular drinks',
                color=BOT_COLOR,
                timestamp=datetime.utcnow()
            )
            
            # Group by categories
            coffee_drinks = ['espresso', 'americano', 'latte', 'cappuccino', 'drip', 'coldbrew']
            other_drinks = ['tea', 'greentea', 'cola', 'energydrink']
            
            coffee_list = []
            for drink in coffee_drinks:
                if drink in caffeine_content:
                    info = caffeine_content[drink]
                    name = drink.replace('coldbrew', 'Cold Brew').replace('drip', 'Drip Coffee')
                    coffee_list.append(f'**{name.title()}**: {info["amount"]} per {info["serving"]}')
            
            other_list = []
            for drink in other_drinks:
                if drink in caffeine_content:
                    info = caffeine_content[drink]
                    name = drink.replace('greentea', 'Green Tea').replace('energydrink', 'Energy Drink')
                    other_list.append(f'**{name.title()}**: {info["amount"]} per {info["serving"]}')
            
            embed.add_field(name='☕ Coffee Drinks', value='\n'.join(coffee_list), inline=True)
            embed.add_field(name='🥤 Other Drinks', value='\n'.join(other_list), inline=True)
            
            embed.add_field(
                name='⚠️ Safety Note',
                value='FDA recommends max **400mg** caffeine per day for healthy adults',
                inline=False
            )
            
            embed.set_footer(text="Use !caffeine <drink> for detailed info")
            
            await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='coffeeshop', aliases=['shop'], description='Find coffee shop recommendations')
    async def coffee_shop(self, ctx):
        """Get coffee shop chain recommendations and tips"""
        
        chains = {
            'Starbucks': {
                'specialty': 'Frappuccinos & Seasonal Drinks',
                'pro_tip': 'Try the Pike Place Roast for classic coffee',
                'rating': '⭐⭐⭐⭐'
            },
            'Dunkin\'': {
                'specialty': 'Iced Coffee & Donuts',
                'pro_tip': 'Their cold brew is surprisingly good',
                'rating': '⭐⭐⭐⭐'
            },
            'Blue Bottle': {
                'specialty': 'Single-Origin Pour Overs',
                'pro_tip': 'Perfect for coffee purists',
                'rating': '⭐⭐⭐⭐⭐'
            },
            'Peet\'s Coffee': {
                'specialty': 'Dark Roasts & Espresso',
                'pro_tip': 'Try their Major Dickason\'s Blend',
                'rating': '⭐⭐⭐⭐'
            },
            'Local Roasters': {
                'specialty': 'Fresh Roasted Beans',
                'pro_tip': 'Support local businesses!',
                'rating': '⭐⭐⭐⭐⭐'
            }
        }
        
        embed = discord.Embed(
            title='☕ Coffee Shop Guide',
            description='Popular coffee chains and what makes them special',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        for shop, info in chains.items():
            embed.add_field(
                name=f'{info["rating"]} {shop}',
                value=f'**Specialty**: {info["specialty"]}\n**Pro Tip**: {info["pro_tip"]}',
                inline=False
            )
        
        embed.add_field(
            name='💡 General Tips',
            value='• Ask about single-origin options\n• Try pour-over for best flavor\n• Don\'t be afraid to ask questions\n• Support local roasters when possible',
            inline=False
        )
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(Coffee(bot))