"""Fun commands cog for MochaBot"""

import discord
from discord.ext import commands
import random
import aiohttp
from datetime import datetime
import asyncio

BOT_COLOR = 0x8B4513

class Fun(commands.Cog):
    """Fun and entertaining commands for your coffee break!"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🎉'
    
    @commands.hybrid_command(name='joke', description='Get a random coffee joke')
    async def joke(self, ctx):
        """Get a random coffee-themed joke"""
        jokes = [
            ("Why did the coffee file a police report?", "It got mugged!"),
            ("How does Moses make coffee?", "Hebrews it!"),
            ("What do you call sad coffee?", "Depresso!"),
            ("Why don't coffee beans ever get speeding tickets?", "Because they know how to espresso themselves!"),
            ("What's the best thing about Switzerland?", "I don't know, but their flag is a big plus... unlike their coffee prices!"),
            ("How do you know if someone's a coffee addict?", "Don't worry, they'll tell you... repeatedly!"),
            ("What did the coffee say to the cream?", "You make me whole milk!"),
            ("Why do coffee lovers prefer dark roast?", "Because light roast is too mainstream!"),
            ("What's a coffee's favorite spell?", "Espresso Patronum!"),
            ("Why did the hipster burn his tongue?", "He drank his coffee before it was cool!")
        ]
        
        setup, punchline = random.choice(jokes)
        
        embed = discord.Embed(
            title='😂 Coffee Joke',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name='Setup', value=setup, inline=False)
        embed.add_field(name='Punchline', value=punchline, inline=False)
        
        embed.set_footer(text="Hope that gave you a good laugh! ☕😄")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('😂')
    
    @commands.hybrid_command(name='8ball', aliases=['eightball'], description='Ask the magic 8-ball a question')
    async def eight_ball(self, ctx, *, question: str):
        """Ask the coffee-themed magic 8-ball a question"""
        responses = [
            "☕ It is certain",
            "☕ Without a doubt", 
            "☕ Yes definitely",
            "☕ You may rely on it",
            "☕ As I see it, yes",
            "☕ Most likely",
            "☕ Outlook good",
            "☕ Yes",
            "☕ Signs point to yes",
            "☕ Reply hazy, try again after coffee",
            "☕ Ask again later when you're caffeinated",
            "☕ Better not tell you now",
            "☕ Cannot predict now without more coffee",
            "☕ Concentrate and ask again",
            "☕ Don't count on it",
            "☕ My reply is no",
            "☕ My sources say no",
            "☕ Outlook not so good",
            "☕ Very doubtful",
            "☕ The coffee grounds say no"
        ]
        
        answer = random.choice(responses)
        
        embed = discord.Embed(
            title='🎱 Magic Coffee Ball',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(name='Question', value=f'"{question}"', inline=False)
        embed.add_field(name='Answer', value=answer, inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='roll', description='Roll dice')
    async def roll(self, ctx, dice: str = '1d6'):
        """Roll dice in NdN format (e.g., 2d6, 1d20)"""
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('❌ Format has to be in NdN! (e.g., 2d6, 1d20)')
            return
        
        if rolls > 20:
            await ctx.send('❌ Too many dice! Maximum is 20.')
            return
        
        if limit > 100:
            await ctx.send('❌ Dice too large! Maximum is 100 sides.')
            return
        
        results = [random.randint(1, limit) for _ in range(rolls)]
        total = sum(results)
        
        embed = discord.Embed(
            title=f'🎲 Rolling {dice}',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        if len(results) <= 10:
            embed.add_field(name='Results', value=', '.join(map(str, results)), inline=False)
        else:
            embed.add_field(name='Results', value=f'{len(results)} dice rolled', inline=False)
        
        embed.add_field(name='Total', value=str(total), inline=False)
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='flip', aliases=['coin'], description='Flip a coin')
    async def flip(self, ctx):
        """Flip a coin"""
        result = random.choice(['Heads', 'Tails'])
        emoji = '🪙' if result == 'Heads' else '🪚'
        
        embed = discord.Embed(
            title=f'{emoji} Coin Flip Result',
            description=f'**{result}!**',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='choose', aliases=['pick'], description='Choose between multiple options')
    async def choose(self, ctx, *, choices: str):
        """Choose randomly between multiple options (separate with commas)"""
        choice_list = [choice.strip() for choice in choices.split(',')]
        
        if len(choice_list) < 2:
            await ctx.send('❌ Please provide at least 2 choices separated by commas!')
            return
        
        if len(choice_list) > 20:
            await ctx.send('❌ Too many choices! Maximum is 20.')
            return
        
        chosen = random.choice(choice_list)
        
        embed = discord.Embed(
            title='🎯 Choice Selector',
            description=f'I choose: **{chosen}**',
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name='Options',
            value=', '.join([f'`{choice}`' for choice in choice_list]),
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='rps', description='Play Rock Paper Scissors with the bot')
    async def rock_paper_scissors(self, ctx, choice: str = None):
        """Play Rock Paper Scissors with MochaBot"""
        if not choice:
            embed = discord.Embed(
                title='✊ Rock Paper Scissors',
                description='Choose: `rock`, `paper`, or `scissors`',
                color=BOT_COLOR
            )
            await ctx.send(embed=embed)
            return
        
        choice = choice.lower()
        if choice not in ['rock', 'paper', 'scissors']:
            await ctx.send('❌ Invalid choice! Choose rock, paper, or scissors.')
            return
        
        bot_choice = random.choice(['rock', 'paper', 'scissors'])
        
        emojis = {
            'rock': '🪨',
            'paper': '📄',
            'scissors': '✂️'
        }
        
        # Determine winner
        if choice == bot_choice:
            result = "It's a tie!"
            color = 0xFFFF00  # Yellow
        elif (choice == 'rock' and bot_choice == 'scissors') or \
             (choice == 'paper' and bot_choice == 'rock') or \
             (choice == 'scissors' and bot_choice == 'paper'):
            result = "You win! 🎉"
            color = 0x00FF00  # Green
        else:
            result = "I win! 🤖"
            color = 0xFF0000  # Red
        
        embed = discord.Embed(
            title='✊ Rock Paper Scissors',
            color=color,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name='Your Choice',
            value=f'{emojis[choice]} {choice.title()}',
            inline=True
        )
        
        embed.add_field(
            name='My Choice',
            value=f'{emojis[bot_choice]} {bot_choice.title()}',
            inline=True
        )
        
        embed.add_field(
            name='Result',
            value=result,
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='quote', description='Get an inspirational quote')
    async def quote(self, ctx):
        """Get a random inspirational quote"""
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('https://api.quotable.io/random') as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        embed = discord.Embed(
                            title='💬 Inspirational Quote',
                            description=f'*"{data["content"]}"*\n\n— {data["author"]}',
                            color=BOT_COLOR,
                            timestamp=datetime.utcnow()
                        )
                        
                        await ctx.send(embed=embed)
                    else:
                        # Fallback quotes
                        fallback_quotes = [
                            ("The only way to do great work is to love what you do.", "Steve Jobs"),
                            ("Innovation distinguishes between a leader and a follower.", "Steve Jobs"),
                            ("Stay hungry, stay foolish.", "Steve Jobs"),
                            ("Life is what happens to you while you're busy making other plans.", "John Lennon"),
                            ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt")
                        ]
                        
                        quote_text, author = random.choice(fallback_quotes)
                        
                        embed = discord.Embed(
                            title='💬 Inspirational Quote',
                            description=f'*"{quote_text}"*\n\n— {author}',
                            color=BOT_COLOR,
                            timestamp=datetime.utcnow()
        )
                        
                        await ctx.send(embed=embed)
            except Exception:
                await ctx.send('❌ Failed to fetch a quote. Try again later!')
    
    @commands.hybrid_command(name='trivia', description='Answer a random trivia question')
    async def trivia(self, ctx):
        """Answer a coffee-themed trivia question"""
        questions = [
            {
                'question': 'Which country is the largest producer of coffee in the world?',
                'options': ['Colombia', 'Brazil', 'Vietnam', 'Ethiopia'],
                'answer': 'Brazil',
                'explanation': 'Brazil produces about 40% of the world\'s coffee!'
            },
            {
                'question': 'What does "espresso" mean in Italian?',
                'options': ['Fast coffee', 'Pressed out', 'Strong drink', 'Black gold'],
                'answer': 'Pressed out',
                'explanation': 'Espresso comes from the Italian word meaning "pressed out"!'
            },
            {
                'question': 'Which animal is said to have discovered coffee?',
                'options': ['Cats', 'Goats', 'Birds', 'Monkeys'],
                'answer': 'Goats',
                'explanation': 'Legend says a goat herder in Ethiopia discovered coffee when his goats became energetic after eating coffee berries!'
            },
            {
                'question': 'What is the most expensive coffee in the world made from?',
                'options': ['Gold flakes', 'Rare beans', 'Civet droppings', 'Volcanic soil'],
                'answer': 'Civet droppings',
                'explanation': 'Kopi Luwak coffee is made from beans that have been eaten and excreted by civets!'
            },
            {
                'question': 'Which country consumes the most coffee per capita?',
                'options': ['United States', 'Italy', 'Finland', 'Turkey'],
                'answer': 'Finland',
                'explanation': 'Finland consumes about 12kg of coffee per person per year!'
            },
            {
                'question': 'What temperature should water be for brewing coffee?',
                'options': ['180°F (82°C)', '195-205°F (90-96°C)', '212°F (100°C)', '175°F (79°C)'],
                'answer': '195-205°F (90-96°C)',
                'explanation': 'The optimal brewing temperature is just below boiling point for best extraction!'
            },
            {
                'question': 'How much caffeine does an average cup of coffee contain?',
                'options': ['50mg', '95mg', '150mg', '200mg'],
                'answer': '95mg',
                'explanation': 'An 8oz cup of coffee typically contains about 95mg of caffeine!'
            },
            {
                'question': 'What is a "shot" in coffee terms?',
                'options': ['1 tablespoon of coffee', '1 ounce of espresso', '1 cup of coffee', '1 teaspoon of sugar'],
                'answer': '1 ounce of espresso',
                'explanation': 'A shot refers to approximately 1 ounce of espresso extracted in 25-30 seconds!'
            }
        ]
        
        question_data = random.choice(questions)
        
        embed = discord.Embed(
            title='☕ Coffee Trivia',
            description=question_data['question'],
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        options_text = '\n'.join([f'{chr(65+i)}. {option}' for i, option in enumerate(question_data['options'])])
        embed.add_field(name='Options', value=options_text, inline=False)
        
        embed.set_footer(text="React with A, B, C, or D to answer! (30 seconds)")
        
        message = await ctx.send(embed=embed)
        
        # Fixed emoji reactions - using standard Unicode emojis
        reactions = ['🅰️', '🅱️', '🄲️', '🄳️']  # A, B, C, D
        
        try:
            for i in range(len(question_data['options'])):
                await message.add_reaction(reactions[i])
        except discord.HTTPException:
            # Fallback to simple letters if emoji reactions fail
            await message.clear_reactions()
            simple_reactions = ['A️⃣', 'B️⃣', 'C️⃣', 'D️⃣']
            for i in range(len(question_data['options'])):
                await message.add_reaction(simple_reactions[i])
            reactions = simple_reactions
        
        # Wait for user reaction
        def check(reaction, user):
            return (
                user == ctx.author and 
                str(reaction.emoji) in reactions and 
                reaction.message.id == message.id
            )
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            user_answer_index = reactions.index(str(reaction.emoji))
            user_answer = question_data['options'][user_answer_index]
            correct_answer = question_data['answer']
            
            # Create result embed
            if user_answer == correct_answer:
                result_embed = discord.Embed(
                    title='✅ Correct!',
                    description=f'**{correct_answer}** is the right answer!\n\n💡 {question_data["explanation"]}',
                    color=0x00FF00,
                    timestamp=datetime.utcnow()
                )
                result_embed.add_field(name='Your Answer', value=f'✅ {user_answer}', inline=True)
            else:
                result_embed = discord.Embed(
                    title='❌ Incorrect!',
                    description=f'The correct answer was **{correct_answer}**.\n\n💡 {question_data["explanation"]}',
                    color=0xFF0000,
                    timestamp=datetime.utcnow()
                )
                result_embed.add_field(name='Your Answer', value=f'❌ {user_answer}', inline=True)
                result_embed.add_field(name='Correct Answer', value=f'✅ {correct_answer}', inline=True)
            
            result_embed.set_footer(text="Thanks for playing! Try another round with !trivia")
            await ctx.send(embed=result_embed)
            
        except asyncio.TimeoutError:
            timeout_embed = discord.Embed(
                title='⏰ Time\'s Up!',
                description=f'No answer received in time.\n\nThe correct answer was **{question_data["answer"]}**.\n\n💡 {question_data["explanation"]}',
                color=0xFFFF00,
                timestamp=datetime.utcnow()
            )
            timeout_embed.set_footer(text="Try again with !trivia - you've got this!")
            await ctx.send(embed=timeout_embed)
        except Exception as e:
            # Handle any other errors gracefully
            error_embed = discord.Embed(
                title='❌ Trivia Error',
                description=f'Something went wrong with the trivia question.\n\nThe answer was **{question_data["answer"]}**: {question_data["explanation"]}',
                color=0xFF6600,
                timestamp=datetime.utcnow()
            )
            await ctx.send(embed=error_embed)
    
    @commands.hybrid_command(name='meme', description='Get a random meme (SFW)')
    async def meme(self, ctx):
        """Get a random meme from Reddit"""
        subreddits = ['memes', 'dankmemes', 'wholesomememes', 'ProgrammerHumor', 'coffee']
        subreddit = random.choice(subreddits)
        
        async with aiohttp.ClientSession() as session:
            try:
                url = f'https://www.reddit.com/r/{subreddit}/random/.json'
                headers = {'User-Agent': 'MochaBot/2.1.2 Discord Bot'}
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        if data and len(data) > 0 and 'data' in data[0]:
                            post_data = data[0]['data']['children'][0]['data']
                            
                            # Skip if NSFW
                            if post_data.get('over_18', False):
                                await ctx.send('❌ Found an NSFW meme, skipping for safety! Try again.')
                                return
                            
                            embed = discord.Embed(
                                title=post_data['title'][:256],  # Discord title limit
                                color=BOT_COLOR,
                                timestamp=datetime.utcnow()
                            )
                            
                            # Check if it's an image
                            if post_data['url'].endswith(('.jpg', '.jpeg', '.png', '.gif')):
                                embed.set_image(url=post_data['url'])
                            else:
                                embed.add_field(name='Link', value=post_data['url'], inline=False)
                            
                            embed.add_field(name='Upvotes', value=f"👍 {post_data['ups']}", inline=True)
                            embed.add_field(name='Subreddit', value=f"r/{post_data['subreddit']}", inline=True)
                            
                            embed.set_footer(text="Powered by Reddit API")
                            
                            await ctx.send(embed=embed)
                        else:
                            await ctx.send('❌ Could not find a suitable meme. Try again!')
                    else:
                        await ctx.send('❌ Failed to fetch meme. Reddit API might be down.')
            except Exception:
                await ctx.send('❌ An error occurred while fetching the meme. Try again later!')
    
    @commands.hybrid_command(name='compliment', description='Get or give a compliment')
    async def compliment(self, ctx, member: discord.Member = None):
        """Give someone (or yourself) a nice compliment"""
        compliments = [
            "You're as amazing as a perfectly brewed cup of coffee!",
            "Your presence lights up the room like morning sunshine!",
            "You have the energy of a double espresso and the warmth of hot cocoa!",
            "You're more refreshing than cold brew on a hot day!",
            "Your personality is as rich and complex as a single-origin roast!",
            "You make everything better, just like cream in coffee!",
            "You're as reliable as a good coffee maker!",
            "Your smile is brighter than a coffee shop's neon sign!",
            "You're the perfect blend of awesome and incredible!",
            "You're as comforting as a warm mug on a cold morning!"
        ]
        
        target = member or ctx.author
        compliment = random.choice(compliments)
        
        embed = discord.Embed(
            title=f'💖 A Compliment for {target.display_name}',
            description=compliment,
            color=BOT_COLOR,
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=target.avatar.url if target.avatar else target.default_avatar.url)
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(Fun(bot))