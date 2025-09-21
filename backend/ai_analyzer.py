import google.generativeai as genai
import os
import re
from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# Initialize Gemini
load_dotenv()

try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    print("✅ Gemini initialized successfully")
except Exception as e:
    print(f"❌ Gemini init error: {e}")
    model = None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=60))
def analyze_resume(resume_text, job_desc_text):
    if not model:
        return {
            'score': 0.0,
            'suggestions': "⚠️ Service unavailable. Please check:\n"
                          "1. Valid API key in .env\n"
                          "2. Enabled billing at cloud.google.com\n"
                          "3. Internet connection"
        }
    
    try:
        # Extract first 5 words as job title/type
        job_context = ' '.join(job_desc_text.split()[:5]) or "this position"
        
        prompt = f"""**Job-Specific Resume Analysis**
        
        Analyzing for: {job_context}
        
        **Job Requirements:**
        {job_desc_text[:2000]}
        
        **Candidate Resume:**
        {resume_text[:4000]}
        
        Provide concise analysis with:
        1. MATCH_SCORE: 0-100 (how well qualifications match)
        2. KEY_STRENGTHS: 3 bullet points
        3. CRITICAL_GAPS: Missing requirements
        4. ACTIONABLE_SUGGESTIONS: 2-3 improvements
        
        Format with clear section headers."""
        
        response = model.generate_content(prompt)
        return parse_response(response.text)
        
    except Exception as e:
        return {
            'score': 0.0,
            'suggestions': f"⚠️ Analysis error: {str(e)[:200]}"
        }

def parse_response(text):
    """Extract structured data from response"""
    try:
        # Extract score (supports multiple formats)
        score_match = re.search(r'(MATCH_SCORE|Score):?\s*(\d+)', text, re.IGNORECASE)
        score = float(score_match.group(2)) if score_match else 50.0
        
        # Clean formatting
        suggestions = (
            text.replace("•", "•")
            .replace("KEY_STRENGTHS", "## Key Strengths")
            .replace("CRITICAL_GAPS", "## Critical Gaps")
            .replace("ACTIONABLE_SUGGESTIONS", "## Suggested Improvements")
        )
        
        return {
            'score': min(100, max(0, score)),
            'suggestions': suggestions
        }
    except Exception:
        return {
            'score': 50.0,
            'suggestions': text  # Fallback to raw response
        }