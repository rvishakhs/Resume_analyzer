def prepare_prompt(resume_txt, jd_txt):
    """Prepare the input prompt with imporved structure and validation"""
    if not resume_txt or not jd_txt:
        raise ValueError("Resume and JD text cannot be empty")
    
    prompt_template = """
    Act as an expert ATS (Applicant Tracking System) and match the resume with the job description, specialist with deep expertise in:
    - Technical fields
    - Sofetware engineering 
    - Data science
    - Machine learning
    - Data analysis
    - web development
    - full stack development

    Evaluate the following resume against the job description. COnsider that the job market is 
    highly competitive and the resume should be tailored to the job description. 

    Resume:
    {resume_txt}

    Job Description:
    {jd_txt}
    """