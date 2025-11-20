# 🚀 Quick Start Guide

Get up and running with AI Meeting Summarizer in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8 or higher (`python --version`)
- ✅ Node.js 18 or higher (`node --version`)
- ✅ Git (`git --version`)

## Step-by-Step Setup

### 1. Get API Keys (5 minutes)

#### Deepgram (Required - Free tier available)
1. Go to [console.deepgram.com](https://console.deepgram.com)
2. Sign up for free account
3. Get API key from dashboard
4. Save it somewhere safe

#### Euron.one (Required)
1. Visit [euron.one](https://euron.one)
2. Create account
3. Get API key
4. Save it

### 2. Install & Configure (2 minutes)

```bash
# Clone repository
git clone https://github.com/yourusername/ai-meeting-summarizer.git
cd ai-meeting-summarizer

# Setup Python
python -m venv venv
venv\Scripts\activate     # Windows
# OR
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
npm install

# Create .env file
# Windows:
copy .env.example .env
# macOS/Linux:
cp .env.example .env
```

### 3. Add Your API Keys (1 minute)

Open `.env` in any text editor and add your keys:

```env
TRANSCRIPTION_MODEL=deepgram
DEEPGRAM_API_KEY=YOUR_DEEPGRAM_KEY_HERE

USE_EURON_API=true
EURON_API_KEY=YOUR_EURON_KEY_HERE
EURON_API_BASE=https://api.euron.one/v1
EURON_MODEL=gpt-4.1-mini
```

### 4. Launch! (30 seconds)

```bash
npm start
```

Wait 10 seconds for both backend and frontend to start.

---

## 🎯 Your First Meeting

### Record
1. Click **"New Meeting"** in sidebar
2. Enter title (e.g., "Test Meeting")
3. Click **"Start Recording"**
4. Speak for at least 30 seconds:
   > "Hello, this is a test meeting. I need to prepare demo slides by Friday. John should review the documentation. We'll schedule a follow-up meeting next week."
5. Click **"Stop Recording"**
6. Wait ~30 seconds for processing

### View Results
- See AI-generated summary
- Check extracted action items
- Play back audio
- Edit title if needed

---

## 🎨 Optional: Setup Integrations

### Google Calendar (10 minutes)
See [GOOGLE_CALENDAR_SETUP.md](GOOGLE_CALENDAR_SETUP.md)

### Notion (2 minutes)
1. Get API key from [notion.so/my-integrations](https://notion.so/my-integrations)
2. Go to Settings → Integrations
3. Paste API key
4. Click "Export to Notion" from any meeting

### Jira (3 minutes)
1. Go to Settings → Integrations → Jira
2. Enter:
   - Server URL
   - Email
   - API Token ([create token](https://id.atlassian.com/manage-profile/security/api-tokens))
   - Project Key
3. Click "Configure Jira"

---

## ❓ Common Issues

### "Backend not connecting"
- Wait 10 seconds after starting
- Check terminal for error messages
- Verify API keys in `.env`

### "No transcription appearing"
- Check Deepgram API key
- Verify internet connection
- Speak clearly for at least 10 seconds

### "Import errors"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

---

## 🎓 Learn More

- [Full Documentation](README.md)
- [Troubleshooting Guide](README.md#troubleshooting)
- [Contributing](CONTRIBUTING.md)

---

**Need help? Open an issue on GitHub!**

Happy meeting summarizing! 🎉
