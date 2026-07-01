import re
import string

# ---------------- STOPWORDS ---------------- #
STOPWORDS = set([
    "the", "is", "in", "and", "to", "of", "a", "for", "on", "with",
    "as", "by", "an", "at", "from", "or", "that", "this", "it",
    "be", "are", "was", "were", "will", "can", "has", "have",
    "had", "not", "but", "we", "they", "their", "our", "you",
    "i", "me", "my", "he", "she", "his", "her"
])


# ---------------- CLEAN TEXT ---------------- #
def clean_text(text):
    """
    Clean text while preserving important information for NLP
    """

    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove phone numbers
    text = re.sub(r'\b\d{10}\b', ' ', text)

    # ⚠️ DO NOT remove all numbers (important for experience)
    # Instead, keep them

    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\+\-]', ' ', text)

    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    # Tokenize
    words = text.split()

    # Remove stopwords (light filtering)
    words = [word for word in words if word not in STOPWORDS]