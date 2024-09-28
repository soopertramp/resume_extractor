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

**Text Extraction**: Extract raw text from resumes using pdfplumber (PDF) and docx (DOCX).

**Information Extraction**: Use Spacy for NLP-based extraction (names, locations), and regex for phone numbers and emails. CSV files are loaded to match skills and job roles.

**Database Storage**: Store the parsed information in PostgreSQL, ensuring no duplicate entries exist based on email.

**Results**: The system streamlines the resume parsing process, automating tasks that were traditionally done manually. It provides structured data that can be further used for recruitment purposes or analysis. The extracted data includes names, qualifications, experience, skills, and contact information, ensuring that all critical aspects of a candidate's resume are covered.

### Growth/Next Steps:

1. File Format Expansion: Expand support to include additional file formats such as .txt or .rtf.

2. Enhanced NLP Models: Integrate more sophisticated NLP models or custom-trained models for improved information extraction accuracy (e.g., handling diverse resume formats).

3. Data Validation & Error Handling: Implement more advanced error handling and validation rules to ensure clean data, especially for experience or qualification mismatches.

4. Front-end Integration: Add a front-end application for users to upload resumes and visualize extracted data in real-time.

5. Resume Matching: Implement a matching feature to connect resumes with job descriptions based on extracted skills and qualifications.