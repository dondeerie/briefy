# Troubleshooting Guide for Briefy

## Common Installation Issues

### Node.js and npm Issues
- Error: "npm error could not determine executable to run"
  Solution: Remove package.json and node_modules, then run `npx create-react-app .`
  Prevention: Always initialize React app before installing additional dependencies

- Error: "node_modules appears to be a git submodule"
  Solution: Delete node_modules folder, update .gitignore, then run `npm install`
  Prevention: Properly configure .gitignore before first commit

### Python and Virtual Environment Issues
- Error: "No module named 'openai'"
  Solution: Activate venv and run `pip install -r requirements.txt`
  Prevention: Always activate virtual environment before running backend

- Error: "ModuleNotFoundError: No module named 'flask_cors'"
  Solution: Run `pip install flask-cors python-multipart`
  Prevention: Keep requirements.txt updated

### Git Repository Issues
- Error: Ellipses (...) appearing in GitHub folder structure
  Solution: Create fresh repository, proper .gitignore, clean commit history
  Prevention: Set up .gitignore before initial commit

- Error: "remote rejected (push declined due to repository rule violations)"
  Solution: Remove sensitive information from git history, create new repository
  Prevention: Never commit API keys or sensitive data

### API and Backend Issues
- Error: "OpenAIError: The api_key client option must be set"
  Solution: Create .env file with valid OpenAI API key
  Prevention: Always set up environment variables before running

- Error: CORS policy blocking requests
  Solution: Properly configure CORS in FastAPI
  Prevention: Include CORS middleware in backend setup

### Frontend Issues
- Error: Dark mode not applying to all components
  Solution: Update Tailwind classes for all components
  Prevention: Use consistent theme structure

- Error: Summary history not updating
  Solution: Verify state management in React components
  Prevention: Implement proper state updates

## General Best Practices
1. Always use virtual environment for Python
2. Keep separate .gitignore for frontend and backend
3. Never commit sensitive data or API keys
4. Use environment variables for configuration
5. Test CORS settings locally before deployment

## Quick Fixes for Common Scenarios

Reset Project State:
rm -rf node_modules
rm -rf venv
npm install
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Clean Git Repository:
git rm -r --cached .
git add .
git commit -m "Clean repository"

Fix CORS Issues:
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Fix Dark Mode:
<div className={`${darkMode ? 'dark bg-gray-800' : 'bg-gray-50'}`}>

## Language Support Issues
- Problem: French text translating to English in detailed summaries
  Solution: Add explicit language preservation in prompts
  Prevention: Include language preservation in API calls

## File Processing Issues
- PDF Files: Ensure PyPDF2 is properly installed
- DOCX Files: Verify python-docx installation
- Web Pages: Check BeautifulSoup4 setup

## Environment Setup Guide
1. Clone repository
2. Create .env file with API keys
3. Install frontend dependencies
4. Set up Python virtual environment
5. Install backend dependencies
6. Start servers (backend: 5001, frontend: 3000)

## Environment Setup Issues
- Error: "Invalid API key"
  Solution: Double-check OPENAI_API_KEY format and validity
- Error: "API key not found"
  Solution: Ensure .env file is in correct location and properly formatted

## Integration Issues
- Error: "Frontend can't connect to backend"
  Solution: Verify ports (3000 and 5001) are correct and available
- Error: "File upload timeout"
  Solution: Check file size limits and connection stability

## Contact and Support
For additional issues or support:
- Create GitHub issue
- Check documentation
- Review code comments

Remember to always check logs for detailed error messages and ensure all dependencies are properly installed before running the application.