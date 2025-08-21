# ResumeFit AI

A Streamlit-based application that ranks candidate resumes based on semantic similarity with a job description using transformer embeddings. Designed to help HR teams quickly screen and prioritize candidates.

---

## Features

- Upload a **job description** (PDF or text)
- Upload multiple **resumes** (PDF or DOCX)
- Generate **vector embeddings** using lightweight transformer models
- Compute **cosine similarity** between job description and resumes
- Display **ranked results** in an intuitive interface

---

## Transformer Models for Embeddings

This project uses **pretrained transformer models** from [Sentence Transformers](https://www.sbert.net/) to generate semantic embeddings:

- **Model:** `sentence-transformers/all-MiniLM-L6-v2`  
  - Lightweight and fast, suitable for CPU inference  
  - Converts text into 384-dimensional vector embeddings  
- **How it works:**  
  1. Job description and each resume are converted into embeddings  
  2. Cosine similarity is computed between JD embedding and each resume embedding  
  3. Candidates are ranked based on similarity score

---

## Installation

1. **Clone the repos

``bash``
git clone https://github.com/rdndelgado/ResumeFitAI.git
cd resumefit-ai

2. **Create and activate a virtual environment**

``bash``
# Linux / Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. **Install Dependencies**
``bash``
pip install -r requirements.txt

4. **Run the Streamlit app**
``bash``
streamlit run app.py