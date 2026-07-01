import PyPDF2
import docx2txt
import os


# ---------------- PDF ---------------- #
def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                try:
                    content = page.extract_text()
                    if content:
                        text += content + " "
                except Exception:
                    continue  # skip problematic pages

        if not text.strip():
            print(f"[EMPTY PDF TEXT] {file_path}")

    except Exception as e:
        print(f"[PDF ERROR] {file_path}: {e}")

    return text.strip()


# ---------------- DOCX ---------------- #
def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text.strip() if text else ""

    except Exception as e:
        print(f"[DOCX ERROR] {file_path}: {e}")

        # fallback (read raw content)
        try:
            with open(file_path, "rb") as f:
                return f.read().decode(errors="ignore")
        except Exception:
            return ""


# ---------------- TXT ---------------- #
def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read().strip()
    except Exception as e:
        print(f"[TXT ERROR] {file_path}: {e}")
        return ""


# ---------------- MAIN FUNCTION ---------------- #
def extract_text(file_path):
    """
    Detect file type and extract text accordingly
    """

    if not file_path or not os.path.exists(file_path):
        return ""

    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path_lower.endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_path_lower.endswith(".txt"):
        return extract_text_from_txt(file_path)

    else:
        print(f"[UNSUPPORTED FILE] {file_path}")
import PyPDF2
import docx2txt
import os


# ---------------- PDF ---------------- #
def extract_text_from_pdf(file_path):
    text = ""

    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                try:
                    content = page.extract_text()
                    if content:
                        text += content + " "
                except Exception:
                    continue  # skip problematic pages

        if not text.strip():
            print(f"[EMPTY PDF TEXT] {file_path}")

    except Exception as e:
        print(f"[PDF ERROR] {file_path}: {e}")

    return text.strip()


# ---------------- DOCX ---------------- #
def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text.strip() if text else ""

    except Exception as e:
        print(f"[DOCX ERROR] {file_path}: {e}")

        # fallback (read raw content)
        try:
            with open(file_path, "rb") as f:
                return f.read().decode(errors="ignore")
        except Exception:
            return ""


# ---------------- TXT ---------------- #
def extract_text_from_txt(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            return file.read().strip()
    except Exception as e:
        print(f"[TXT ERROR] {file_path}: {e}")
        return ""


# ---------------- MAIN FUNCTION ---------------- #
def extract_text(file_path):
    """
    Detect file type and extract text accordingly
    """

    if not file_path or not os.path.exists(file_path):
        return ""

    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path_lower.endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_path_lower.endswith(".txt"):
        return extract_text_from_txt(file_path)

    else:
        print(f"[UNSUPPORTED FILE] {file_path}")
        return ""