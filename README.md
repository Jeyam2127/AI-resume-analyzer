# 🤖 AI Resume Analyzer (ATS-Based)
## 📌 Overview

The **AI Resume Analyzer** is a web-based application that mimics the behavior of an **Applicant Tracking System (ATS)** by analyzing resumes against a given job description.

It uses **Natural Language Processing (NLP)** and **TF-IDF-based similarity scoring** to evaluate how well a resume matches a job role and provides actionable insights for improvement.

---

## 🎯 Features

* 📄 **Multi-Resume Upload**
  Upload and analyze multiple resumes at once

* 📊 **ATS Match Score**
  Calculates similarity between resume and job description using TF-IDF + cosine similarity

* 🧠 **Keyword Extraction (NLP)**
  Uses SpaCy to extract meaningful keywords (nouns & proper nouns)

* ✅ **Matched Skills Detection**
  Identifies overlapping skills between resume and JD

* ⚠️ **Missing Skills Identification**
  Highlights important skills missing from the resume

* 🏆 **Best Resume Ranking**
  Automatically ranks and selects the best matching resume

---

## 🛠️ Tech Stack

* **Frontend & UI:** Streamlit
* **Backend:** Python

### 📚 Libraries Used

* `streamlit` – Interactive UI
* `pdfplumber` – PDF text extraction
* `docx2txt` – DOCX parsing
* `scikit-learn` – TF-IDF & cosine similarity
* `spaCy` – NLP & keyword extraction
* `re` – Text preprocessing

---

## ⚙️ How It Works

1. Upload one or more **Resumes** (.pdf or .docx)
2. Upload a **Job Description**
3. The system:

   * Extracts and cleans text
   * Applies NLP for keyword extraction
   * Computes similarity score using TF-IDF
4. Outputs:

   * Match Score (%)
   * Matched Skills
   * Missing Skills
   * Best Resume Ranking

---

## 🧠 Core Logic

### 🔹 Text Extraction

* Supports both PDF and DOCX formats
* Uses `pdfplumber` and `docx2txt`

### 🔹 Text Preprocessing

* Removes special characters
* Converts text to lowercase
* Normalizes input for accurate comparison

### 🔹 Similarity Calculation

* Uses **TF-IDF Vectorization**
* Applies **Cosine Similarity** to compute match score

### 🔹 Skill Analysis

* Extracts keywords using **SpaCy NLP model**
* Compares:

  * Resume Keywords ∩ JD Keywords → Matched Skills
  * JD Keywords − Resume Keywords → Missing Skills

---

## 📈 Example Output

* ✅ Match Score: 72.45%
* ✅ Matched Skills: Python, Machine Learning, SQL
* ⚠️ Missing Skills: Docker, Kubernetes, AWS

---

## 🚀 How to Run

```bash
# Clone the repository
git clone https://github.com/your-username/ai-resume-analyzer.git

# Navigate to project folder
cd ai-resume-analyzer

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

---

## 🔮 Limitations (Be Honest)

* Keyword-based matching (not deep semantic understanding)
* No context-aware skill evaluation
* Depends on quality of job description
* Basic NLP model (spaCy small model)

---

## 🔮 Future Improvements

* Use transformer models (BERT / LLMs) for better semantic matching
* Resume rewriting suggestions
* Skill weighting based on job role
* Integration with job portals (LinkedIn, Indeed)
* Improved UI/UX

---

## 📄 License

This project is open-source and available under the MIT License.
