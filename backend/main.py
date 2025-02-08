from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2
import docx
import requests
from fastapi import Query
from bs4 import BeautifulSoup
from io import BytesIO
from typing import Optional

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:3000"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

def validate_text_length(text):
    words = len(text.split())
    if words < 50:
        return {
            "is_valid": False,
            "message": """
            The provided text is too short for meaningful summarization.
            For better results:
            • Provide at least 50 words
            • Include complete sentences
            • Ensure content has clear points or arguments
            """
        }
    return {"is_valid": True}

def assess_content_quality(text):
    sentences = text.split('.')
    if len(sentences) < 3:
        return {
            "is_valid": False,
            "message": """
            Unable to generate a meaningful summary.
            The provided content lacks sufficient detail or structure.
            Please provide text with:
            • More detailed information
            • Multiple connected points
            • Clear context or arguments
            """
        }
    
    meaningful_words = len(set(text.lower().split()))
    if meaningful_words < 20:
        return {
            "is_valid": False,
            "message": """
            Cannot create a comprehensive summary.
            The text appears to be too limited in content.
            For better results, provide material with:
            • Richer content
            • More detailed discussion
            • Clear main points
            """
        }
    
    return {"is_valid": True}

def extract_pdf_text(file_bytes):
   pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
   return " ".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

def extract_docx_text(file_bytes):
   doc = docx.Document(BytesIO(file_bytes))
   return " ".join(para.text for para in doc.paragraphs)

def extract_webpage_text(url):
   try:
       response = requests.get(url, headers=headers, timeout=10)
       response.raise_for_status()
       soup = BeautifulSoup(response.text, 'html.parser')
       
       for element in soup(['script', 'style', 'nav', 'footer', 'ad', 'ads', 'header']):
           element.decompose()
       
       article = soup.find('article') or soup.find(class_='article-content') or soup.find('main')
       return article.get_text(separator=' ', strip=True) if article else soup.get_text(separator=' ', strip=True)
   except Exception as e:
       return f"Error accessing the webpage: {str(e)}"

def generate_summary(text, summary_type):
    print(f"Generating {summary_type} summary...")
    
    # Validate text
    length_check = validate_text_length(text)
    if not length_check["is_valid"]:
        return length_check["message"]
        
    content_check = assess_content_quality(text)
    if not content_check["is_valid"]:
        return content_check["message"]
    
    try:
        if summary_type == "brief":
            return generate_key_points(text)
        else:
            quality_check = assess_content_quality(text)
            if not quality_check["is_valid"] and summary_type == "detailed":
                return "Text lacks sufficient detail for comprehensive analysis. Consider using brief summary instead."
            return generate_comprehensive_analysis(text)
    except Exception as e:
        return f"An error occurred during summarization: {str(e)}"

def generate_key_points(text, max_points=3):
    prompt = f"""Create a concise summary with {max_points} key points:
    1. Each point should be 1-2 sentences
    2. Include one supporting detail or context for each point
    3. Keep points in order of importance
    4. Each point should still be focused and clear
    5. Keep ALL summaries in their original language.
    6. If text is in French, summarize in French.
    7. If text is in Spanish, summarize in Spanish.
    
    FORMAT REQUIREMENTS:
    • Use numbered points (1., 2., 3.)
    • Add a blank line between each point
    • Bold the main point, followed by supporting context
    • Example:
    
    1. **[Main point]**
       [Supporting context]

    2. **[Main point]**
       [Supporting context]

    3. **[Main point]**
       [Supporting context]
    
    Text: {text}"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a precise summarizer who creates clear, contextualized points."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def generate_comprehensive_analysis(text):
   prompt = f"""⚠️ CRITICAL INSTRUCTION - DO NOT IGNORE:
    1. This text is in its original language
    2. You MUST generate the DETAILED summary in the SAME language
    3. NEVER translate to English if original text is not English
    4. Pour le texte français: GARDEZ LE FRANÇAIS! NE TRADUISEZ PAS!
    
    Create a detailed analysis following this structure, while maintaining the original language:
    
    MAIN FINDINGS (use original language)
    • List 3 major findings
    • Include specific details
    • Focus on primary outcomes

    SUPPORTING EVIDENCE (use original language)
    • Provide specific numbers and data
    • Include relevant statistics
    • Reference key examples

    IMPLICATIONS(use original language)
    • Explain broader impact
    • Discuss consequences
    • Address future implications

    RECOMMENDATIONS (use original language)
    • Provide clear action items
    • Suggest next steps
    • Highlight priorities

    FORMAT REQUIREMENTS:
    • Use section headers in ALL CAPS with arrow (→)
    • Use arrow (→) after MAIN FINDINGS, SUPPORTING EVIDENCE, IMPLICATIONS and RECOMMENDATIONS
    • Use bullet points (•) for each item
    • Add blank line between sections
    • Bold key terms or statistics
    • Example:

    MAIN FINDINGS
    →→
    • Finding 1
    • Finding 2

   Text: {text}"""

   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[
           {"role": "system", "content": "You are an analytical expert who creates structured reports with clear sections."},
           {"role": "user", "content": prompt}
       ],
       temperature=0.1
   )
   return response.choices[0].message.content

@app.post("/api/summarize")
async def summarize(request: dict):
    try:
        text = request.get('text', '')
        url = request.get('url', '')
        summary_type = request.get('type', 'brief')
        
        text_to_summarize = text if text else (extract_webpage_text(url) if url else "")
        
        if not text_to_summarize:
            return {"summary": "No text provided for summarization."}
            
        # Validate text length
        length_check = validate_text_length(text_to_summarize)
        if not length_check["is_valid"]:
            return {"summary": length_check["message"]}
            
        return {"summary": generate_summary(text_to_summarize, summary_type)}
    except Exception as e:
        return {"summary": f"Error processing request: {str(e)}"}

@app.post("/api/summarize/file")
async def summarize_file(file: UploadFile = File(...), type: str = Query(default='brief')):
    try:
        file_content = await file.read()
        text = ""
        
        if file.filename.endswith('.pdf'):
            text = extract_pdf_text(file_content)
        elif file.filename.endswith('.docx'):
            text = extract_docx_text(file_content)
        else:
            return {"summary": "Unsupported file format. Please upload PDF or DOCX files only."}
            
        if not text:
            return {"summary": "Could not extract text from file. Please check if the file is valid and not empty."}
            
        # Validate text length
        length_check = validate_text_length(text)
        if not length_check["is_valid"]:
            return {"summary": length_check["message"]}
            
        return {"summary": generate_summary(text, type)}
    except Exception as e:
        return {"summary": f"Error processing file: {str(e)}"}

if __name__ == "__main__":
   import uvicorn
   uvicorn.run(app, host="0.0.0.0", port=5001)