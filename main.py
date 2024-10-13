import streamlit as st
from utils.utils import extract_text_from_pdf, send_email, get_response_from_openai
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    # Initialize session state variables
    if 'editable_email' not in st.session_state:
        st.session_state.editable_email = ''
    if 'subject' not in st.session_state:
        st.session_state.subject = 'Application for Generative AI Engineer Intern'
    
    st.title("Auto Email Sender")

    email_id = st.text_input("Enter Email ID")
    job_description = st.text_area("Enter Job Description")
    
    if st.button("Submit"):
        resume_text = extract_text_from_pdf(st.secrets("resume_path"))
        generated_email = get_response_from_openai(resume_text, job_description)
        st.session_state.editable_email = generated_email  # Store the generated email in session state
    
    st.subheader("Generated Email")
    # Use the session state for editable email content
    editable_email = st.text_area("Generated Email Content", st.session_state.editable_email, height=300)

    st.subheader("Subject")
    # Use the session state for subject content
    subject = st.text_input("Subject", st.session_state.subject)

    if st.button("Send Email"):
        send_email(email_id, editable_email, subject)
        st.balloons()

if __name__ == "__main__":
    main()
