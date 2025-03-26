import PyPDF2 as pdf
import json
import os

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