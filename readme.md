# Resume Information Extractor

## Table of contents

1. Project Overview
    - Context
    - Actions
    - Results
    - Growth/Next Steps
2. Data Overview
3. Growth & Next Steps

## Project Overview

### Context : 

This project automates resume processing by extracting key information such as names, phone numbers, emails, qualifications, and skills from PDF and DOCX files. 

NLP and regular expressions are used to process text, while the extracted data is saved in a PostgreSQL database for easy access and retrieval. 

The system ensures data validation and checks for duplicates before insertion.

### Actions:

- **Text Extraction**: Extract raw text from resumes using pdfplumber (PDF) and docx (DOCX).

- **Information Extraction**: Use Spacy for NLP-based extraction (names, locations), and regex for phone numbers and emails. CSV files are loaded to match skills and job roles.

- **Database Storage**: Store the parsed information in PostgreSQL, ensuring no duplicate entries exist based on email.

- **Results**: The system streamlines the resume parsing process, automating tasks that were traditionally done manually. It provides structured data that can be further used for recruitment purposes or analysis. The extracted data includes names, qualifications, experience, skills, and contact information, ensuring that all critical aspects of a candidate's resume are covered.

### Growth/Next Steps:

1. File Format Expansion: Expand support to include additional file formats such as .txt or .rtf.

2. Enhanced NLP Models: Integrate more sophisticated NLP models or custom-trained models for improved information extraction accuracy (e.g., handling diverse resume formats).

3. Data Validation & Error Handling: Implement more advanced error handling and validation rules to ensure clean data, especially for experience or qualification mismatches.

4. Front-end Integration: Add a front-end application for users to upload resumes and visualize extracted data in real-time.

5. Resume Matching: Implement a matching feature to connect resumes with job descriptions based on extracted skills and qualifications.

## Data Overview & Preparation
The project relies on resume documents (PDF and DOCX) as input and pre-defined structured data (CSV files) for reference.

**Resume Data**:

The resumes are sourced in PDF and DOCX formats, uploaded by users via the Flask API. The system extracts unstructured text from these files using libraries like pdfplumber for PDFs and docx for Word documents. The extracted raw text forms the basis for the information extraction pipeline.

```python
import pdfplumber 
from docx import Document

def extract_text_from_file(file_path):
    if file_path.lower().endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.lower().endswith('.docx'):
        return extract_text_from_word(file_path)
    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are supported.")

def extract_text_from_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + '\n'
    return text.strip()

def extract_text_from_word(docx_path):
    doc = Document(docx_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text.strip()
```

```extract_text_from_file(file_path)``` : This function determines the file type based on the file extension (either PDF or DOCX). It then calls the appropriate function (extract_text_from_pdf or extract_text_from_word) to extract text from the file. If the file is not of type PDF or DOCX, it raises an error.

```extract_text_from_pdf(pdf_path)``` : This function uses the pdfplumber library to open and read the content of a PDF file. It loops through each page of the PDF, extracts the text, and concatenates it into a single string.

```extract_text_from_word(docx_path)```: This function uses the python-docx library to open a DOCX file and extract the text from each paragraph in the document, concatenating it into a single string.

Then comes information extraction from the extracted text.

**Skills and Job Roles Data**:

The project uses pre-defined CSV files for matching skills and job roles:

-   Skills: A CSV file (skills.csv) contains a comprehensive list of skills categorized by industry or domain. This is used to match and extract skills from the resume text.

-   Job Roles: Another CSV file (job_role.csv) contains job role titles, also categorized, which are compared against the resume text.

Example:

```python

def extract_skillset(text):
    '''
    Helper function to extract skills from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param skills_file: path to CSV file containing skills
    :return: list of skills extracted
    '''
    # Load skills from the provided CSV file
    data = pd.read_csv("data/skills.csv")
    skills = list(data.columns.values)
    
    skillset = [skill for skill in skills if skill.lower() in text.lower()]
    
    return skillset
```

