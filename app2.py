import streamlit as st
import pdfplumber
import docx2txt
import json
import re

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity



# ==========================
# LOAD SKILLS
# ==========================

with open("skills.json") as f:
    SKILLS = json.load(f)



# ==========================
# LOAD AI MODEL
# ==========================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)



# ==========================
# TEXT EXTRACTION
# ==========================

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



# ==========================
# SKILL EXTRACTION
# ==========================

def extract_skills(text):

    found=[]

    text=text.lower()


    for skill in SKILLS:

        pattern = r"\b" + re.escape(skill) + r"\b"


        if re.search(pattern,text):

            found.append(skill)


    return list(set(found))



# ==========================
# NAME EXTRACTION
# ==========================

def extract_name(text):

    lines=text.split("\n")


    for line in lines:

        line=line.strip()

        if len(line)>2:

            return line


    return "Unknown"



# ==========================
# EXPERIENCE EXTRACTION
# ==========================

def extract_experience(text):

    years=re.findall(
        r'(\d+)\+?\s*(?:years|year)',
        text.lower()
    )


    if years:

        return max(
            [int(x) for x in years]
        )


    return 0



# ==========================
# EDUCATION EXTRACTION
# ==========================

def extract_education(text):

    education=[]


    keywords=[
        "b.tech",
        "b.e",
        "m.tech",
        "mca",
        "mba",
        "computer science",
        "engineering",
        "degree"
    ]


    text=text.lower()


    for word in keywords:

        if word in text:

            education.append(word)


    return list(set(education))




# ==========================
# CREATE RESUME JSON
# ==========================

def create_resume_json(text):

    return {

        "name":
        extract_name(text),


        "skills":
        extract_skills(text),


        "experience_years":
        extract_experience(text),


        "education":
        extract_education(text)

    }




# ==========================
# CREATE JD JSON
# ==========================

def create_jd_json(text):

    return {

        "required_skills":
        extract_skills(text),


        "experience_required":
        extract_experience(text)

    }
# ==========================
# SKILL SCORE
# ==========================

def calculate_skill_score(
        resume_skills,
        jd_skills
):

    if len(jd_skills)==0:

        return 0



    matched = list(
        set(resume_skills)
        &
        set(jd_skills)
    )



    score = (
        len(matched)
        /
        len(jd_skills)
    ) * 100



    return round(score,2)




# ==========================
# SEMANTIC AI SCORE
# ==========================

def calculate_semantic_score(
        resume_text,
        jd_text
):


    resume_vector=model.encode(
        resume_text
    )


    jd_vector=model.encode(
        jd_text
    )


    score=cosine_similarity(
        [resume_vector],
        [jd_vector]
    )[0][0]


    return round(
        score*100,
        2
    )




# ==========================
# EXPERIENCE SCORE
# ==========================

def calculate_experience_score(
        resume_exp,
        jd_exp
):

    if jd_exp==0:

        return 100



    if resume_exp >= jd_exp:

        return 100



    return round(
        (resume_exp/jd_exp)*100,
        2
    )




# ==========================
# FINAL ATS SCORE
# ==========================

def calculate_ats_score(
        skill,
        semantic,
        experience
):


    score=(

        skill*0.50

        +

        semantic*0.30

        +

        experience*0.15

        +

        100*0.05

    )


    return round(score,2)




# ==========================
# STREAMLIT UI
# ==========================


st.title(
    "🤖 AI ATS Resume Analyzer"
)



resume_file=st.file_uploader(
    "Upload Resume",
    type=["pdf","docx"]
)



jd_file=st.file_uploader(
    "Upload Job Description",
    type=["pdf","docx"]
)





if resume_file and jd_file:


    # TEXT

    resume_text=extract_text(
        resume_file
    )


    jd_text=extract_text(
        jd_file
    )



    # JSON

    resume_json=create_resume_json(
        resume_text
    )


    jd_json=create_jd_json(
        jd_text
    )



    st.subheader(
        "📄 Resume JSON"
    )

    st.json(
        resume_json
    )



    st.subheader(
        "📌 JD JSON"
    )

    st.json(
        jd_json
    )




    # SCORE


    skill_score = calculate_skill_score(
        resume_json["skills"],
        jd_json["required_skills"]
    )



    semantic_score = calculate_semantic_score(
        resume_text,
        jd_text
    )



    experience_score = calculate_experience_score(
        resume_json["experience_years"],
        jd_json["experience_required"]
    )



    ats_score = calculate_ats_score(
        skill_score,
        semantic_score,
        experience_score
    )



    matched=list(
        set(resume_json["skills"])
        &
        set(jd_json["required_skills"])
    )


    missing=list(
        set(jd_json["required_skills"])
        -
        set(resume_json["skills"])
    )



    st.divider()


    st.subheader(
        "🏆 ATS RESULT"
    )



    st.metric(
        "Final ATS Score",
        f"{ats_score}%"
    )



    st.write(
        "🎯 Skill Score:",
        skill_score
    )


    st.write(
        "🧠 Semantic AI Score:",
        semantic_score
    )


    st.write(
        "💼 Experience Score:",
        experience_score
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



else:


    st.info(
        "Upload Resume and Job Description"
    )