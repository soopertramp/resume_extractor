import re
import spacy
from spacy.matcher import Matcher
import pandas as pd 
import nltk
from nltk.corpus import stopwords
from collections import Counter

nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")

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

def extract_phone_numbers(text):
    phone_numbers = re.findall(r'\b\d{10}\b', text)
    return phone_numbers

def extract_email(text):
    email = re.findall(r'\S+@\S+', text)
    return email[0] if email else ''

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

def extract_location(text):
    # Process the text through the NLP pipeline
    doc = nlp(text)
    
    # Extract locations (GPE)
    locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
    
    return locations[0] if locations else ''