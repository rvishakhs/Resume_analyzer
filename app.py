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


