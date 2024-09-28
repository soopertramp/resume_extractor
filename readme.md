# Resume Information Extractor

## Table of contents

1. [Project Overview](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#project-overview)
    - [Context](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#context-)
    - [Actions](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#actions)
    - [Results](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#results)
    - [Growth/Next Steps](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#growthnext-steps)
2. [Data Overview & Preparation](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#data-overview--preparation)
    - [Resume Data](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#resume-data)
    - [Skills and Job Roles Data](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#skills-and-job-roles-data)
    - [Qualification and Experience Data](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#qualification-and-experience-data)
    - [Spacy NLP Pipeline](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#spacy-nlp-pipeline)
    - [Handling Multiple Data Types](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#handling-multiple-data-types)
    - [Summary of Data Preparation](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#summary-of-data-preparation)
3. [Database Integration](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#database-integration)
    - [Environment Configuration](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#environment-configuration)
    - [Data Insertion Workflow](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#data-insertion-workflow)
    - [Schema Overview](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#schema-overview)
    - [Database Interaction](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#database-interaction)
4. [How It Works: Overall Process](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#how-it-works-overall-process)
    - [File Upload](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#file-upload-users-upload-resumes-in-pdf-or-docx-format-via-a-flask-api)
    - [Text Extraction](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#text-extraction-the-system-extracts-the-raw-text-from-the-uploaded-resume-using)
    - [Information Extraction](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#information-extraction)
    - [Data Structuring](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#data-structuring)
    - [Duplicate Checking](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#duplicate-checking)
    - [Database Insertion](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#database-insertion)
    - [Response](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#response)
    - [Error Handling](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#error-handling)
5. [Technologies Used](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#technologies-used)
6. [Folder Structure](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#folder-structure)
7. [Future Improvements](https://github.com/soopertramp/resume_extractor?tab=readme-ov-file#future-improvements)

## Project Overview

### Context : 

This project automates resume processing by extracting key information such as names, phone numbers, emails, qualifications, and skills from PDF and DOCX files. 

NLP and regular expressions are used to process text, while the extracted data is saved in a PostgreSQL database for easy access and retrieval. 

The system ensures data validation and checks for duplicates before insertion.

### Actions:

- **Text Extraction**: Extract raw text from resumes using pdfplumber (PDF) and docx (DOCX).

- **Information Extraction**: Use Spacy for NLP-based extraction (names, locations), and regex for phone numbers and emails. CSV files are loaded to match skills and job roles.

- **Database Storage**: Store the parsed information in PostgreSQL, ensuring no duplicate entries exist based on email.

### Results: 
The system streamlines the resume parsing process, automating tasks that were traditionally done manually. It provides structured data that can be further used for recruitment purposes or analysis. The extracted data includes names, qualifications, experience, skills, and contact information, ensuring that all critical aspects of a candidate's resume are covered.

### Growth/Next Steps:

1. File Format Expansion: Expand support to include additional file formats such as .txt or .rtf.

2. Enhanced NLP Models: Integrate more sophisticated NLP models or custom-trained models for improved information extraction accuracy (e.g., handling diverse resume formats).

3. Data Validation & Error Handling: Implement more advanced error handling and validation rules to ensure clean data, especially for experience or qualification mismatches.

4. Front-end Integration: Add a front-end application for users to upload resumes and visualize extracted data in real-time.

5. Resume Matching: Implement a matching feature to connect resumes with job descriptions based on extracted skills and qualifications.

## Data Overview & Preparation
The project relies on resume documents (PDF and DOCX) as input and pre-defined structured data (CSV files) for reference.

### Resume Data:

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

**Then comes information extraction from the extracted text.**

### Skills and Job Roles Data:

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
```extract_skillset(text)```:

- This function extracts skills from the provided text.
- It loads a list of skills from a CSV file (skills.csv) and compares each skill against the text (case-insensitive).
- If a skill from the CSV file is found in the text, it is added to the skillset list, which is then returned.

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

```extract_job_role(text)```:

- This function extracts job roles from the provided text.
- It loads a list of job roles from another CSV file (job_role.csv) and checks if any of the job roles appear in the text (also case-insensitive).
- If a matching job role is found, it returns the first one; if no match is found, it returns an empty string.

### Qualification and Experience Data:
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
```
```extract_qualification(text):```

- This function extracts educational qualifications and possible graduation years from the given text.
- EDUCATION: A predefined list of common educational degrees is checked against the text to identify qualifications.
- YEAR: A regular expression (\b(19|20)\d{2}\b) is used to match a year pattern (from 1900 to 2099).
- The text is tokenized using SpaCy's NLP model, and the function looks for matches with qualifications and extracts nearby words or tokens to determine whether a year is mentioned.
- The result is a list of tuples containing the degree and the year (if available) or just the degree if no year is found.

```python
def extract_experience(text):
    experience = re.findall(r'\b\d+ years\b', text)
    return experience[0] if experience else ''
```

```extract_experience(text):```

- This function extracts the number of years of experience from the text.
- It uses a regular expression (\b\d+ years\b) to search for patterns like "5 years," indicating years of experience.
- If a match is found, the first match is returned; otherwise, an empty string is returned.

### Spacy NLP Pipeline:

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
```NAME_PATTERN```: This pattern defines a sequence of two proper nouns (PROPN), which generally correspond to a first and last name. The pattern helps identify name-like structures in the text.

```extract_names(text):```

- The function processes the input text using SpaCy to tokenize and identify parts of speech.
- It then initializes a Matcher object, which is used to find patterns (like names) in the text. The Matcher uses SpaCy’s vocabulary (nlp.vocab).
- The NAME_PATTERN is added to the matcher to search for two consecutive proper nouns, which is a common structure for names.
- The function searches for matches, and when it finds a match, it checks that the span of text does not include the word "name" (to avoid false positives).
- If a match is found, it splits the span into individual words, assuming the first and last words are the first and last names, respectively.
- If no valid name is found, it returns empty strings ('', '').

### Handling Multiple Data Types:

The system supports both structured (CSV files) and unstructured (text from resumes) data types. CSV files are used for matching skills and job roles, while the unstructured text is processed using regex and NLP.

### Summary of Data Preparation:

The project efficiently handles text extraction, qualification matching, skills/job role matching, and ensures data is structured before storage. Using CSV files for reference, regex for patterns, and Spacy for NLP tasks, the system can handle various types of resume data and ensure accurate extraction for further analysis or recruitment purposes.

## Database Integration
The database integration is a critical part of the project, enabling structured storage of the extracted resume information in PostgreSQL. Here’s how it is set up:

### Environment Configuration:
The database connection parameters (host, port, username, password, and database name) are securely stored in a .env file to ensure confidentiality and ease of access.

```python

load_dotenv()  # Load environment variables from .env file
conn = psycopg2.connect(
    dbname=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
```

This snippet illustrates how the database connection is established using environment variables, which are loaded via the dotenv library to ensure sensitive information is not hardcoded.

### Data Insertion Workflow:
After resume information is extracted and structured, it is inserted into the candidate table in the PostgreSQL database.

- Duplicate Checking: Before inserting, the system checks whether a record with the same email already exists in the candidate table or other related tables (e.g., users or company).

- Data Formatting: Special care is taken to format data like phone numbers and skills into database-friendly formats (e.g., converting a list of skills into a semicolon-separated string).

```python

def save_to_postgresql(data, tenant_id):
    candidate_id = str(uuid.uuid4())
    cursor = conn.cursor()

    # Check for duplicates in the candidate table
    email = data.get('Email')
    check_query = "SELECT candidate_id FROM candidate WHERE email_id = %s"
    cursor.execute(check_query, (email,))
    if cursor.fetchone():
        raise ValueError("A record with this email already exists.")

    # Insert new candidate data into the table
    insert_query = """
        INSERT INTO candidate (candidate_id, name, phone_number, email_id, relevant_experience, skill_set, current_job_role, current_work_location, account_active, tenant_id, terms_and_policy_accepted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true, %s, true)
    """
    cursor.execute(insert_query, (
        candidate_id,
        data.get('First Name') + " " + data.get('Last Name'),
        data.get('Phone Numbers'),
        data.get('Email'),
        data.get('Experience', 0.0),  # Defaults to 0.0 if not present
        data.get('Skillset'),
        data.get('Job Role'),
        data.get('Location'),
        tenant_id
    ))

    conn.commit()
    cursor.close()
    return candidate_id

```
This function ensures that the extracted resume information is formatted and inserted into the database while preventing duplicate records. The UUID is used to assign unique identifiers to each candidate.

### Schema Overview:
The schema for the candidate table includes fields such as:

- candidate_id: A unique identifier (UUID) for each candidate.
- name: Full name of the candidate (first and last name combined).
- phone_number: Contact information of the candidate.
- email_id: Unique email ID (used for duplicate checking).
- relevant_experience: Years of relevant experience extracted from the resume.
- skill_set: A semicolon-separated string of skills.
- current_job_role: Job role extracted from the resume.
- current_work_location: Geographic location extracted using NLP.
- account_active, terms_and_policy_accepted: Boolean flags for tracking active accounts and terms acceptance.

### Database Interaction:

- Duplicate Prevention: The system checks for the candidate’s email across multiple tables (candidate, users, company) to avoid inserting duplicate records. This ensures data integrity and prevents redundant data entries.

- Error Handling: The system implements error handling to manage situations like invalid inputs or failed connections.

```python

try:
    # Check and insert candidate data
except ValueError as ve:
    print(f"ValueError: {ve}")
except Exception as e:
    print(f"An error occurred: {e}")
```
In case a duplicate is found or another error occurs, the system returns an appropriate error message and aborts the insertion process.

## How It Works: Overall Process
### File Upload: 
Users upload resumes in PDF or DOCX format via a Flask API. The file is saved temporarily in a designated upload folder.

### Text Extraction: The system extracts the raw text from the uploaded resume using:

- pdfplumber for PDFs.
- docx for Word documents.

### Information Extraction:

- Names: Extracted using Spacy's Named Entity Recognition (NER).
- Phone Numbers & Emails: Identified using regex patterns.
- Skills & Job Roles: Matched from pre-defined CSV files.
- Experience & Qualifications: Extracted using predefined patterns and keyword matching.

### Data Structuring: 

The extracted information is structured into a JSON format that includes fields like name, phone number, email, qualifications, job role, experience, and skills.

### Duplicate Checking: 
Before inserting data into the PostgreSQL database, the system checks for duplicate email entries across several tables (candidate, users, company) to avoid redundant records.

### Database Insertion: 
Once validated, the structured data is inserted into the PostgreSQL database. A unique UUID is generated for each candidate, and fields are mapped to corresponding database columns.

### Response: 
The Flask API returns a success message along with the candidate_id if the insertion is successful, or an error message if issues such as duplicates are detected.

### Error Handling: 
The system gracefully handles errors (e.g., unsupported file types, duplicate records) by returning appropriate error responses.

## Technologies Used
- Python: The core programming language used for text extraction, data processing, and server-side API handling.
- pdfplumber: Used for extracting text from PDF files.
- docx: Used for extracting text from DOCX files.
- Spacy: Utilized for NLP tasks such as extracting names and locations through Named Entity Recognition (NER).
- Regex: Employed to identify and extract phone numbers and email addresses.
- Pandas: Used to process structured CSV data for skills and job role matching.
- Flask: A lightweight web framework used to build the API for uploading resumes and handling requests.
- PostgreSQL: The relational database used for storing and managing structured resume data. It supports efficient querying, ensures data integrity, and handles large volumes of candidate information.
- psycopg2: The Python library used to interface with the PostgreSQL database. It manages database connections, queries, and transactions.
- dotenv: Used to securely manage environment variables like database credentials, ensuring sensitive information is not hardcoded in the application.

## Folder Structure

The project follows a well-organized folder structure to ensure scalability and easy management of components:

```bash

/project_root
│
├── /data
│   ├── skills.csv          # CSV file containing a list of skills for matching.
│   ├── job_role.csv        # CSV file containing job roles for matching.
│
├── /src
│   ├── info_extractor.py   # Contains functions for extracting names, phone numbers, emails, skills, job roles, and qualifications using Spacy and regex.
│   ├── text_extractor.py   # Handles the extraction of text from resumes in PDF and DOCX formats using pdfplumber and docx.
│
├── /uploads                # Directory for temporarily storing uploaded resumes.
│
├── connector.py            # Flask API to handle file uploads and interact with PostgreSQL for data storage.
├── .env                    # Environment variables (e.g., database credentials).
├── requirements.txt        # List of dependencies for the project (Flask, Spacy, pdfplumber, etc.).
```

## Future Improvements:

- File Format Expansion: Support for more file types like .txt, .rtf, and even image-based resumes (via OCR technology) can be added.

- Advanced NLP Models: Implement more sophisticated or custom-trained models (e.g., BERT or GPT-based) for extracting information more accurately, handling varied resume formats, and better understanding context.

- Enhanced Front-end Interface: A front-end dashboard for users to upload resumes, view extracted data, and interact with the system in real time could improve user experience.

- Matching Algorithms: Implementing resume-to-job matching based on extracted skills and job roles would add significant value to the recruitment process.

- Machine Learning Integration: Integrate machine learning models to rank or recommend candidates based on extracted data and match it with job descriptions.

- Data Validation: Improve validation for extracted fields like experience, qualifications, and skills by cross-referencing with real-world databases or job boards.

- Security Enhancements: Strengthen data security by implementing encryption for sensitive data (e.g., contact information) during both storage and transmission.

- Scalability: Containerization with Docker and Kubernetes can be added for better scalability, allowing the system to handle larger datasets and multiple concurrent uploads seamlessly.

- Analytics & Reporting: Develop advanced reporting and analytics features to provide insights on trends, skills demand, and candidate qualifications, making the system useful for broader workforce analysis.

- Internationalization: Enhance the system to handle resumes in multiple languages using multilingual NLP models, making the platform globally accessible.