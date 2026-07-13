import streamlit as st
import pdfplumber
import docx2txt
import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



# -------------------------------
# Load AI Model
# -------------------------------
#pre-trained Deep Learning NLP model.

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# -------------------------------
# Load Skills
# -------------------------------

with open("skills.json") as f:
    SKILLS=json.load(f)




# -------------------------------
# Extract Text
# -------------------------------

def extract_text(file):

    if file.name.endswith(".pdf"):

        text=""

        with pdfplumber.open(file) as pdf:

            for page in pdf.pages:
                text += page.extract_text() or ""

        return text


    elif file.name.endswith(".docx"):

        return docx2txt.process(file)

    return ""




# -------------------------------
# Cleaning
# -------------------------------

def clean_text(text):

    text=text.lower()

    text=re.sub(
        r'[^a-zA-Z0-9\s\+\#\.]',
        " ",
        text
    )

    return text




# -------------------------------
# AI Semantic Score
# -------------------------------

def ai_similarity(resume,jd):


    resume_vector=model.encode(
        resume
    )


    jd_vector=model.encode(
        jd
    )


    score=cosine_similarity(
        [resume_vector],
        [jd_vector]
    )[0][0]


    return round(score*100,2)




# -------------------------------
# Skill Extraction
# -------------------------------

def extract_skills(text):

    found=[]

    text=text.lower()


    for skill in SKILLS:

        if skill in text:

            found.append(skill)


    return list(set(found))





# -------------------------------
# Skill Score
# -------------------------------

def skill_score(
        resume_skills,
        jd_skills
):

    total=0
    matched=0


    for skill in jd_skills:

        weight=SKILLS[skill]

        total += weight


        if skill in resume_skills:

            matched += weight



    if total==0:
        return 0


    return round(
        (matched/total)*100,
        2
    )





# -------------------------------
# Final ATS Score
# -------------------------------

def final_score(
        ai_score,
        skill_score
):

    score = (
        ai_score*0.5
        +
        skill_score*0.5
    )


    return round(score,2)





# -------------------------------
# Streamlit UI
# -------------------------------


st.title(
    "🤖 AI ATS Resume Analyzer"
)



resumes=st.file_uploader(
    "Upload Resumes",
    type=["pdf","docx"],
    accept_multiple_files=True
)


jd_file=st.file_uploader(
    "Upload Job Description",
    type=["pdf","docx"]
)




if resumes and jd_file:


    jd_text=clean_text(
        extract_text(jd_file)
    )


    jd_skills=extract_skills(
        jd_text
    )


    st.subheader(
        "JD Required Skills"
    )

    st.write(
        jd_skills
    )


    results=[]



    for resume in resumes:


        resume_text=clean_text(
            extract_text(resume)
        )


        resume_skills=extract_skills(
            resume_text
        )


        ai_score=ai_similarity(
            resume_text,
            jd_text
        )


        skill_match=skill_score(
            resume_skills,
            jd_skills
        )


        ats=final_score(
            ai_score,
            skill_match
        )



        matched=list(
            set(resume_skills)
            &
            set(jd_skills)
        )


        missing=list(
            set(jd_skills)
            -
            set(resume_skills)
        )



        results.append(
            {
            "name":resume.name,
            "score":ats
            }
        )



        st.divider()

        st.header(
            resume.name
        )


        st.metric(
            "AI ATS Score",
            f"{ats}%"
        )


        st.write(
            "🧠 Semantic AI Score:",
            ai_score
        )


        st.write(
            "🎯 Skill Score:",
            skill_match
        )


        st.success(
            "Matched Skills"
        )

        st.write(
            matched
        )


        st.error(
            "Missing Skills"
        )

        st.write(
            missing
        )



        if ats < 60:

            st.warning(
                "Resume needs improvement for this job"
            )



    results.sort(
        key=lambda x:x["score"],
        reverse=True
    )


    st.divider()

    st.subheader(
        "🏆 Ranking"
    )


    for r in results:

        st.write(
            f"{r['name']} : {r['score']}%"
        )


else:

    st.info(
        "Upload Resume and JD"
    )