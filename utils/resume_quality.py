import re

def score_resume(text: str) -> dict:
    score = 100
    issues = []

    # Length check
    word_count = len(text.split())
    if word_count < 150:
        score -= 20
        issues.append("Too short")
    elif word_count > 3000:
        score -= 10
        issues.append("Too long")

    # Contact info check
    if not re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text):
        score -= 15
        issues.append("Missing email")
    if not re.search(r"(\+?\d{1,3}[\s\-]?)?(\(?\d{2,4}\)?[\s\-]?)?\d{2,4}[\s\-]?\d{2,4}[\s\-]?\d{2,4}", text):
        score -= 10
        issues.append("Missing phone number")

    # LinkedIn
    if "linkedin.com" not in text.lower():
        score -= 5
        issues.append("No LinkedIn link")

    # Skills section
    if "skills" not in text.lower():
        score -= 15
        issues.append("No skills section")

    # Experience section
    if "experience" not in text.lower():
        score -= 15
        issues.append("No experience section")

    return {
        "score": max(score, 0),
        "issues": issues
    }