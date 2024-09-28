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