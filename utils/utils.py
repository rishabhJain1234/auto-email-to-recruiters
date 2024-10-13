import pdfplumber
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import streamlit as st
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

import os
from openai import OpenAI

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = ''
        for page in pdf.pages:
            text += page.extract_text()
    return text


def send_email(email_id, actual_email, subject):
            sender_email = st.secrets("EMAIL")
            sender_password = st.secrets("PASSWORD")

            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email_id
            msg['Subject'] = subject

            msg.attach(MIMEText(actual_email, 'plain'))
            
            with open(st.secrets("resume_path"), "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= resume.pdf",
                )
                msg.attach(part)

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = msg.as_string()
                server.sendmail(sender_email, email_id, text)
                server.quit()
                print('Email sent successfully!')
                st.success("Email sent successfully!")
            except Exception as e:
                print(f"Failed to send email: {e}")
                st.error(f"Failed to send email: {e}")
                
                
def get_response_from_openai(resume_text, job_description):
    client = OpenAI()
    messages = [
    {"role": "system", "content": "You are a helpful AI assistant.You will be given a resume and a job description. You need to generate an email response to the job description based on the resume."},
    {
        "role": "user",
        "content": 
            f'''Based on the resume provided below, generate an email response to the job description provided below. 
                Take necessary information about me from the resume.
                Emphasize the skills and experiences that are relevant to the job description.
                
                <Resume>
                {resume_text}
                </Resume>
                
                <Job Description>
                {job_description}
                </Job Description>
                
                Output your response with just the content of the email (without the subject line).
                
        '''
    }
]


    # Call the OpenAI GPT-4 model using the chat endpoint
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # You can use "gpt-4" or "gpt-3.5-turbo"
        messages=messages,
        temperature=0,
    )
    
    answer = response.choices[0].message.content.strip()
    return answer
    