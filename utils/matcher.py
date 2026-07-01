<<<<<<< HEAD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ---------------- TF-IDF SIMILARITY ---------------- #
def compute_tfidf_similarity(job_description, resumes):
    """
    Compute cosine similarity using TF-IDF
    Returns list of scores (0 to 1)
    """

    if not resumes:
        return []

    try:
        documents = [job_description] + resumes

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        tfidf_matrix = vectorizer.fit_transform(documents)

        jd_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]

        similarities = cosine_similarity(jd_vector, resume_vectors)[0]

        return similarities.tolist()  # ✅ ensure list

    except Exception as e:
        print("TF-IDF error:", e)
        return [0.0] * len(resumes)


# ---------------- HYBRID SIMILARITY ---------------- #
def combine_similarity(semantic_scores, tfidf_scores, alpha=0.7):
    """
    Combine BERT + TF-IDF scores
    alpha = weight for semantic similarity
    """

    if not semantic_scores:
        return []

    if not tfidf_scores or len(semantic_scores) != len(tfidf_scores):
        return semantic_scores  # fallback

    combined = []

    for s, t in zip(semantic_scores, tfidf_scores):
        try:
            score = alpha * float(s) + (1 - alpha) * float(t)
        except:
            score = float(s)
        combined.append(score)

    return combined


# ---------------- NORMALIZATION (OPTIONAL) ---------------- #
def normalize_scores(scores):
    """
    Normalize scores to 0–1 range
    """

    if not scores:
        return scores

    max_score = max(scores)
    min_score = min(scores)

    if max_score == min_score:
        return [1.0 for _ in scores]

    return [(s - min_score) / (max_score - min_score) for s in scores]


# ---------------- RANKING ---------------- #
def rank_resumes(resume_names, scores):
    """
    Return ranked resumes with scores
    """

    if not resume_names or not scores:
        return []

    results = list(zip(resume_names, scores))
    results.sort(key=lambda x: x[1], reverse=True)

=======
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# ---------------- TF-IDF SIMILARITY ---------------- #
def compute_tfidf_similarity(job_description, resumes):
    """
    Compute cosine similarity using TF-IDF
    Returns list of scores (0 to 1)
    """

    if not resumes:
        return []

    try:
        documents = [job_description] + resumes

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        tfidf_matrix = vectorizer.fit_transform(documents)

        jd_vector = tfidf_matrix[0]
        resume_vectors = tfidf_matrix[1:]

        similarities = cosine_similarity(jd_vector, resume_vectors)[0]

        return similarities.tolist()  # ✅ ensure list

    except Exception as e:
        print("TF-IDF error:", e)
        return [0.0] * len(resumes)


# ---------------- HYBRID SIMILARITY ---------------- #
def combine_similarity(semantic_scores, tfidf_scores, alpha=0.7):
    """
    Combine BERT + TF-IDF scores
    alpha = weight for semantic similarity
    """

    if not semantic_scores:
        return []

    if not tfidf_scores or len(semantic_scores) != len(tfidf_scores):
        return semantic_scores  # fallback

    combined = []

    for s, t in zip(semantic_scores, tfidf_scores):
        try:
            score = alpha * float(s) + (1 - alpha) * float(t)
        except:
            score = float(s)
        combined.append(score)

    return combined


# ---------------- NORMALIZATION (OPTIONAL) ---------------- #
def normalize_scores(scores):
    """
    Normalize scores to 0–1 range
    """

    if not scores:
        return scores

    max_score = max(scores)
    min_score = min(scores)

    if max_score == min_score:
        return [1.0 for _ in scores]

    return [(s - min_score) / (max_score - min_score) for s in scores]


# ---------------- RANKING ---------------- #
def rank_resumes(resume_names, scores):
    """
    Return ranked resumes with scores
    """

    if not resume_names or not scores:
        return []

    results = list(zip(resume_names, scores))
    results.sort(key=lambda x: x[1], reverse=True)

>>>>>>> 118300982c44287abdc232ca47b54103d0994b90
    return results