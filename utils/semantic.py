from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---------------- LOAD MODEL (ONCE) ---------------- #
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print("Error loading model:", e)
    model = None


# ---------------- SEMANTIC SIMILARITY ---------------- #
def compute_semantic_similarity(job_description, resumes):
    """
    Compute semantic similarity using Sentence-BERT embeddings
    Returns list of similarity scores (0 to 1)
    """

    if not model:
        return [0.0] * len(resumes)

    if not resumes:
        return []

    try:
        documents = [job_description] + resumes

        # ✅ optimized encoding
        embeddings = model.encode(
            documents,
            normalize_embeddings=True,
            batch_size=8
        )

        jd_embedding = embeddings[0]
        resume_embeddings = embeddings[1:]

        similarities = cosine_similarity(
            [jd_embedding],
            resume_embeddings
        )[0]

        return similarities.tolist()  # ✅ ensure list

    except Exception as e:
        print("Error in semantic similarity:", e)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# ---------------- LOAD MODEL (ONCE) ---------------- #
try:
    model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    print("Error loading model:", e)
    model = None


# ---------------- SEMANTIC SIMILARITY ---------------- #
def compute_semantic_similarity(job_description, resumes):
    """
    Compute semantic similarity using Sentence-BERT embeddings
    Returns list of similarity scores (0 to 1)
    """

    if not model:
        return [0.0] * len(resumes)

    if not resumes:
        return []

    try:
        documents = [job_description] + resumes

        # ✅ optimized encoding
        embeddings = model.encode(
            documents,
            normalize_embeddings=True,
            batch_size=8
        )

        jd_embedding = embeddings[0]
        resume_embeddings = embeddings[1:]

        similarities = cosine_similarity(
            [jd_embedding],
            resume_embeddings
        )[0]

        return similarities.tolist()  # ✅ ensure list

    except Exception as e:
        print("Error in semantic similarity:", e)
        return [0.0] * len(resumes)