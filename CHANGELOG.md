# Changelog

All notable changes to AI Meeting Summarizer will be documented in this file.

## [1.0.0] - 2025-11-20

### Added
- 🎙️ Local audio capture with microphone recording
- ⚡ Real-time transcription (10-second chunks) using Deepgram
- 🤖 AI-powered meeting summarization with Euron.one GPT-4.1 mini
- 📋 Automatic action item extraction with priorities
- 🎯 Smart task list generation
- 📅 Google Calendar integration for action item sync
- 📝 Notion export for meeting notes
- 🎯 Jira task creation from action items
- 🌐 Multi-language translation (12+ languages)
- 🔔 Desktop notifications for all major events
- ✏️ Meeting title editing
- 🎵 Audio playback in meeting details
- 🔍 Advanced search and filtering (date, title, action status)
- 👥 Participant tracking
- 💾 Local SQLite database storage
- 🎨 Modern, dark-themed UI
- ⚙️ Comprehensive settings panel

### Technical Implementation
- Electron desktop framework
- Python Flask backend with Socket.IO
- SQLAlchemy ORM with SQLite
- Deepgram API for transcription
- Euron.one API for AI processing
- Real-time chunk-based transcription
- Enhanced detailed summary prompts

### Documentation
- Complete README with installation guide
- Google Calendar setup documentation
- Contributing guidelines
- MIT License

---

## Future Releases

### [1.1.0] - Planned
- Speaker diarization (identify who said what)
- Meeting templates
- Export to PDF
- Custom action item templates

### [1.2.0] - Planned
- Meeting analytics dashboard
- Team collaboration features
- Cloud sync option
- Mobile companion app

---

**Note:** This project follows [Semantic Versioning](https://semver.org/)
