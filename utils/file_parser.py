import fitz  # PyMuPDF
import docx

def extract_text_from_pdf(file) -> str:
    text = ""
    links_text = []
    
    with fitz.open(stream=file.read(), filetype="pdf") as pdf:
        for page in pdf:
            # Extract visible text
            page_text = page.get_text("text")
            if page_text:
                text += page_text + "\n"
            
            # Extract all links
            for link in page.get_links():
                if "uri" in link:  # external URLs
                    links_text.append(link["uri"])

    # Deduplicate links and append at the end
    if links_text:
        text += "\n\nLinks:\n" + "\n".join(sorted(set(links_text)))

    return text.strip()


def extract_text_from_docx(file) -> str:
    doc = docx.Document(file)
    text = []
    links = []

    # Extract paragraph text
    for para in doc.paragraphs:
        if para.text.strip():
            text.append(para.text)

    # Extract hyperlinks from document XML
    rels = doc.part.rels
    for rel in rels:
        if "hyperlink" in rels[rel].reltype:
            links.append(rels[rel].target_ref)

    result = "\n".join(text)
    
    if links:
        result += "\n\nLinks:\n" + "\n".join(sorted(set(links)))

    return result.strip()
