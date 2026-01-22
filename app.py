import streamlit as st
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# -------- LLM --------
def get_llm_response(prompt):
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )
    response = llm.invoke(prompt)
    return response.content


# -------- PDF READER --------
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# -------- PROMPT --------
input_prompt = """
You are an expert ATS (Applicant Tracking System).

Evaluate the resume against the job description.

Return ONLY valid JSON in this format:
{{
  "JD Match": "%",
  "Missing Keywords": [],
  "Profile Summary": ""
}}

Resume:
{resume}

Job Description:
{jd}
"""


# -------- STREAMLIT UI --------
st.title("Smart ATS")
st.text("Improve Your Resume ATS Score")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf")

submit = st.button("Submit")

if submit:
    if uploaded_file and jd:
        resume_text = input_pdf_text(uploaded_file)

        final_prompt = input_prompt.format(
            resume=resume_text,
            jd=jd
        )

        response = get_llm_response(final_prompt)

        st.subheader("ATS Analysis")
        st.write(response)
