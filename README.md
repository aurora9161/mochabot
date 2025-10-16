# ☕ MochaBot - Mental Health & Coffee Community Support

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Mental Health](https://img.shields.io/badge/focus-Mental%20Health-blue.svg)](#mental-health-features)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/aurora9161/mochabot)

> **Combining the comfort of coffee culture with mental health resources and therapeutic support**

MochaBot is an advanced Discord bot that creates a safe, supportive environment where coffee culture meets mental wellness. Designed for communities focused on mental health, therapy support groups, and wellness-oriented servers, it provides both engaging coffee-themed features and comprehensive mental health resources.

## 🎯 **Mission Statement**

To provide a digital safe space where the warmth of coffee culture combines with evidence-based mental health tools, creating supportive communities that prioritize both connection and wellbeing.

## ✨ Key Features

### 🧠 **Mental Health & Therapy Support**
- **Crisis Resources** with international helplines and emergency contacts
- **Daily Wellness Check-ins** for mood tracking and self-reflection
- **Guided Breathing Exercises** for anxiety and panic management
- **Grounding Techniques** including 5-4-3-2-1 method and progressive muscle relaxation
- **Positive Affirmations** for self-esteem and motivation
- **Mood Tracking** with personalized insights and support
- **Self-Care Suggestions** across physical, emotional, mental, and social dimensions
- **Therapy Resources** including finding therapists and online therapy options
- **Mindfulness Tools** for present-moment awareness

### 🎛️ **Advanced Help System**
- **Mental Health Quick Access** button for immediate support
- **Interactive Help Menu** with crisis resource integration
- **Categorized Commands** with therapy-focused organization
- **Command Details** including mental health context
- **Safe Space Indicators** for sensitive commands

### ☕ **Coffee-Themed Community Building**
- Coffee suggestions and brewing guides for community bonding
- Coffee facts and quotes that promote mindfulness
- Caffeine content calculator for health awareness
- Coffee shop recommendations for social connection
- Random coffee images for mood enhancement

### 🎮 **Therapeutic Games & Activities**
- Coffee-themed humor for mood lifting
- Interactive trivia for cognitive engagement
- Stress-relief games and activities
- Compliment generator for positive reinforcement
- Creative exercises for emotional expression

### 🔧 **Community Wellness Tools**
- Anonymous polls for group feedback
- Reminder system for self-care activities
- QR codes for sharing resources
- Wellness check broadcast system
- Support group coordination tools

### 🛡️ **Safe Space Moderation**
- Trauma-informed moderation tools
- Gentle warning system
- Crisis intervention protocols
- Content filtering for mental health safety
- Support-focused timeout system

## 🆘 **Crisis Support Features**

### **Immediate Access**
- `!crisis` - International crisis helplines
- `!therapy` - Professional therapy resources
- `!breathe` - Emergency breathing exercises
- `!ground` - Panic attack grounding techniques

### **Safety Measures**
- 24/7 crisis resource availability
- Privacy-focused mental health tracking
- Non-judgmental automated responses
- Professional resource recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Understanding of mental health community needs

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aurora9161/mochabot.git
   cd mochabot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure for mental health support**
   ```bash
   cp .env.example .env
   # Edit .env with your Discord bot token
   ```

4. **Run MochaBot**
   ```bash
   python bot.py
   ```

## 🏥 **Setting Up Mental Health Channels**

For optimal mental health support, create these channels:

- `#wellness` - Daily wellness reminders
- `#mental-health` - Mental health discussions
- `#support` - Peer support conversations
- `#daily-wellness` - Automated wellness checks
- `#self-care` - Self-care tips and activities
- `#crisis-resources` - Crisis support information

## 📝 **Mental Health Commands**

### 🆘 **Crisis & Support**
- `!crisis [country]` - Emergency mental health resources
- `!therapy` - Find professional mental health support
- `!breathe [exercise]` - Guided breathing exercises
- `!ground [technique]` - Grounding techniques for anxiety

### 🌸 **Daily Wellness**
- `!checkin` - Daily mental health reflection
- `!mood <1-10> [notes]` - Track and log your mood
- `!affirmation` - Receive positive affirmations
- `!selfcare [category]` - Personalized self-care suggestions

### ☕ **Coffee & Community**
- `!coffee` - Random coffee suggestions for social bonding
- `!brew [method]` - Brewing guides as mindfulness practice
- `!coffeefact` - Educational coffee content
- `!coffeeapi` - Mood-boosting coffee images

### 🎮 **Wellness Activities**
- `!joke` - Light humor for mood enhancement
- `!compliment [@user]` - Spread positivity
- `!quote` - Inspirational quotes
- `!trivia` - Engaging mental stimulation

## 🤝 **Community Guidelines**

### **For Mental Health Communities**
1. **Respect Privacy** - Never pressure sharing personal details
2. **No Diagnosis** - Avoid giving medical advice
3. **Crisis Protocol** - Always direct to `!crisis` for emergencies
4. **Inclusive Support** - Welcome all mental health experiences
5. **Professional Boundaries** - Encourage professional help when needed

### **Safe Space Principles**
- Trauma-informed interactions
- Non-judgmental automated responses
- Privacy-focused data handling
- Crisis-aware content filtering
- Supportive community building

## 🔒 **Privacy & Safety**

- **No Personal Data Storage** - Mood logs are not permanently stored
- **Anonymous Crisis Access** - Crisis resources available without logging
- **Safe Command Design** - Mental health commands include safety disclaimers
- **Professional Referrals** - Always recommend professional help for serious issues

## ⚙️ **Configuration for Therapy Groups**

### Environment Variables
```env
# Required
DISCORD_TOKEN=your_bot_token

# Mental Health Focused Settings
BOT_PREFIX=!
MENTAL_HEALTH_MODE=true
CRISIS_PING_ROLE=crisis-support
WELLNESS_CHANNEL=wellness
```

### Therapy Group Features
- Automated wellness check-ins
- Mood tracking without permanent storage
- Crisis resource quick access
- Anonymous support tools
- Professional therapy resource database

## 👩‍⚕️ **For Mental Health Professionals**

### Integration Benefits
- **Client Engagement** - Interactive tools for therapy homework
- **Mood Tracking** - Simple mood monitoring between sessions
- **Crisis Resources** - 24/7 crisis support availability
- **Community Building** - Safe peer support environment
- **Wellness Reminders** - Automated self-care prompts

### Professional Use Cases
- Support group servers
- Therapy practice community building
- Mental health education servers
- Peer support networks
- Wellness-focused Discord communities

## 🐛 **Troubleshooting**

### **Mental Health Commands Not Working**
- Ensure mental health cog is loaded
- Check channel permissions for sensitive content
- Verify crisis resource links are current

### **Crisis Command Issues**
- Update crisis resources regularly
- Test international helpline numbers
- Ensure 24/7 availability

## 📄 **Disclaimer**

**Important:** MochaBot is designed to support mental wellness but is not a replacement for professional mental health care. If you or someone you know is in crisis, please contact emergency services or a mental health professional immediately.

- Bot tools are supportive, not therapeutic
- Crisis resources should be verified regularly
- Professional help is always recommended for serious mental health concerns
- This bot is not supervised by mental health professionals

## 🤝 **Contributing to Mental Health Support**

### **Ways to Help**
1. **Update Crisis Resources** - Keep helplines current
2. **Add Therapeutic Activities** - Contribute wellness exercises
3. **Improve Safety Features** - Enhance crisis detection
4. **Expand Language Support** - Make resources more accessible
5. **Test with Communities** - Gather feedback from mental health servers

### **Mental Health-Focused Development**
- Follow trauma-informed design principles
- Research evidence-based mental health tools
- Prioritize privacy and safety
- Collaborate with mental health professionals
- Test in real support communities

## 🔗 **Mental Health Resources**

### **Crisis Lines (24/7)**
- **US**: 988 (Suicide & Crisis Lifeline)
- **UK**: 116 123 (Samaritans)
- **Canada**: 1-833-456-4566 (Talk Suicide Canada)
- **Australia**: 13 11 14 (Lifeline)
- **International**: Use `!crisis <country>` for local resources

### **Professional Support**
- [Psychology Today](https://www.psychologytoday.com/) - Find therapists
- [BetterHelp](https://www.betterhelp.com/) - Online therapy
- [NAMI](https://www.nami.org/) - Mental health education
- [Mental Health America](https://www.mhanational.org/) - Resources and support

## 🏆 **Awards & Recognition**

*Designed with input from mental health advocates and support communities*

## 📄 **License**

This project is licensed under the MIT License with a focus on mental health community support - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Mental Health Advocates** - For guidance on community needs
- **Crisis Intervention Specialists** - For safety protocol advice
- **Discord Therapy Communities** - For real-world testing and feedback
- **Coffee Communities** - For the inspiration behind the coffee theme
- **Open Source Mental Health Projects** - For shared resources and approaches

## ☕💙 **Show Your Support**

If MochaBot has supported your mental health community:
- ⭐ Star the repository to show appreciation
- 🍴 Fork and contribute mental health improvements
- 💬 Share with other mental health communities
- ☕ Support the developer (coffee fund coming soon!)
- 💙 Spread awareness about mental health resources

---

<div align="center">
  <h3>💙 Remember: You Matter, You're Not Alone, and Help is Available 💙</h3>
  <p><strong>Crisis? Text "HELLO" to 741741 (US) or use <code>!crisis</code> for international resources</strong></p>
  <br>
  <p><em>Made with ☕, 💙, and deep care for mental health by <a href="https://github.com/aurora9161">aurora9161</a></em></p>
  <p><em>"In a world where you can be anything, be kind - especially to yourself"</em></p>
</div>