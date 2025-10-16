"""Mental Health and Therapy commands cog for MochaBot"""

import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
import json

BOT_COLOR = 0x8B4513

class MentalHealth(commands.Cog):
    """Mental health support, mindfulness, and wellness resources"""
    
    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🧠'
        
        # Positive affirmations
        self.affirmations = [
            "You are stronger than you think.",
            "Every small step counts towards your wellbeing.",
            "You deserve love and kindness, especially from yourself.",
            "It's okay to not be okay sometimes.",
            "Your feelings are valid and important.",
            "You have overcome challenges before, and you can do it again.",
            "Taking care of your mental health is a sign of strength.",
            "You are worthy of happiness and peace.",
            "Progress, not perfection, is what matters.",
            "You are not alone in your struggles.",
            "Your mental health matters as much as your physical health.",
            "It's brave to ask for help when you need it.",
            "You are capable of creating positive change in your life.",
            "Your journey is unique and valuable.",
            "You have the power to choose how you respond to challenges."
        ]
        
        # Breathing exercises
        self.breathing_exercises = [
            {
                'name': '4-7-8 Breathing',
                'description': 'Inhale for 4, hold for 7, exhale for 8',
                'steps': [
                    'Sit comfortably and close your eyes',
                    'Inhale through your nose for 4 counts',
                    'Hold your breath for 7 counts',
                    'Exhale through your mouth for 8 counts',
                    'Repeat 3-4 times'
                ]
            },
            {
                'name': 'Box Breathing',
                'description': 'Equal counts for inhale, hold, exhale, hold',
                'steps': [
                    'Inhale for 4 counts',
                    'Hold for 4 counts',
                    'Exhale for 4 counts',
                    'Hold empty for 4 counts',
                    'Repeat 5-10 times'
                ]
            },
            {
                'name': 'Belly Breathing',
                'description': 'Deep diaphragmatic breathing',
                'steps': [
                    'Place one hand on chest, one on belly',
                    'Breathe slowly through your nose',
                    'Feel your belly rise more than your chest',
                    'Exhale slowly through pursed lips',
                    'Continue for 5-10 minutes'
                ]
            }
        ]
        
        # Grounding techniques
        self.grounding_techniques = [
            {
                'name': '5-4-3-2-1 Technique',
                'description': 'Use your senses to ground yourself',
                'steps': [
                    '5 things you can see',
                    '4 things you can touch',
                    '3 things you can hear',
                    '2 things you can smell',
                    '1 thing you can taste'
                ]
            },
            {
                'name': 'Progressive Muscle Relaxation',
                'description': 'Tense and relax muscle groups',
                'steps': [
                    'Start with your toes, tense for 5 seconds',
                    'Release and notice the relaxation',
                    'Move up through each muscle group',
                    'Finish with your face and scalp',
                    'Breathe deeply throughout'
                ]
            },
            {
                'name': 'Mindful Observation',
                'description': 'Focus completely on one object',
                'steps': [
                    'Choose an object near you',
                    'Observe its color, texture, shape',
                    'Notice how light hits it',
                    'Focus only on this object for 2-3 minutes',
                    'Let other thoughts pass without judgment'
                ]
            }
        ]
        
        # Crisis resources
        self.crisis_resources = {
            'US': {
                'National Suicide Prevention Lifeline': '988',
                'Crisis Text Line': 'Text HOME to 741741',
                'SAMHSA National Helpline': '1-800-662-4357'
            },
            'UK': {
                'Samaritans': '116 123',
                'Crisis Text Line UK': 'Text SHOUT to 85258',
                'NHS 111': '111'
            },
            'Canada': {
                'Talk Suicide Canada': '1-833-456-4566',
                'Crisis Text Line Canada': 'Text TALK to 686868'
            },
            'Australia': {
                'Lifeline': '13 11 14',
                'Kids Helpline': '1800 55 1800'
            },
            'India': {
                'Vandrevala Foundation': '1860-2662-345',
                'AASRA': '91-9820466726'
            }
        }
    
    @commands.hybrid_command(name='affirmation', aliases=['affirm'], description='Get a positive affirmation')
    async def affirmation(self, ctx):
        """Receive a positive affirmation to boost your mood"""
        affirmation = random.choice(self.affirmations)
        
        embed = discord.Embed(
            title='🌟 Daily Affirmation',
            description=f'*"{affirmation}"*',
            color=0x87CEEB,  # Sky blue for calmness
            timestamp=datetime.utcnow()
        )
        
        embed.set_footer(text="Remember: You matter and you are valued ❤️")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('❤️')
        await message.add_reaction('🌟')
    
    @commands.hybrid_command(name='breathe', description='Get a guided breathing exercise')
    async def breathe(self, ctx, exercise_name: str = None):
        """Practice breathing exercises for anxiety and stress relief"""
        
        if exercise_name:
            # Find specific exercise
            exercise = None
            for ex in self.breathing_exercises:
                if exercise_name.lower() in ex['name'].lower():
                    exercise = ex
                    break
            
            if not exercise:
                available = ', '.join([ex['name'] for ex in self.breathing_exercises])
                await ctx.send(f'❌ Exercise not found! Available: {available}')
                return
        else:
            exercise = random.choice(self.breathing_exercises)
        
        embed = discord.Embed(
            title=f'🫁 {exercise["name"]}',
            description=exercise['description'],
            color=0x98FB98,  # Light green for relaxation
            timestamp=datetime.utcnow()
        )
        
        steps_text = '\n'.join([f'{i+1}. {step}' for i, step in enumerate(exercise['steps'])])
        embed.add_field(name='Steps', value=steps_text, inline=False)
        
        embed.add_field(
            name='💡 Tip',
            value='Find a quiet, comfortable space. Take your time and don\'t rush.',
            inline=False
        )
        
        embed.set_footer(text="Breathe at your own pace. You're doing great! 🌸")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='ground', aliases=['grounding'], description='Get a grounding technique for anxiety')
    async def ground(self, ctx, technique_name: str = None):
        """Use grounding techniques to manage anxiety and panic"""
        
        if technique_name:
            technique = None
            for tech in self.grounding_techniques:
                if technique_name.lower() in tech['name'].lower():
                    technique = tech
                    break
            
            if not technique:
                available = ', '.join([tech['name'] for tech in self.grounding_techniques])
                await ctx.send(f'❌ Technique not found! Available: {available}')
                return
        else:
            technique = random.choice(self.grounding_techniques)
        
        embed = discord.Embed(
            title=f'🌱 {technique["name"]}',
            description=technique['description'],
            color=0xDDA0DD,  # Plum for grounding
            timestamp=datetime.utcnow()
        )
        
        steps_text = '\n'.join([f'• {step}' for step in technique['steps']])
        embed.add_field(name='How to Practice', value=steps_text, inline=False)
        
        embed.add_field(
            name='🎯 Purpose',
            value='Grounding helps bring you back to the present moment when feeling overwhelmed.',
            inline=False
        )
        
        embed.set_footer(text="Take it slow. You're safe in this moment. 🕊️")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='mood', description='Log and track your current mood')
    async def mood(self, ctx, mood_level: int = None, *, notes: str = None):
        """Track your mood on a scale of 1-10"""
        
        if mood_level is None:
            # Show mood tracking info
            embed = discord.Embed(
                title='📊 Mood Tracking',
                description='Track your daily mood to identify patterns and triggers.',
                color=0xFFB6C1,  # Light pink
                timestamp=datetime.utcnow()
            )
            
            embed.add_field(
                name='How to Use',
                value='`!mood <1-10> [optional notes]`\n\nExample: `!mood 7 Had a good day at work`',
                inline=False
            )
            
            embed.add_field(
                name='Mood Scale',
                value='1-2: Very Low 😞\n3-4: Low 😔\n5-6: Neutral 😐\n7-8: Good 😊\n9-10: Great 😄',
                inline=False
            )
            
            embed.add_field(
                name='💡 Benefits',
                value='• Identify patterns\n• Track progress\n• Recognize triggers\n• Share with therapist',
                inline=False
            )
            
            await ctx.send(embed=embed)
            return
        
        if mood_level < 1 or mood_level > 10:
            await ctx.send('❌ Mood level must be between 1 and 10!')
            return
        
        # Mood responses
        mood_emojis = {
            1: '😢', 2: '😞', 3: '😔', 4: '🙁', 5: '😐',
            6: '🙂', 7: '😊', 8: '😄', 9: '😁', 10: '🤩'
        }
        
        mood_colors = {
            1: 0x8B0000, 2: 0xDC143C, 3: 0xFF4500, 4: 0xFF8C00, 5: 0xFFD700,
            6: 0xADFF2F, 7: 0x32CD32, 8: 0x00FF7F, 9: 0x00CED1, 10: 0x9370DB
        }
        
        embed = discord.Embed(
            title=f'{mood_emojis[mood_level]} Mood Logged',
            description=f'You rated your mood as **{mood_level}/10**',
            color=mood_colors[mood_level],
            timestamp=datetime.utcnow()
        )
        
        if notes:
            embed.add_field(name='Notes', value=notes, inline=False)
        
        if mood_level <= 3:
            embed.add_field(
                name='💙 Remember',
                value='It\'s okay to have difficult days. Consider reaching out to someone you trust or using the `!crisis` command if you need immediate support.',
                inline=False
            )
        elif mood_level <= 5:
            embed.add_field(
                name='🌱 Suggestion',
                value='Try a `!breathe` exercise or `!affirmation` to help lift your spirits.',
                inline=False
            )
        else:
            embed.add_field(
                name='🌟 Great!',
                value='I\'m glad you\'re feeling good! Remember this feeling for tougher days.',
                inline=False
            )
        
        embed.set_footer(text=f"Logged by {ctx.author.display_name} | Your feelings matter")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='crisis', description='Get emergency mental health resources')
    async def crisis(self, ctx, country: str = 'US'):
        """Access crisis helplines and emergency mental health resources"""
        
        country = country.upper()
        
        if country not in self.crisis_resources:
            available_countries = ', '.join(self.crisis_resources.keys())
            embed = discord.Embed(
                title='🆘 Crisis Resources',
                description=f'Available countries: {available_countries}\nUse `!crisis <country>` for specific resources.',
                color=0xFF0000,
                timestamp=datetime.utcnow()
            )
        else:
            resources = self.crisis_resources[country]
            embed = discord.Embed(
                title=f'🆘 Crisis Resources - {country}',
                description='**If you are in immediate danger, call emergency services (911, 999, 112)**',
                color=0xFF0000,
                timestamp=datetime.utcnow()
            )
            
            for service, contact in resources.items():
                embed.add_field(
                    name=f'📞 {service}',
                    value=f'**{contact}**',
                    inline=False
                )
        
        embed.add_field(
            name='💙 Remember',
            value='You are not alone. There are people who want to help you through this difficult time.',
            inline=False
        )
        
        embed.add_field(
            name='🌟 You Matter',
            value='Your life has value. Tomorrow can be different. Please reach out.',
            inline=False
        )
        
        embed.set_footer(text="Crisis resources are available 24/7 | You deserve support")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='checkin', description='Daily mental health check-in')
    async def checkin(self, ctx):
        """Interactive daily mental health check-in"""
        
        embed = discord.Embed(
            title='🌅 Daily Check-In',
            description='Take a moment to reflect on how you\'re doing today.',
            color=0xFFA07A,  # Light salmon
            timestamp=datetime.utcnow()
        )
        
        questions = [
            '❤️ How is your heart feeling today?',
            '🧠 How is your mind feeling today?',
            '💪 How is your body feeling today?',
            '🤝 How are your relationships today?',
            '🎯 What\'s one thing you\'re grateful for?'
        ]
        
        embed.add_field(
            name='Reflection Questions',
            value='\n'.join(questions),
            inline=False
        )
        
        embed.add_field(
            name='💡 How to Use',
            value='Take a few minutes to think about these questions. You don\'t need to answer them here - just reflect personally.',
            inline=False
        )
        
        embed.add_field(
            name='🌱 Daily Practice',
            value='Regular check-ins help you stay aware of your mental health and catch issues early.',
            inline=False
        )
        
        embed.set_footer(text="Self-awareness is the first step to self-care 🌸")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction('💝')  # Heart gift
        await message.add_reaction('🌱')  # Growth
        await message.add_reaction('✨')  # Sparkles
    
    @commands.hybrid_command(name='selfcare', aliases=['care'], description='Get self-care suggestions')
    async def selfcare(self, ctx, category: str = None):
        """Get personalized self-care suggestions"""
        
        selfcare_activities = {
            'physical': [
                'Take a warm bath or shower',
                'Go for a gentle walk outside',
                'Do some light stretching',
                'Practice yoga or meditation',
                'Get enough sleep tonight',
                'Drink a glass of water',
                'Eat a nourishing meal',
                'Dance to your favorite music'
            ],
            'emotional': [
                'Write in a journal',
                'Call someone you care about',
                'Practice gratitude',
                'Allow yourself to cry if needed',
                'Listen to calming music',
                'Watch a comfort movie',
                'Practice self-compassion',
                'Set a boundary you need'
            ],
            'mental': [
                'Take breaks from social media',
                'Read a book you enjoy',
                'Practice a hobby you love',
                'Learn something new',
                'Organize a small space',
                'Do a puzzle or brain game',
                'Limit news consumption',
                'Practice mindfulness'
            ],
            'social': [
                'Reach out to a friend',
                'Join a support group',
                'Spend time with pets',
                'Video call family',
                'Write a thank you note',
                'Volunteer for a cause you care about',
                'Join an online community',
                'Practice active listening'
            ]
        }
        
        if category and category.lower() in selfcare_activities:
            activities = selfcare_activities[category.lower()]
            title = f'💆 {category.title()} Self-Care'
            color = 0x98FB98
        elif category:
            available = ', '.join(selfcare_activities.keys())
            await ctx.send(f'❌ Category not found! Available: {available}')
            return
        else:
            # Random activity from any category
            all_activities = []
            for activities in selfcare_activities.values():
                all_activities.extend(activities)
            activities = [random.choice(all_activities)]
            title = '💆 Self-Care Suggestion'
            color = 0x98FB98
        
        embed = discord.Embed(
            title=title,
            color=color,
            timestamp=datetime.utcnow()
        )
        
        if len(activities) == 1:
            embed.description = f'✨ {activities[0]}'
        else:
            suggestions = random.sample(activities, min(5, len(activities)))
            embed.add_field(
                name='Try one of these:',
                value='\n'.join([f'• {activity}' for activity in suggestions]),
                inline=False
            )
        
        embed.add_field(
            name='💝 Remember',
            value='Self-care isn\'t selfish - it\'s necessary. You deserve care and kindness.',
            inline=False
        )
        
        embed.set_footer(text="Small acts of self-care make a big difference 🌺")
        
        await ctx.send(embed=embed)
    
    @commands.hybrid_command(name='therapy', description='Information about therapy and mental health resources')
    async def therapy(self, ctx):
        """Get information about therapy and mental health support"""
        
        embed = discord.Embed(
            title='🛋️ Therapy & Mental Health Support',
            description='Professional mental health support can be incredibly helpful.',
            color=0x9370DB,  # Medium purple
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name='🔍 Finding a Therapist',
            value='• Psychology Today directory\n• Your insurance provider\'s website\n• Local community health centers\n• University counseling centers\n• Employee assistance programs',
            inline=False
        )
        
        embed.add_field(
            name='💻 Online Therapy Options',
            value='• BetterHelp\n• Talkspace\n• MDLIVE\n• Amwell\n• 7 Cups (peer support)',
            inline=False
        )
        
        embed.add_field(
            name='💰 Affordable Options',
            value='• Community mental health centers\n• Sliding scale fee therapists\n• Support groups\n• Crisis text lines\n• Mental health apps',
            inline=False
        )
        
        embed.add_field(
            name='🌟 What to Expect',
            value='Therapy is a safe space to explore your thoughts and feelings with a trained professional. It\'s okay to shop around for the right fit!',
            inline=False
        )
        
        embed.add_field(
            name='💙 Remember',
            value='Seeking therapy is a sign of strength, not weakness. You deserve support and care.',
            inline=False
        )
        
        embed.set_footer(text="Your mental health is just as important as your physical health 💚")
        
        await ctx.send(embed=embed)


async def setup(bot):
    """Setup function to add the cog"""
    await bot.add_cog(MentalHealth(bot))