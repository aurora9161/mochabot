# 🧠 MochaBot Mental Health Setup Guide

> **Quick setup guide for mental health communities and therapy support groups**

## 🎯 Purpose

MochaBot combines the comfort of coffee culture with evidence-based mental health tools, creating a safe digital space for:
- Mental health support communities
- Therapy group servers
- Wellness-focused Discord communities
- Peer support networks
- Crisis intervention resources

## ⚡ Quick Start (5 Minutes)

### 1. **Essential Setup**
```bash
# Clone and install
git clone https://github.com/aurora9161/mochabot.git
cd mochabot
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your Discord bot token to .env file

# Run
python bot.py
```

### 2. **Create Mental Health Channels**
Create these channels for optimal support:
- `#wellness` - Daily wellness reminders
- `#mental-health` - Mental health discussions  
- `#support` - Peer support conversations
- `#crisis-resources` - Emergency resources

### 3. **Test Crisis Features**
```
!crisis        # Test crisis resources
!breathe       # Test breathing exercises
!checkin       # Test wellness check-in
!help          # See mental health quick access
```

## 🆘 **Critical Crisis Support**

### **Immediate Access Commands**
- `!crisis` - International crisis helplines (24/7)
- `!crisis US` - US-specific resources
- `!crisis UK` - UK-specific resources
- `!therapy` - Find professional therapy support

### **Emergency Features**
- ✅ 24/7 crisis resource availability
- ✅ International helpline database
- ✅ No data logging for crisis commands
- ✅ Anonymous access to all resources

## 🌸 **Daily Wellness Tools**

### **Mental Health Commands**
```bash
!checkin           # Daily mental health reflection
!mood 7 "feeling better today"  # Mood tracking (1-10)
!affirmation       # Positive affirmations
!breathe           # Guided breathing exercises
!ground            # Grounding techniques for anxiety
!selfcare physical # Self-care suggestions by category
```

### **Automated Wellness**
- ✅ Daily wellness reminders (every 12 hours)
- ✅ Supportive keyword responses
- ✅ Mental health awareness in welcomes
- ✅ Crisis-aware content filtering

## 🛋️ **For Therapy Groups**

### **Professional Integration**
- **Mood Tracking** - Simple between-session monitoring
- **Homework Tools** - Interactive exercises for therapy assignments
- **Crisis Safety** - 24/7 emergency resource access
- **Group Support** - Peer connection tools
- **Resource Sharing** - Easy therapy resource distribution

### **Privacy Features**
- No permanent mood data storage
- Anonymous crisis resource access
- HIPAA-aware design principles
- No personal information required

## ⚙️ **Advanced Configuration**

### **Environment Variables**
```env
# Basic Setup
DISCORD_TOKEN=your_bot_token_here
BOT_PREFIX=!

# Mental Health Settings
MENTAL_HEALTH_MODE=true
CRISIS_PING_ROLE=crisis-support
WELLNESS_CHANNEL=wellness
```

### **Bot Permissions Needed**
- Send Messages
- Embed Links
- Add Reactions
- Manage Messages (for safety)
- Read Message History

## 🛡️ **Safety Features**

### **Built-in Protections**
- Crisis keyword detection and response
- Gentle, non-judgmental automated replies
- Professional resource recommendations
- Privacy-first design
- Trauma-informed interactions

### **Content Safety**
- Mental health-aware moderation tools
- Supportive warning system
- Crisis intervention protocols
- Safe space preservation

## 👩‍⚕️ **For Mental Health Professionals**

### **Use Cases**
- **Support Groups** - Facilitate peer connections
- **Therapy Practice** - Client engagement tools
- **Education** - Mental health awareness servers
- **Crisis Prevention** - 24/7 resource availability
- **Wellness Tracking** - Simple mood monitoring

### **Professional Benefits**
- Evidence-based tool integration
- Crisis resource standardization
- Community engagement enhancement
- Automated wellness reminders
- Safe peer support facilitation

## 📊 **Community Wellness Features**

### **Interactive Tools**
- Daily check-ins with reflection questions
- Mood tracking with supportive responses
- Breathing exercises for panic/anxiety
- Grounding techniques for dissociation
- Self-care suggestions across all dimensions

### **Community Building**
- Coffee-themed social connection
- Positive affirmation sharing
- Compliment exchange system
- Wellness-focused games and activities
- Mental health education integration

## ⚠️ **Important Disclaimers**

### **Professional Boundaries**
- 🚫 Bot is **NOT** a replacement for professional therapy
- 🚫 Does **NOT** provide medical or psychological advice
- 🚫 Crisis situations require **human professional intervention**
- ✅ Bot **SUPPORTS** existing mental health care
- ✅ Encourages professional help-seeking

### **Crisis Protocol**
1. **Immediate Danger** → Call emergency services (911, 999, 112)
2. **Mental Health Crisis** → Use `!crisis` for local helplines
3. **Ongoing Support** → Use `!therapy` to find professional help
4. **Daily Wellness** → Use other mental health commands as supplements

## 🔗 **Quick Reference**

### **Essential Commands**
| Command | Purpose | Usage |
|---------|---------|-------|
| `!crisis` | Emergency resources | `!crisis` or `!crisis US` |
| `!breathe` | Breathing exercises | `!breathe` or `!breathe box` |
| `!checkin` | Daily wellness check | `!checkin` |
| `!mood` | Mood tracking | `!mood 6 having an okay day` |
| `!therapy` | Find professional help | `!therapy` |
| `!selfcare` | Self-care suggestions | `!selfcare emotional` |

### **Crisis Resources (24/7)**
- **US**: 988 (Suicide & Crisis Lifeline)
- **UK**: 116 123 (Samaritans)
- **Canada**: 1-833-456-4566 (Talk Suicide Canada)
- **Australia**: 13 11 14 (Lifeline)
- **Crisis Text**: Text HOME to 741741 (US)

## 🤝 **Community Support**

- **Issues**: [GitHub Issues](https://github.com/aurora9161/mochabot/issues)
- **Mental Health Focus**: Label issues with "mental-health"
- **Crisis Resource Updates**: High priority for community safety
- **Professional Consultation**: Welcome input from mental health professionals

---

<div align="center">
  <h3>💙 Remember: This is a tool to support, not replace, professional mental health care 💙</h3>
  <p><strong>If you're in crisis, please reach out to a human professional immediately</strong></p>
  <p><em>Your mental health matters, and you deserve support</em></p>
</div>