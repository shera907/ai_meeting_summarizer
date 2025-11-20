# 🚀 Euron.one API Configuration Guide

## ✅ You're Using Euron.one API - Great Choice!

Euron.one provides OpenAI-compatible APIs at better prices. I've already updated your application to support it!

---

## 🔑 Your API Key (from screenshot)

Your API key: `euri-dg8...bbo` ✅

---

## ⚙️ **SETUP - 3 Easy Steps**

### **Step 1: Create/Edit `.env` file**

In your project root (`c:\AI_PROJECTS\ai_meeting_summarizer\`), create or edit the `.env` file:

```env
# ============================================
# Euron.one API Configuration
# ============================================

# Set this to true to use Euron.one
USE_EURON_API=true

# Your Euron.one API key (paste your full key here)
EURON_API_KEY=euri-dg8...bbo

# API endpoint (keep as is)
EURON_API_BASE=https://api.euron.one/api/v1/euri

# Model to use (you can change this)
EURON_MODEL=gpt-4.1-mini

# Transcription (keep Whisper - it's free and local)
TRANSCRIPTION_MODEL=whisper

# Keep these as false
USE_LOCAL_MODEL=false
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

---

### **Step 2: Replace with Your FULL API Key**

In the `.env` file, replace `euri-dg8...bbo` with your **complete API key** from the screenshot.

It should look like:
```env
EURON_API_KEY=euri-dg8xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbbo
```

---

### **Step 3: Start the App**

```bash
npm start
```

That's it! 🎉

---

## 🎯 **Available Models on Euron.one**

Based on your screenshot, you can use these models:

| Model | Use Case | Speed | Quality |
|-------|----------|-------|---------|
| **gpt-4.1-mini** ⭐ | Recommended | Fast | Excellent |
| **gpt-4.1-nano** | Fastest, cheaper | Very Fast | Good |
| **gpt-4.0-ultra** | Best quality | Medium | Best |

To change the model, edit `.env`:
```env
EURON_MODEL=gpt-4.1-mini   # or gpt-4.1-nano, gpt-4.0-ultra
```

---

## 💰 **Pricing**

Euron.one is typically **50-70% cheaper** than official OpenAI API!

Estimated costs per 30-minute meeting:
- **Transcription (Whisper)**: FREE ✅
- **Summary (GPT-4.1-mini)**: ~$0.005-0.01
- **Action Items (GPT-4.1-mini)**: ~$0.005-0.01

**Total: ~$0.01-0.02 per meeting** (very cheap!)

---

## 🧪 **Test Your Setup**

### **Quick Test:**

1. Make sure `.env` has your API key
2. Run: `npm start`
3. Record a 30-second test meeting
4. Check the console output for: `✓ Using Euron.one API with model: gpt-4.1-mini`

---

## 📝 **Complete `.env` File Example**

Here's a complete example (copy this):

```env
# ============================================
# AI Meeting Summarizer Configuration
# ============================================

# === EURON.ONE API (Recommended) ===
USE_EURON_API=true
EURON_API_KEY=euri-dg8xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbbo
EURON_API_BASE=https://api.euron.one/api/v1/euri
EURON_MODEL=gpt-4.1-mini

# === Transcription ===
TRANSCRIPTION_MODEL=whisper

# === Local Processing (not needed with Euron) ===
USE_LOCAL_MODEL=false

# === Other APIs (leave blank if using Euron) ===
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
DEEPGRAM_API_KEY=
ASSEMBLYAI_API_KEY=

# === Backend Configuration ===
FLASK_PORT=5000
FLASK_HOST=localhost
DEBUG=true
SECRET_KEY=change-this-to-a-random-secret-key

# === Database ===
DATABASE_PATH=./data/meetings.db

# === Integration APIs (Optional) ===
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
NOTION_API_KEY=
JIRA_API_URL=
JIRA_API_TOKEN=
JIRA_EMAIL=
```

---

## 🔧 **How It Works**

Your app now:

1. **Transcribes audio** using Whisper (local, free) ✅
2. **Sends transcript** to Euron.one API at `https://api.euron.one/api/v1/euri`
3. **Uses GPT-4.1-mini** model for:
   - Meeting summaries
   - Action item extraction
4. **Saves results** to your local database

---

## 🆚 **Euron.one vs Official OpenAI**

| Feature | Euron.one | Official OpenAI |
|---------|-----------|-----------------|
| **Cost** | 50-70% cheaper | Standard pricing |
| **Models** | GPT-4.1 variants | GPT-4 Turbo, GPT-3.5 |
| **API** | OpenAI-compatible | Official |
| **Speed** | Similar | Similar |
| **Reliability** | Good | Excellent |

---

## 🚨 **Troubleshooting**

### **Error: "Invalid API key"**
- Check your `.env` file has the complete API key
- Make sure no spaces before/after the key
- Verify the key is still active on Euron.one dashboard

### **Error: "Connection refused"**
- Check internet connection
- Verify `EURON_API_BASE` is set to: `https://api.euron.one/api/v1/euri`

### **Error: "Model not found"**
Try these models:
```env
EURON_MODEL=gpt-4.1-mini    # Recommended
# or
EURON_MODEL=gpt-4.1-nano    # Cheaper/faster
# or
EURON_MODEL=gpt-4.0-ultra   # Best quality
```

### **Not using Euron.one?**
Check your `.env` file:
```env
USE_EURON_API=true    # Must be true!
```

---

## 📊 **Verify It's Working**

When you start the app, check the console output:

**You should see:**
```
✓ Using Euron.one API with model: gpt-4.1-mini
Backend: Starting...
✓ Whisper model loaded
```

**If you see this instead:**
```
✓ Using official OpenAI API
```
Then `USE_EURON_API=true` is not set correctly in `.env`.

---

## 🎓 **Advanced: Testing the API Directly**

You can test your Euron.one API key directly with curl:

```bash
curl -X POST https://api.euron.one/api/v1/euri/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_FULL_API_KEY_HERE" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}],
    "model": "gpt-4.1-mini"
  }'
```

You should get a response with AI-generated text.

---

## ✅ **Final Checklist**

Before running `npm start`:

- [ ] `.env` file created in project root
- [ ] `USE_EURON_API=true` is set
- [ ] `EURON_API_KEY=` has your **complete** API key (not just `euri-dg8...bbo`)
- [ ] `EURON_MODEL=gpt-4.1-mini` is set
- [ ] `TRANSCRIPTION_MODEL=whisper` is set
- [ ] Dependencies installed (`pip install -r requirements.txt` and `npm install`)

---

## 🚀 **Ready to Go!**

1. **Edit your `.env` file** with your complete API key
2. **Run: `npm start`**
3. **Record a test meeting**
4. **Enjoy AI-powered summaries!** 🎉

Your setup is now using:
- ✅ **Whisper** (local, free) for transcription
- ✅ **Euron.one GPT-4.1-mini** for summaries & action items
- ✅ **Cost**: ~$0.01 per meeting (very cheap!)

---

## 📞 **Need Help?**

If you have issues:
1. Check your `.env` file (make sure API key is complete)
2. Run `python test_installation.py`
3. Check console output when you run `npm start`
4. Verify your Euron.one API key is active

---

**You're all set with Euron.one! Much cheaper than OpenAI and just as good!** 🎊

