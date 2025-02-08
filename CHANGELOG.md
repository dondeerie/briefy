# Changelog

## [1.0.0] - 2024-02-07
### Added
- Initial release
- Text summarization functionality
- Support for PDF and DOCX files
- Web URL summarization
- Dark mode feature
- Summary history
- Multi-language support (English, Spanish, French)
- OpenAI integration
- Frontend React implementation
- Backend FastAPI server

### Fixed
- Language preservation in summaries
- CORS issues
- Git repository structure
- Dark mode styling consistency

# CONTRIBUTING.md
# Contributing to Briefy

## Getting Started
1. Fork the repository
2. Create a new branch for your feature
3. Make your changes
4. Submit a pull request

## Code Style
- Follow PEP 8 for Python code
- Use ESLint standards for JavaScript/React
- Comment your code when necessary
- Keep functions small and focused

## Pull Request Process
1. Update documentation if needed
2. Add tests if applicable
3. Update CHANGELOG.md
4. Request review from maintainers

## Development Setup
1. Install dependencies
2. Set up environment variables
3. Run tests before submitting

# Updates to README.md
# Briefy 🚀

[Existing badges]

## Features Showcase
[Add screenshots or GIFs here showing:]
- Text summarization
- File upload
- Dark mode
- Multi-language support

## Quick Start
```bash
# Clone repository
git clone https://github.com/yourusername/briefy.git

# Frontend setup
cd frontend
npm install
npm start

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py