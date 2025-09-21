# frontend/app.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # Fix path to reach backend

from backend.resume_parser import extract_text_from_pdf, extract_text_from_image
from backend.ai_analyzer import analyze_resume
import streamlit as st

def main():
    st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
    
    # Sidebar
    with st.sidebar:
        st.header("Upload Resume")
        uploaded_file = st.file_uploader("Choose file", type=["pdf", "jpg", "png"])
        st.header("Job Description")
        job_desc = st.text_area("Paste job description", height=200)

    # Main content
    st.title("AI Resume Analyzer")
    st.divider()

    if uploaded_file and job_desc:
        try:
            # Text extraction
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = extract_text_from_image(uploaded_file)
            
            if not text.strip():
                st.error("Failed to extract text from file")
                return
                
            st.success("File processed successfully!")
            
            with st.expander("Extracted Text Preview"):
                st.text(text[:500] + "...")

            # Analysis
            with st.spinner("Analyzing..."):
                result = analyze_resume(text, job_desc)
                
                if not isinstance(result, dict) or 'score' not in result:
                    st.error("Analysis failed. Please try again.")
                    return
                
                st.progress(result['score']/100)
                st.metric("Match Score", f"{result['score']}%")
                st.subheader("Suggestions")
                st.markdown(result.get('suggestions', "No suggestions available"))

        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.progress(0)
    else:
        st.info("Please upload a resume and job description")

if __name__ == "__main__":
    main()