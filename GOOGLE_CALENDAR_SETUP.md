# Google Calendar Integration Setup

## Prerequisites
1. A Google account
2. Python packages installed (run `pip install -r requirements.txt`)

## Setup Steps

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Calendar API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

### 2. Create OAuth 2.0 Credentials
1. Go to "APIs & Services" > "Credentials"
2. Click "+ CREATE CREDENTIALS" > "OAuth client ID"
3. Configure the OAuth consent screen if prompted:
   - Choose "External" for User Type
   - Fill in App name, user support email, and developer contact
   - Add scope: `https://www.googleapis.com/auth/calendar.events`
   - Add test users (your email)
   - Save and continue
4. Create OAuth Client ID:
   - Application type: **Web application**
   - Name: "AI Meeting Summarizer"
   - Authorized redirect URIs: `http://localhost:5000/api/google/callback`
   - Click "Create"
5. Download the JSON file (click the download icon)
6. Rename it to `google_credentials.json`
7. Move it to the `data/` folder in your project

### 3. Connect in the App
1. Launch the app (`npm start`)
2. Go to Settings
3. Click "Connect to Google" under Integrations
4. Authorize the app in your browser
5. You'll see "✅ Connected" when successful

### 4. Sync Action Items
1. Open any meeting with action items
2. Click "📅 Sync to Google Calendar"
3. Action items will appear in your Google Calendar!

## Troubleshooting

**Error: "Google OAuth credentials file not found"**
- Make sure `google_credentials.json` is in the `data/` folder

**Error: "Not authenticated with Google Calendar"**
- Go to Settings and click "Connect to Google"

**401 Unauthorized**
- Your OAuth token may have expired
- Delete `data/google_token.json` and reconnect

## Privacy & Security
- Credentials are stored locally in the `data/` folder
- No data is sent to third parties
- You can revoke access anytime from [Google Account Permissions](https://myaccount.google.com/permissions)

