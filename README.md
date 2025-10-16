# ☕ MochaBot

[![Discord.py](https://img.shields.io/badge/discord.py-2.3.0+-blue.svg)](https://github.com/Rapptz/discord.py)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/aurora9161/mochabot)

MochaBot is an advanced, coffee-themed Discord bot designed for community management and engagement. Built with Python and Discord.py, it features a beautiful custom help system, comprehensive moderation tools, fun games, and coffee-themed commands that will keep your server buzzing with activity!

## ✨ Features

### 🎛️ **Advanced Help System**
- **Interactive Help Menu** with button navigation
- **Beautiful Embeds** with coffee-themed design
- **Categorized Commands** for easy browsing
- **Command Details** with usage examples and cooldowns
- **Search Functionality** to find specific commands

### ☕ **Coffee Commands**
- Get random coffee suggestions and descriptions
- Brewing guides for different methods (espresso, pour-over, French press, cold brew)
- Coffee facts and quotes to fuel your day
- Caffeine content calculator for various drinks
- Coffee shop recommendations
- Random coffee images from APIs

### 🎮 **Fun & Games**
- Coffee-themed jokes and trivia
- Interactive games (Rock Paper Scissors, 8-Ball, Dice Rolling)
- Meme generator from Reddit
- Inspirational quotes
- Compliment generator
- And much more!

### 🛡️ **Moderation Tools**
- Comprehensive moderation commands (kick, ban, timeout, warn)
- Message management (clear, slowmode)
- Channel lockdown system
- Detailed logging with embeds
- Permission-based command access

### 🔧 **Utility Commands**
- Interactive polls with emoji reactions
- Reminder system
- Weather information (with API integration)
- QR code generator
- Base64 encoder/decoder
- Hash generator (MD5, SHA1, SHA256)
- Timestamp converter
- Color information display

### 📊 **General Commands**
- Bot and server information
- User profiles with detailed stats
- Ping and latency checking
- Avatar display
- System resource monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Discord Bot Token
- Git (for cloning)

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

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Discord bot token and other settings
   ```

4. **Run the bot**
   ```bash
   python bot.py
   ```

### Docker Setup (Alternative)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "bot.py"]
```

```bash
docker build -t mochabot .
docker run -d --env-file .env mochabot
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Required
DISCORD_TOKEN=your_discord_bot_token_here

# Optional
OPENWEATHER_API_KEY=your_api_key  # For weather commands
BOT_PREFIX=!                      # Default command prefix
LOG_LEVEL=INFO                    # Logging level
```

### Getting a Discord Bot Token

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section
4. Click "Add Bot"
5. Copy the token and add it to your `.env` file
6. Enable necessary intents:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent (optional)

### Inviting the Bot

1. In the Developer Portal, go to OAuth2 > URL Generator
2. Select "bot" and "applications.commands" scopes
3. Select necessary permissions:
   - Send Messages
   - Embed Links
   - Add Reactions
   - Use Slash Commands
   - Manage Messages (for moderation)
   - Kick Members (for moderation)
   - Ban Members (for moderation)
   - Moderate Members (for timeouts)
4. Use the generated URL to invite the bot

## 📝 Commands Overview

### ☕ Coffee Commands
- `!coffee` - Get a random coffee suggestion
- `!brew [method]` - Get brewing tips and guides
- `!coffeefact` - Learn interesting coffee facts
- `!coffeeapi` - Get random coffee images
- `!coffeequote` - Inspirational coffee quotes
- `!caffeine [drink]` - Check caffeine content
- `!coffeeshop` - Coffee shop recommendations

### 🎮 Fun Commands
- `!joke` - Coffee-themed jokes
- `!8ball <question>` - Magic 8-ball with coffee twist
- `!roll [dice]` - Roll dice (e.g., 2d6)
- `!flip` - Flip a coin
- `!choose <options>` - Choose between options
- `!rps <choice>` - Rock Paper Scissors
- `!trivia` - Coffee trivia questions
- `!meme` - Random memes from Reddit
- `!compliment [@user]` - Give compliments

### 🔧 Utility Commands
- `!poll <question> <option1> <option2>...` - Create polls
- `!remind <time> <message>` - Set reminders
- `!weather <city>` - Get weather info
- `!qr <text>` - Generate QR codes
- `!base64 <encode/decode> <text>` - Base64 operations
- `!hash <algorithm> <text>` - Generate hashes
- `!timestamp [unix_time]` - Timestamp converter
- `!color <hex>` - Color information

### 🛡️ Moderation Commands
- `!kick <member> [reason]` - Kick a member
- `!ban <member> [days] [reason]` - Ban a member
- `!unban <user_id> [reason]` - Unban a user
- `!timeout <member> <duration> [reason]` - Timeout a member
- `!untimeout <member> [reason]` - Remove timeout
- `!clear [amount]` - Clear messages
- `!slowmode [seconds]` - Set channel slowmode
- `!warn <member> [reason]` - Warn a member
- `!lockdown [action]` - Lock/unlock channel

### 📊 General Commands
- `!ping` - Check bot latency
- `!info` - Bot information
- `!serverinfo` - Server information
- `!userinfo [@user]` - User information
- `!avatar [@user]` - Display avatar

## 🎨 Customization

### Changing the Bot Color
Edit `BOT_COLOR` in each cog file or the main bot file:
```python
BOT_COLOR = 0x8B4513  # Coffee brown
```

### Adding New Commands
1. Create commands in existing cogs or create new cog files
2. Follow the existing pattern with hybrid commands
3. Add proper error handling and permission checks

### Custom Emojis
Replace the emoji variables in cog files with your server's custom emojis:
```python
self.emoji = '<:custom_emoji:emoji_id>'
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
4. **Commit your changes**
   ```bash
   git commit -m "Add amazing feature"
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions and classes
- Test your changes thoroughly
- Update documentation as needed

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/aurora9161/mochabot/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/aurora9161/mochabot/issues)
- **Discord Support**: [Join our support server](https://discord.gg/example)

## 📋 Roadmap

- [ ] Database integration for persistent data
- [ ] Web dashboard for bot configuration
- [ ] Music commands
- [ ] Economy system with coffee-themed currency
- [ ] Custom server settings
- [ ] Advanced logging system
- [ ] Slash command migration
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Discord.py** - The amazing Python library for Discord bots
- **Coffee API** - For providing coffee images
- **OpenWeatherMap** - Weather data provider
- **Various APIs** - For quotes, memes, and other content
- **Coffee Community** - For inspiration and testing

## ☕ Show Your Support

If you found this project helpful, please consider:
- ⭐ Starring the repository
- 🍴 Forking and contributing
- ☕ Buying me a coffee (links coming soon!)
- 💬 Sharing with your friends

---

<div align="center">
  <b>Made with ☕ and ❤️ by <a href="https://github.com/aurora9161">aurora9161</a></b>
  <br>
  <i>Keep brewing, keep coding!</i>
</div>