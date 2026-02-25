# 🚀 How to Start the Application

## Method 1: Using npm (Recommended)
```powershell
cd C:\Users\scl\Videos\meetingsummary\AI_meeting_summarizer
npm start
```

## Method 2: Using Node directly
```powershell
cd C:\Users\scl\Videos\meetingsummary\AI_meeting_summarizer
node start.js
```

## Method 3: Double-click
1. Navigate to: `C:\Users\scl\Videos\meetingsummary\AI_meeting_summarizer`
2. Double-click `RUN.bat`

---

## What Happens When You Start:
1. ✅ Flask backend starts on `http://127.0.0.1:5000`
2. ✅ Electron desktop app opens automatically
3. ✅ You're ready to record meetings!

---

## To Stop the Application:
- Close the Electron window
- Or press `Ctrl+C` in the terminal

---

## Troubleshooting:
- **If nothing happens**: Make sure you're in the `AI_meeting_summarizer` directory
- **If backend fails**: Check that Python venv is properly installed
- **If frontend doesn't open**: Wait 5-10 seconds for backend to start first

---

## All Settings:
Edit `.env` file to configure integrations (Google Calendar, Notion, Jira, etc.)

See `INTEGRATION_SETUP.md` for detailed configuration guide.

