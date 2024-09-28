from flask import Flask, request, jsonify
import os
import json
import psycopg2
from dotenv import load_dotenv
import uuid
from src.text_extractor import extract_text_from_pdf, extract_text_from_word
from src.info_extractor import (
    extract_names, extract_phone_numbers, extract_email,
    extract_qualification, extract_experience, extract_skillset,
    extract_job_role, extract_location
)

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def extract_resume_info(file_path):

    file_extension = os.path.splitext(file_path)[1].lower()
    text = None

    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif file_extension == '.doc' or file_extension == '.docx':
        text = extract_text_from_word(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    if text is None:
        raise ValueError("Failed to extract text from the file.")
    
    first_name, last_name = extract_names(text)
    phone_numbers = extract_phone_numbers(text)
    email = extract_email(text)
    qualification = extract_qualification(text)
    experience = extract_experience(text)
    skillset = extract_skillset(text)
    job_role = extract_job_role(text)
    location = extract_location(text)

    # Capitalize first and last names
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    
    # Format the skillset as a semicolon-separated string with quotes
    skillset_formatted = ';'.join(f'{skill}' for skill in skillset)

    resume_info = {
        'First Name': first_name,
        'Last Name': last_name,
        'Phone Numbers': phone_numbers,
        'Email': email,
        'Qualification': qualification,
        'Experience': experience,
        'Skillset': skillset_formatted,
        'Job Role': job_role,
        'Location': location
    }

    # Convert resume_info to a JSON string without extra escaping
    resume_info_json = json.dumps(resume_info, indent=4)

    return resume_info_json

def save_to_postgresql(data, tenant_id):
    candidate_id = str(uuid.uuid4())
    try:
        # Connect to your postgres DB using environment variables
        conn = psycopg2.connect(
            dbname=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD"),
            host=os.getenv("DATABASE_HOST"),
            port=os.getenv("DATABASE_PORT")
        )
        # Create a cursor object
        cursor = conn.cursor()

        # Check if email already exists in the candidate table
        email = data.get('Email')
        check_candidate_query = "SELECT candidate_id FROM candidate WHERE email_id = %s"
        cursor.execute(check_candidate_query, (email,))
        if cursor.fetchone():
            raise ValueError("A record with this email already exists in the candidate table")

        # Check if email exists in the company table
        check_company_query = "SELECT company_email_id FROM company WHERE company_email_id = %s"
        cursor.execute(check_company_query, (email,))
        if cursor.fetchone():
            raise ValueError("A record with this email already exists in the company table")

        # Check if email exists in the users table
        check_users_query = "SELECT email_id FROM users WHERE email_id = %s"
        cursor.execute(check_users_query, (email,))
        if cursor.fetchone():
            raise ValueError("A record with this email already exists in the users table")

        # Convert Experience to float, handle empty string
        experience = 0.0
        if 'Experience' in data:
            if data['Experience'] == "":
                experience = 0.0
            else:
                try:
                    experience = float(data['Experience'])
                except ValueError:
                    print("Experience is not a valid float")

        # Convert Phone Numbers to string, handle list or dict
        phone_numbers = data.get('Phone Numbers', '')
        if isinstance(phone_numbers, list):
            phone_numbers = ', '.join(phone_numbers)  # Join list items into a single string
        elif isinstance(phone_numbers, dict):
            phone_numbers = str(phone_numbers)  # Convert dict to string representation

        # Insert data into the table
        insert_query = """
        INSERT INTO candidate (candidate_id, name, phone_number, email_id, relevant_experience, skill_set, current_job_role, current_work_location, account_active, deleted, tenant_id, terms_and_policy_accepted)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true, false, %s, true)
        """
        cursor.execute(insert_query, (
            candidate_id,
            data.get('First Name') +" "+ data.get('Last Name'),
            phone_numbers,
            email,
            experience,
            data.get('Skillset'),
            data.get('Job Role'),
            data.get('Location'),
            tenant_id
        ))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()
    except ValueError as ve:
        print(f"ValueError: {ve}")
        candidate_id = None
    except Exception as e:
        print(f"An error occurred: {e}")
        candidate_id = None
    return candidate_id

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    # Get the tenant_id from request parameters
    tenant_id = request.args.get('tenant_id', 'default_tenant_id')

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        resume_info_json = extract_resume_info(filepath)
        resume_info_dict = json.loads(resume_info_json)
        candidate_id = save_to_postgresql(resume_info_dict, tenant_id)
        if candidate_id:
            return jsonify({'message': 'Resume successfully processed', 'candidate_id': candidate_id})
        else:
            return jsonify({'error': 'A record with this email already exists'}), 500

if __name__ == "__main__":
    app.run(debug=True)