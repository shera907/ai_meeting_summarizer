# Python Virtual Environment Setup for AI Meeting Summarizer

## ✅ YES, You Should Use venv!

Using a virtual environment (venv) is **highly recommended** for Python projects to avoid dependency conflicts.

---

## 🚀 Quick Setup (2 minutes)

### **Step 1: Create Virtual Environment**

```bash
# In your project root (c:\AI_PROJECTS\ai_meeting_summarizer)
python -m venv venv
```

This creates a `venv` folder with isolated Python environment.

---

### **Step 2: Activate venv**

**Windows (PowerShell):**
```bash
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You'll see `(venv)` prefix in your terminal when activated.

---

### **Step 3: Install Dependencies**

```bash
# With venv activated
pip install --upgrade pip
pip install -r requirements.txt
```

---

### **Step 4: Run the App**

```bash
# Still with venv activated
npm start
```

---

## 📦 What Gets Installed?

With Euron.one setup, you need these essential packages:

### **Core (Required):**
- `flask` - Backend server
- `flask-socketio` - Real-time communication
- `sqlalchemy` - Database
- `openai` - For Euron.one API (OpenAI-compatible)
- `openai-whisper` - Local transcription
- `sounddevice` - Audio recording
- `python-dotenv` - Environment variables

### **Optional (Not needed for Euron.one):**
- `anthropic` - Only if you want Claude support
- `llama-cpp-python` - Only for local LLM models
- `torch` - Only for local models
- `transformers` - Only for local models

---

## 🎯 Minimal Installation (Euron.one Setup)

If you only want Euron.one + Whisper (no Claude, no local models):

```bash
# Activate venv first
pip install flask flask-cors flask-socketio
pip install sqlalchemy python-dotenv
pip install openai openai-whisper
pip install sounddevice soundfile pyaudio
pip install requests python-dateutil
```

---

## 🔧 Update requirements.txt (Optional Packages)

Edit `requirements.txt` to make some packages optional:

```txt
# Core Framework
flask==3.0.0
flask-cors==4.0.0
flask-socketio==5.3.5

# Audio Processing
pyaudio==0.2.14
sounddevice==0.4.6
soundfile==0.12.1

# AI & Transcription (Core)
openai-whisper==20231117
openai==1.12.0
python-dotenv==1.0.1

# Database
sqlalchemy==2.0.25

# Utilities
requests==2.31.0
python-dateutil==2.8.2

# === OPTIONAL PACKAGES (uncomment if needed) ===

# Claude/Anthropic support (not needed for Euron.one)
# anthropic==0.18.1

# Local LLM support (not needed if using Euron.one)
# llama-cpp-python==0.2.55
# transformers==4.37.2
# torch==2.2.0

# LangChain/CrewAI (advanced features)
# langchain==0.1.9
# langchain-openai==0.0.6
# langgraph==0.0.25
# crewai==0.1.25

# Task Integrations (install only if you need them)
# google-api-python-client==2.119.0
# google-auth-httplib2==0.2.0
# google-auth-oauthlib==1.2.0
# notion-client==2.2.1
# jira==3.6.0
```

---

## 🐍 Verify Your Setup

```bash
# Check Python version (should be 3.8+)
python --version

# Check if venv is active (should show path inside venv folder)
python -c "import sys; print(sys.prefix)"

# Check installed packages
pip list
```

---

## 💡 Pro Tips

### **1. Always Activate venv**
Before running the app, always activate venv:
```bash
venv\Scripts\Activate.ps1  # Windows
```

### **2. Deactivate venv**
When done:
```bash
deactivate
```

### **3. Update Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

### **4. Add venv to .gitignore**
The `venv/` folder is already in `.gitignore` - don't commit it!

---

## 🆘 Common Issues

### **"venv\Scripts\Activate.ps1 cannot be loaded"**
Run PowerShell as Administrator:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **"pip not found"**
Make sure venv is activated. Try:
```bash
python -m pip install -r requirements.txt
```

### **"anthropic not found"**
You don't need it for Euron.one! The code now handles it as optional.

---

## ✅ Your Setup Checklist

- [ ] Create venv: `python -m venv venv`
- [ ] Activate venv: `venv\Scripts\Activate.ps1`
- [ ] Install core packages: `pip install flask flask-socketio openai openai-whisper sounddevice sqlalchemy python-dotenv`
- [ ] Setup `.env` file with Euron.one API key
- [ ] Run: `npm start`

---

## 🎊 Done!

With venv active and Euron.one configured:

```bash
# 1. Activate venv
venv\Scripts\Activate.ps1

# 2. Run app
npm start

# 3. Record meetings!
```

**Your environment is now clean, isolated, and ready!** 🚀

