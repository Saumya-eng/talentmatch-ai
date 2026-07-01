<<<<<<< HEAD
import re


# ---------------- DEGREE EXTRACTION ---------------- #
def extract_education(text):
    text = text.lower()

    degree_map = {
        "btech": r"b\.?\s?tech",
        "mtech": r"m\.?\s?tech",
        "be": r"b\.?\s?e",
        "me": r"m\.?\s?e",
        "bachelor": r"bachelor(?:'s)?",
        "master": r"master(?:'s)?",
        "mba": r"mba",
        "bsc": r"bsc",
        "msc": r"msc",
        "phd": r"phd"
    }

    found = set()

    for name, pattern in degree_map.items():
        if re.search(pattern, text):
            found.add(name)

    return list(found)


# ---------------- EXPERIENCE EXTRACTION ---------------- #
def extract_experience(text):
    """
    Extract years of experience from various formats
    """

    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*(years|yrs|year)',
        r'(\d+)\s*-\s*(\d+)\s*(years|yrs)',
        r'over\s*(\d+)\s*(years|yrs)',
        r'(\d+)\s*(years|yrs)\s*of\s*experience'
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                if len(match) == 2:
                    years.append(int(match[0]))
                elif len(match) == 3:
                    years.append(int(match[1]))  # upper range
            except:
                continue

    return max(years) if years else 0


# ---------------- COMPANY EXTRACTION ---------------- #
def extract_companies(text):
    """
    Extract company names using contextual patterns
    """

    # Patterns like: "at Infosys", "worked at TCS"
    patterns = [
        r'at\s+([A-Z][a-zA-Z&\s]+)',
        r'with\s+([A-Z][a-zA-Z&\s]+)',
        r'for\s+([A-Z][a-zA-Z&\s]+)'
    ]

    companies = set()

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            cleaned = m.strip()
            if len(cleaned) > 2:
                companies.add(cleaned)

    return list(companies)


# ---------------- MAIN PARSER ---------------- #
def parse_resume_details(text):
    return {
        "education": extract_education(text),
        "experience_years": extract_experience(text),
        "companies": extract_companies(text)
=======
import re


# ---------------- DEGREE EXTRACTION ---------------- #
def extract_education(text):
    text = text.lower()

    degree_map = {
        "btech": r"b\.?\s?tech",
        "mtech": r"m\.?\s?tech",
        "be": r"b\.?\s?e",
        "me": r"m\.?\s?e",
        "bachelor": r"bachelor(?:'s)?",
        "master": r"master(?:'s)?",
        "mba": r"mba",
        "bsc": r"bsc",
        "msc": r"msc",
        "phd": r"phd"
    }

    found = set()

    for name, pattern in degree_map.items():
        if re.search(pattern, text):
            found.add(name)

    return list(found)


# ---------------- EXPERIENCE EXTRACTION ---------------- #
def extract_experience(text):
    """
    Extract years of experience from various formats
    """

    text = text.lower()

    patterns = [
        r'(\d+)\+?\s*(years|yrs|year)',
        r'(\d+)\s*-\s*(\d+)\s*(years|yrs)',
        r'over\s*(\d+)\s*(years|yrs)',
        r'(\d+)\s*(years|yrs)\s*of\s*experience'
    ]

    years = []

    for pattern in patterns:
        matches = re.findall(pattern, text)

        for match in matches:
            try:
                if len(match) == 2:
                    years.append(int(match[0]))
                elif len(match) == 3:
                    years.append(int(match[1]))  # upper range
            except:
                continue

    return max(years) if years else 0


# ---------------- COMPANY EXTRACTION ---------------- #
def extract_companies(text):
    """
    Extract company names using contextual patterns
    """

    # Patterns like: "at Infosys", "worked at TCS"
    patterns = [
        r'at\s+([A-Z][a-zA-Z&\s]+)',
        r'with\s+([A-Z][a-zA-Z&\s]+)',
        r'for\s+([A-Z][a-zA-Z&\s]+)'
    ]

    companies = set()

    for pattern in patterns:
        matches = re.findall(pattern, text)
        for m in matches:
            cleaned = m.strip()
            if len(cleaned) > 2:
                companies.add(cleaned)

    return list(companies)


# ---------------- MAIN PARSER ---------------- #
def parse_resume_details(text):
    return {
        "education": extract_education(text),
        "experience_years": extract_experience(text),
        "companies": extract_companies(text)
>>>>>>> 118300982c44287abdc232ca47b54103d0994b90
    }