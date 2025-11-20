# Contributing to AI Meeting Summarizer

First off, thank you for considering contributing to AI Meeting Summarizer! 🎉

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details** (OS, Python version, Node version)

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Clear description** of the feature
- **Use case** - why would this be useful?
- **Possible implementation** (if you have ideas)

### Pull Requests

1. **Fork the repo** and create your branch from `main`
2. **Make your changes**
3. **Test thoroughly**
4. **Update documentation** if needed
5. **Follow code style** guidelines
6. **Write meaningful commit messages**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ai-meeting-summarizer.git
cd ai-meeting-summarizer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
npm install

# Create .env file
cp .env.example .env
# Add your API keys

# Run in development mode
npm start
```

## Code Style

### Python
- Follow **PEP 8**
- Use **docstrings** for functions
- Add **type hints** where appropriate
- Keep functions **focused** and **small**

### JavaScript
- Use **ES6+** syntax
- **camelCase** for variables and functions
- **Descriptive** variable names
- **Comments** for complex logic

### Commit Messages
```
feat: Add speaker diarization feature
fix: Resolve audio playback issue on Windows
docs: Update installation instructions
style: Format code with prettier
refactor: Simplify transcription agent
test: Add unit tests for summarizer
```

## Testing

```bash
# Run Python tests
pytest

# Run linting
flake8 backend/
eslint frontend/
```

## Project Structure

```
backend/agents/      # AI agent modules
backend/app.py       # Main Flask app
frontend/            # Electron frontend
electron/            # Electron main process
```

## Adding New Features

### Adding a New AI Agent

1. Create file in `backend/agents/`
2. Follow existing agent structure
3. Add initialization in `backend/app.py`
4. Update documentation

### Adding New Integration

1. Create agent file (e.g., `slack_sync.py`)
2. Add API routes in `backend/app.py`
3. Add UI in `frontend/index.html`
4. Add frontend logic in `frontend/app.js`
5. Update settings page
6. Document setup in README

## Questions?

Feel free to open an issue for discussion!

Thank you for contributing! 🚀
