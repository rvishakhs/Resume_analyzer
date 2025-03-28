import streamlit as st
import os
import json
from streamlit_extras.add_vertical_space import add_vertical_space
from transformers import pipeline
#from dotenv import load_dotenv
from src.helper import read_file, get_llm_response
from src.prompt import prepare_prompt

def init_session_state():
    """"
    Initialize the session state in stream lit for state management
    """
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def main():
    # Initialize the session state
    init_session_state()

    # Sidebar 
    with st.sidebar:
        st.title("Resume Decoder")
        st.subheader("About")
        st.write("""
                 Upload your resume and job description to get a detailed analysis of the match

                 - Evaluate your resume against the job description
                 - Profile Summary
                 - Identifying your strong skills 
                 - Finding Missing keywords
                 - Recommendations to improve your resume
                 """)

    # Set the title of the app
    st.title("Resume Decoder - Smart ATS Resume Analyzer")
    st.subheader( "Optimize Your Resume for ATS and job matching")


    # Input sections with validation
    jd = st.text_area("Job Description", 
                      height=200,
                      placeholder="Paste the job description here",
                      help="Enter the complete job description here for accurate results"
                    )
    uploaded_resume = st.file_uploader(
        "Upload your resume",
        type=["pdf"],
        help="Upload your resume in PDF format")
    
    # Process buttom with upload state
    if st.button("Analyse Resume", disabled=st.session_state.processing):
        if not jd:
            st.warning("Please enter the job description")
            return
        
        if not uploaded_resume:
            st.warning("Please upload the resume")
            return
        
        # Set the processing state to True
        st.session_state.processing = True 

        try:
            with st.spinner("Analysing your resume..."):

                # Extract text from pdf 
                resume_text = read_file(uploaded_resume)

                # Prepare the prompt 
                prompt = prepare_prompt(resume_text, jd)

                # Get the response from the LLM model 
                response = get_llm_response(prompt)
                response_json = json.loads(response)

                # Display the response
                st.success("Resume analysis completed")
                left, right = st.columns(2, border=True)
                # Match Percentage 
                match_percantage = response_json.get("JD_Match", "N/A")
                left.metric("Match Percentage", match_percantage)

                # Skills Match
                skills_percentage = response_json.get("Skills_Match", "N/A")
                right.metric("Match Percentage", match_percantage)

                # Top Skills 
                st.subheader("Top Skills Match")
                top_skills = response_json.get("Top Skills", [])

                if top_skills:
                    st.write(",".join(top_skills))
                else:
                    st.write("No top skills found")

                # Missing Keywords    
                st.subheader("Missing Keywords")
                missing_keywords = response_json.get("Missing Keywords", [])

                if top_skills:
                    st.write(",".join(top_skills))
                else:
                    st.write("No top skills found")

                # Profile Summary 
                st.subheader("Profile Summary")
                st.write(response_json.get("Profile Summary", "N/A"))

                # Recommendations
                st.subheader("Recommendations")
                st.write(response_json.get("Recommendations", "N/A"))
        
        except Exception as e:
            st.error(f"An error occured while Resume generation: {str(e)}")

        finally:
            st.session_state.processing = False 

if __name__ == "__main__":
    main()