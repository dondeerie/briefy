# Briefy Backend

FastAPI backend for Briefy text summarization app.

## Setup
1. Create virtual environment:
python -m venv venv
source venv/bin/activate

2. Install dependencies:
pip install -r requirements.txt

3. Create .env with:
OPENAI_API_KEY=your_key_here

4. Run server:
python main.py

## API Endpoints
- POST /api/summarize
- POST /api/summarize/file

## Structure
- app/
  - services/: Core summarization logic
  - utils/: Helper functions
- main.py: Server configuration