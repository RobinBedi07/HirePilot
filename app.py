import streamlit as st
import PyPDF2
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="HirePilot Resume_Screening_System",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>
.title{
    text-align:center;
    color:#00C853;
    font-size:42px;
    font-weight:bold;
}
.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='title'>🤖 HirePilot Resume_Screening_System</p>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI Resume Screening & ATS Analysis System</p>", unsafe_allow_html=True)

st.divider()


col1, col2 = st.columns(2)

with col1:
    resume = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

with col2:
    job = st.file_uploader("📋 Upload Job Description (PDF)", type=["pdf"])



def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text



if resume and job:

    resume_text = read_pdf(resume)
    job_text = read_pdf(job)

    st.success("✅ Files uploaded successfully!")

    st.subheader("📄 Resume Preview")
    st.write(resume_text[:1000])

    st.subheader("📋 Job Description Preview")
    st.write(job_text[:1000])

    
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    
    matching_words = resume_words.intersection(job_words)
    missing_words = job_words - resume_words

    
    if len(job_words) > 0:
        score = (len(matching_words) / len(job_words)) * 100
    else:
        score = 0

    
    st.subheader("📊 ATS Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("ATS Score", f"{score:.2f}%")

    with col2:
        if score >= 80:
            st.success("Excellent Match")
        elif score >= 60:
            st.warning("Good Match")
        else:
            st.error("Needs Improvement")

    st.progress(min(int(score), 100))

    
    st.subheader("✅ Matching Skills")

    if matching_words:
        st.write(", ".join(sorted(list(matching_words))[:50]))
    else:
        st.write("No matching skills found.")


    st.subheader("❌ Missing Skills")

    if missing_words:
        st.write(", ".join(sorted(list(missing_words))[:50]))
    else:
        st.write("No missing skills.")

    
    st.subheader("💡 AI Suggestions")

    if score >= 80:
        st.success("Excellent resume. Your profile matches this job very well.")
    elif score >= 60:
        st.warning("Good resume. Add more relevant technical skills to improve your ATS score.")
    else:
        st.error("Your resume needs improvement to increase the ATS score.")

    if missing_words:
        st.info("Important missing keywords:")
        st.write(", ".join(sorted(list(missing_words))[:20]))


    st.subheader("🏆 Final Result")

    if score >= 70:
        st.success("Candidate is Selected")
    elif score >= 50:
        st.warning("Candidate may be Considered")
    else:
        st.error("Candidate is Rejected")

else:
    st.info("📂 Please upload both the Resume and Job Description.")
