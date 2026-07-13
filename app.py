import streamlit as st
import pdfplumber
import docx2txt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
import spacy

# Load NLP model

nlp = spacy.load("en_core_web_sm")

# Function to extract text
def extract_text(file):
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            return ' '.join([page.extract_text() or '' for page in pdf.pages])
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    else:
        return ""

# Clean text
def clean_text(text):
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.lower()

# Extract keywords using SpaCy
def extract_keywords(text):
    doc = nlp(text)
    return list(set([token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop]))

#TF-IDF = Term Frequency - Inverse Document Frequency
# Calculate similarity
def calculate_similarity(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    return round(score * 100, 2)

# Streamlit UI
st.title("🧠 AI Resume Analyzer")

# Upload multiple resumes
resumes = st.file_uploader("📄 Upload Resumes (.pdf or .docx)", type=['pdf', 'docx'], accept_multiple_files=True)

# Upload job description
jd_file = st.file_uploader("📄 Upload Job Description (.pdf or .docx)", type=['pdf', 'docx'])

if resumes and jd_file:
    jd_text = clean_text(extract_text(jd_file))
    st.subheader("📄 Job Description")
    st.write(jd_text)

    # Initialize lists to store results
    match_scores = []
    matched_skills_list = []
    missing_skills_list = []

    for resume_file in resumes:
        resume_text = clean_text(extract_text(resume_file))
        score = calculate_similarity(resume_text, jd_text)
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(jd_text)

        matched_skills = list(set(resume_keywords) & set(jd_keywords))
        missing_skills = list(set(jd_keywords) - set(resume_keywords))

        # Append results
        match_scores.append(score)
        matched_skills_list.append(matched_skills)
        missing_skills_list.append(missing_skills)

        # Display results for each resume
        st.subheader(f"📄 {resume_file.name}")
        st.write(f"✅ Match Score: {score} %")
        st.write("### ✅ Matched Skills")
        st.write(', '.join(matched_skills) if matched_skills else "None")
        st.write("### ⚠️ Missing Skills")
        st.write(', '.join(missing_skills) if missing_skills else "None")

        if score < 60:
            st.info("Consider updating your resume to include the missing skills.")

    # Rank resumes based on match score
    best_match_index = match_scores.index(max(match_scores))
    st.subheader("🏆 Best Match")
    st.write(f"The best matching resume is: {resumes[best_match_index].name} with a match score of {match_scores[best_match_index]}%")
else:
    st.info("Please upload both resumes and a job description to analyze.")