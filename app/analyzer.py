import spacy
import re

nlp = spacy.load('en_core_web_sm')

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
    return list(set(keywords))

def analyze_resume_against_jd(resume_text, job_desc):
    resume_text = resume_text.lower()
    job_keywords = extract_keywords(job_desc)
    matched = []
    missing = []

    for kw in job_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', resume_text):
            matched.append(kw)
        else:
            missing.append(kw)

    ats_score = int((len(matched) / len(job_keywords)) * 100) if job_keywords else 0

    doc = nlp(resume_text)
    action_verbs = [token.lemma_ for token in doc if token.pos_ == "VERB"]
    action_score = int(min((len(set(action_verbs)) / 20) * 100, 100))

    suggestions = []
    if ats_score < 70:
        suggestions.append("Align your resume more with the job description.")
    if action_score < 50:
        suggestions.append("Use more strong action verbs.")
    if len(resume_text.split()) < 300:
        suggestions.append("Consider adding more detailed experience.")

    return {
        'ats_score': ats_score,
        'matched_keywords': matched,
        'missing_keywords': missing,
        'action_verbs_used': len(set(action_verbs)),
        'action_verb_score': action_score,
        'suggestions': suggestions
    }
