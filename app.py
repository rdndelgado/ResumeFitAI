import streamlit as st
from datetime import datetime
from models.embedding_model import load_model
from utils.file_parser import extract_text_from_pdf, extract_text_from_docx
from utils.similarity import rank_resumes
from utils.resume_quality import score_resume

# Streamlit Page Config
st.set_page_config(page_title="ResumeFit AI", layout="wide")

# Header
st.title("📄 ResumeFit AI")
st.write("Upload a job description and resumes to rank candidates by semantic similarity using transformer embeddings, with resume quality checks for missing info and structure.")
st.divider()

# Load embedding model
model = load_model()

# Body
input_grid = st.columns(2)

# Job Description
with input_grid[0]:

    st.header("Job Description")
    job_input_type = st.radio("Provide job description:", ("Upload PDF", "Paste Text"))

    job_text = ""
    if job_input_type == "Upload PDF":
        jd_file = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])
        if jd_file:
            job_text = extract_text_from_pdf(jd_file)
            st.text_area("Preview", job_text, height=200)
    else:
        job_text = st.text_area("Paste Job Description", height=200)

# Resume (s)
with input_grid[1]:
    st.header("Candidate Resumes")
    resume_files = st.file_uploader("Upload Resumes (PDF/DOCX)", type=["pdf", "docx"], accept_multiple_files=True)

    resumes_texts = []
    if resume_files:
        for file in resume_files:
            if file.type == "application/pdf":
                text = extract_text_from_pdf(file)
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                text = extract_text_from_docx(file)
            else:
                text = ""

            resumes_texts.append({"name": file.name, "text": text})

        st.success(f"Uploaded {len(resumes_texts)} resumes")

# Ranking
if st.button("Rank Resumes"):
    if not job_text:
        st.warning("⚠️ Provide a job description first.")
    elif not resumes_texts:
        st.warning("⚠️ Upload at least one resume.")
    else:
        # Run ranking only once, store in session state
        st.session_state["results"] = rank_resumes(model, job_text, resumes_texts)
st.divider()

# Results
if "results" in st.session_state:

    results = st.session_state["results"]
    max_n = len(results)

    result_grid = st.columns(8)

    with result_grid[0]:
        top_n = st.number_input("Filter results", min_value=1, max_value=max_n, value=max_n, step=1)
    st.subheader(f"🔎 Top {top_n} Ranked Resumes")

    for r in results[:top_n]:
        quality = score_resume(r['text'])

        with st.expander(f"{r['name']} → Similarity: `{r['score']*100:.1f}%`"):
            st.write(f"Resume Quality: `{quality['score']}/100`")

            if quality["issues"]:
                st.warning("⚠️ Issues: " + ", ".join(quality["issues"]))
            else:
                st.success("✅ No major issues found")

# Footer
current_year = datetime.now().year
st.write("")
st.caption(f"© {current_year} Rudini Delgado | ResumeFit AI | Built with Streamlit")
