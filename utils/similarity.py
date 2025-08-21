from sentence_transformers import util

def rank_resumes(model, job_text, resumes_texts):
    jd_embedding = model.encode(job_text, convert_to_tensor=True)
    results = []

    for resume in resumes_texts:
        if resume["text"].strip():
            embedding = model.encode(resume["text"], convert_to_tensor=True)
            score = util.cos_sim(jd_embedding, embedding).item()
            results.append({"name": resume["name"], "text": resume["text"].strip(), "score": score})

    # Sort by highest score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results