```python
def extract_job_role(text):

    '''
    Helper function to extract job roles from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :param skills_file: path to CSV file containing job_roles
    :return: list of job_roles extracted
    '''

    # Load job_role from the provided CSV file
    data = pd.read_csv("data/job_role.csv")
    job_role = list(data.columns.values)

    job_role = [job for job in job_role if job.lower() in text.lower()]
    
    return job_role[0] if job_role else ''
```

**Qualification and Experience Data**:
-   The system looks for standard education degrees (e.g., B.Tech, M.Sc) in the resume text by referencing a list of common qualifications embedded in the code.

-   Years of Experience: Experience is identified using regular expressions, typically in the format "X years of experience." If available, experience is parsed and converted into a structured format.

Example:

```python

def extract_qualification(text):
    '''
    Helper function to extract education from spacy nlp text

    :param nlp_text: object of `spacy.tokens.doc.Doc`
    :return: tuple of education degree and year if year is found
             else only returns education degree
    '''

    # Define the necessary variables within the function
    EDUCATION = ['B.Tech', 'M.Tech', 'B.Sc', 'M.Sc', 'PhD', 'MBA', 'B.E', 'B.Com', 'B.A', 'BBA', 'BCA',
        'M.E', 'M.Com', 'M.A', 'MBA', 'MCA', 'M.Phil', 'MBBS', 'BDS', 'B.Pharm', 'M.Pharm', 
        'B.Ed', 'M.Ed', 'B.Arch', 'M.Arch', 'LLB', 'LLM', 'MD', 'MS', 'DNB', 'CA', 'CS', 
        'ICWA', 'Diploma', 'Certificate Course']
    STOPWORDS = set(stopwords.words('english'))
    YEAR = r'\b(19|20)\d{2}\b'  # pattern for matching year

    edu = {}
    text = nlp(text)
    # Extract education degree
    try:
        for index, token in enumerate(text):
            for tex in token.text.split():
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex.upper() not in STOPWORDS:
                    edu[tex] = token.text + (text[index + 1].text if index + 1 < len(text) else '')
    except IndexError:
        pass

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(YEAR), edu[key])
        if year:
            education.append((key, ''.join(year.group(0))))
        else:
            education.append(key)
    return education

def extract_experience(text):
    experience = re.findall(r'\b\d+ years\b', text)
    return experience[0] if experience else ''
```

**Spacy NLP Pipeline**:

Spacy’s Named Entity Recognition (NER) is employed to identify proper nouns, like names, and geographic entities (locations) from the resume text.

- Name Extraction: Using NER models, the project extracts the first and last names from resumes.

- Location Extraction: Geographic entities are identified and extracted to determine where the candidate has lived or worked.

Example:

```python

# Define the name pattern
NAME_PATTERN = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

def extract_names(text):
    '''
    Helper function to extract first and last names from text

    :param text: string of text
    :return: tuple of (first_name, last_name)
    '''
    # Process text with spacy
    nlp_text = nlp(text)
    
    # Initialize the matcher with the shared vocabulary
    matcher = Matcher(nlp.vocab)
    
    # Add the pattern to the matcher
    matcher.add('NAME', [NAME_PATTERN])

    matches = matcher(nlp_text)

    for _, start, end in matches:
        span = nlp_text[start:end]
        if 'name' not in span.text.lower():
            names = span.text.split()
            if len(names) >= 2:
                first_name, last_name = names[0], names[-1]
                return first_name, last_name
    return '', ''

```
**Handling Multiple Data Types**:

The system supports both structured (CSV files) and unstructured (text from resumes) data types. CSV files are used for matching skills and job roles, while the unstructured text is processed using regex and NLP.

**Summary of Data Preparation**:

The project efficiently handles text extraction, qualification matching, skills/job role matching, and ensures data is structured before storage. Using CSV files for reference, regex for patterns, and Spacy for NLP tasks, the system can handle various types of resume data and ensure accurate extraction for further analysis or recruitment purposes.