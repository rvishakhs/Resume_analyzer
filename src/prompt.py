def prepare_prompt(resume_txt, jd_txt):
    """Prepare the input prompt with imporved structure and validation"""
    if not resume_txt or not jd_txt:
        raise ValueError("Resume and JD text cannot be empty")
    
    prompt_template = " "