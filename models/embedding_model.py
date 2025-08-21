from sentence_transformers import SentenceTransformer
import streamlit as st

@st.cache_resource
def load_model():
    try:
        # Primary model
        return SentenceTransformer("BAAI/bge-small-en")
    except Exception as e:
        st.warning(f"⚠️ Could not load 'BAAI/bge-small-en'. Falling back to 'all-MiniLM-L6-v2'. Error: {e}")
        # Fallback model
        return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")