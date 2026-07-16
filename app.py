import streamlit as st
import PyPDF2

st.set_page_config(page_title="HirePilot - AI Resume Screening System")

st.title("HirePilot - AI Resume Screening System")
st.write("Upload your Resume and Job Description to check the ATS Match Score.")

# Upload Files
resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])


# Function to Read PDF
def read_pdf(file):
    pdf = PyPDF2.PdfReader(file)
    text = ""

    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


# Process Files
if resume and job:

    resume_text = read_pdf(resume)
    job_text = read_pdf(job)

    st.success("Files uploaded successfully.")

    st.subheader("Resume Preview")
    st.write(resume_text[:1000])

    st.subheader("Job Description Preview")
    st.write(job_text[:1000])

    # Convert to lowercase
    resume_words = set(resume_text.lower().split())
    job_words = set(job_text.lower().split())

    # Matching and Missing Words
    matching_words = resume_words.intersection(job_words)
    missing_words = job_words - resume_words

    # Calculate Match Score
    if len(job_words) > 0:
        score = (len(matching_words) / len(job_words)) * 100
    else:
        score = 0

    st.subheader("Resume Match Score")
    st.progress(min(int(score), 100))
    st.write(f"Match Score: {score:.2f}%")

    st.subheader("Matching Keywords")
    if matching_words:
        st.write(", ".join(sorted(list(matching_words))[:50]))
    else:
        st.write("No matching keywords found.")

    st.subheader("Missing Keywords")
    if missing_words:
        st.write(", ".join(sorted(list(missing_words))[:50]))
    else:
        st.write("No missing keywords.")

    st.subheader("Final Result")

    if score >= 70:
        st.success("Candidate is Selected")
    elif score >= 50:
        st.warning("Candidate may be Considered")
    else:
        st.error("Candidate is Rejected")

else:
    st.info("Please upload both the Resume and Job Description.")
