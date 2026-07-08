import streamlit as st
import PyPDF2
st.set_page_config(page_title="Resume Screening System")
st.title("AI Resume Screening System")
st.write("upload your resume and Job descriptions.")
#upload resume
resume = st.file_uploader("upload Resume (PDF)" , type=["pdf"])
# upload job decription
job = st.file_uploader("upload job Description (PDF)",type=["pdf"])

def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text =""
    for page in pdf.pages:
        text += page.extract_text()
    return text
if resume and job:
    resume_text = read_pdf(resume)
    job_text = read_pdf(job)

    st.success("files upload successfully!")

    st.subheader("Resume Preview")
    st.write(resume_text[:1000])

    st.subheader("Job Description Preview")

    st.write(job_text[:1000])

# Convert text to lowercase
resume_words = set(resume_text.lower().split())
job_words = set(job_text.lower().split())

# Find matching words
matching_words = resume_words.intersection(job_words)

# Calculate score
score = (len(matching_words) / len(job_words)) * 100

st.subheader("Resume Match Score")
st.progress(min(int(score), 100))
st.write(f"Match Score: {score:.2f}%")

st.subheader("Matching Keywords")
st.write(", ".join(list(matching_words)[:50]))

st.subheader("Result")
if score >= 50:
    st.success("Candidate is selected")
elif score >= 50:
    st.warning("Candidate may be considered")
else:
    st.error("Candidate is rejected")

missing_words =job_words-resume_words

st.subheader("Missing Keywords")
st.write(",".join(list(missing_words)[:50]))