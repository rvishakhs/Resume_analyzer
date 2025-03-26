import PyPDF2 as pdf
import json
import os
from transformers import pipeline

def read_file(file):
    """
    Read the file and return the text
    """
    try: 
        if file.name.endswith(".pdf"):
            pdf_reader = pdf.PdfReader(file)
            if len(pdf_reader.pages) == 0:
                raise Exception("No pages found in the pdf file")
            
            text = " "
            for page in pdf_reader.pages:
                text += page.extract_text()

            if not text:
                raise Exception("No text found in the pdf file")
            
            return " ".join(text)
        else: 
            raise Exception("Invalid file format, This model only supports .pdf files")
    
    except Exception as e:
        raise Exception(f"Error reading the file: {str(e)}")
    

def get_llm_response(prompt):
    """
    This function generate a response using the LLM Model with enhanced error handling and response formatting
    """
    # Initialize the pipeline
    pipe = pipeline(
        "text-generation",
        model="google/gemma-2-9b",
        device="mps",  # replace with "mps" to run on a Mac device
    )

    # Generating the response from LLM 
    outputs = pipe(prompt, max_new_tokens=512,temperature=0.9)

    response = outputs[0]["generated_text"]

    # Error handling if the LLM response is empty
    if not response or not response.text():
        raise Exception("No response found from the model")
    
    # Try to parse the response as JSON
    try:
        response_json = json.loads(response)

        # Validate the response to check the strcuture
        required_fields = ['JD_Match','Skills_Match','Top Skills', 'Missing Keywords', 'Profile Summary', 'Recommendations']

        for field in required_fields:
            if field not in response_json:
                raise Exception(f"Missing field in the response: {field}")
            
        return response_json
    except Exception as e:
        raise Exception(f"Error while parsing the response to json: {str(e)}")


