import streamlit as st
import google.generativeai as genai
import os
import PyPDF2  as pdf
from dotenv import load_dotenv
import json

load_dotenv() # load all the environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text

def input_pdf_text(upload_file):
    reader = pdf.PdfReader(upload_file)
    text=""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template for our input

input_prompt = """Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and the missing keywords with high accuracy.
resume:{text}
description:{jd}

I want the response in one single string having the structure
{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}
"""

#Streamlit App

st.title("Resume Analysis")
st.text("Upload the JD and resume file")
jd = st.text_area("Paste the Job Description from the Job")
upload_file = st.file_uploader("Upload you resume",type='pdf',help="Please upload the resume PDF")
submit = st.button("Submit")

if submit:
    if upload_file is not None:
        text = input_pdf_text(upload_file)
        response = get_gemini_response(input_prompt)
        st.json(json.loads(response))