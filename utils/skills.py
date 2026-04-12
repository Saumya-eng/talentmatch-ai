import re

# ---------------- SKILLS DATABASE WITH SYNONYMS ---------------- #

SKILLS_DB = {
    "python": ["python", "python3"],
    "java": ["java"],
    "c++": ["c++"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript"],

    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "nlp": ["nlp", "natural language processing"],
    "data analysis": ["data analysis", "data analytics"],

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],

    "sql": ["sql"],
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb"],

    "excel": ["excel"],
    "power bi": ["power bi", "powerbi"],
    "tableau": ["tableau"],

    "html": ["html"],
    "css": ["css"],
    "react": ["react", "reactjs"],
    "node": ["node", "nodejs", "node.js"],

    "flask": ["flask"],
    "django": ["django"],

    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "gcp": ["gcp", "google cloud"],

    "git": ["git"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "linux": ["linux"]
}


# ---------------- NORMALIZE TEXT ---------------- #
def normalize_text(text):
    """
    Normalize text for better matching
    """
    text = text.lower()

    # Normalize common variations
    text = text.replace("node.js", "nodejs")
    text = text.replace("react.js", "reactjs")

    return text


# ---------------- EXTRACT SKILLS ---------------- #
def extract_skills(text):
    """
    Extract skills using keyword + synonym matching
    """

    if not text:
        return []

    text = normalize_text(text)

    found_skills = set()

    for skill, keywords in SKILLS_DB.items():
        for keyword in keywords:

            # Flexible matching (handles python-based, ml-model, etc.)
            pattern = r'\b' + re.escape(keyword) + r'[\w\-]*\b'

            if re.search(pattern, text):
                found_skills.add(skill)

    return sorted(list(found_skills))


# ---------------- SKILL MATCH SCORE ---------------- #
def skill_match_score(jd_skills, resume_skills):
    """
    Calculate normalized skill match score (0 to 1)
    """

    if not jd_skills:
        return 0.0

    jd_set = set(jd_skills)
    resume_set = set(resume_skills)

    matched = jd_set.intersection(resume_set)

    return len(matched) / len(jd_set)


# ---------------- SKILL GAP ---------------- #
def get_missing_skills(jd_skills, resume_skills):
    """
    Return missing skills (for UI)
    """
    return list(set(jd_skills) - set(resume_skills))