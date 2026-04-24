import streamlit as st
import PyPDF2
import re

st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume (PDF) and get instant feedback.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Analyze resume
def analyze_resume(text):
    score = 0
    feedback = []

    # Check sections
    sections = ["education", "experience", "skills", "projects"]
    for section in sections:
        if section in text.lower():
            score += 20
        else:
            feedback.append(f"❌ Missing section: {section.capitalize()}")

    # Check email
    if re.search(r"[\w\.-]+@[\w\.-]+", text):
        score += 10
    else:
        feedback.append("❌ Email not found")

    # Check phone number
    if re.search(r"\d{10}", text):
        score += 10
    else:
        feedback.append("❌ Phone number not found")

    return score, feedback

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)

    st.subheader("📊 Analysis Result")
    score, feedback = analyze_resume(text)

    st.progress(score / 100)
    st.write(f"### Resume Score: {score}/100")

    if feedback:
        st.subheader("🔍 Suggestions")
        for f in feedback:
            st.write(f)
    else:
        st.success("✅ Great resume! No major issues found.")

    st.subheader("📄 Extracted Text")
    st.text_area("", text, height=200)

st.markdown("---")
st.write("Made with ❤️ using Streamlit")
