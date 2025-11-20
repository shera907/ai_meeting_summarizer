# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainers directly (see package.json for contact)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours and work with you to address the issue.

## Security Best Practices

### API Keys

- **NEVER** commit API keys to the repository
- Use `.env` file for all sensitive credentials
- The `.env` file is in `.gitignore` by default

### Data Privacy

- All recordings are stored **locally** in the `data/` folder
- Transcripts and summaries are only sent to AI APIs if configured
- Use **offline mode** for maximum privacy

### Local Storage

- Database: SQLite file in `data/meetings.db`
- Audio files: Stored in `data/audio/`
- No data is sent to external servers except:
  - AI API calls (if using OpenAI, Anthropic, etc.)
  - Integration syncs (if you enable Google Calendar, Notion, Jira)

### Offline Mode

For maximum security and privacy:

```env
USE_LOCAL_MODEL=true
TRANSCRIPTION_MODEL=whisper
```

This ensures:
- No data leaves your computer
- All processing happens locally
- No internet connection required

### Network Security

- Backend runs on `localhost:5000` only
- No external network access required for basic operation
- CORS is configured for local frontend only

### Recommended Practices

1. **Keep dependencies updated**: Run `npm audit` and `pip list --outdated`
2. **Use strong API keys**: If using cloud services
3. **Enable offline mode**: For sensitive meetings
4. **Encrypt backups**: If backing up the `data/` folder
5. **Review integrations**: Only connect services you trust

## Known Limitations

- Audio files are stored unencrypted
- Database is not encrypted
- API keys in `.env` are in plain text

To enhance security:
- Use full-disk encryption on your system
- Store the project folder in an encrypted directory
- Use a password manager for API keys

## Updates

We will release security updates as needed. Keep your installation up to date:

```bash
git pull
npm install
pip install -r requirements.txt --upgrade
```

## Audit

This project has not undergone a professional security audit. Use at your own discretion, especially for sensitive information.

