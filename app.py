from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename

# Import custom modules
from utils.parser import extract_text
from utils.preprocess import clean_text
from utils.semantic import compute_semantic_similarity
from utils.skills import extract_skills, skill_match_score
from utils.parser_advanced import parse_resume_details

# ------------------ CONFIG ------------------ #
app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# ------------------ HELPERS ------------------ #
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def compute_ats_score(skill_score, semantic_score, experience_score):
    """
    Final ATS scoring logic
    """
    return (
        0.6 * semantic_score +
        0.3 * skill_score +
        0.1 * experience_score
    )


# ------------------ ROUTES ------------------ #
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/match", methods=["POST"])
def match_resumes():
    try:
        print("FILES RECEIVED:", request.files)

        job_description = request.form.get("job_description")

        if not job_description:
            return jsonify({"error": "Job description is required"}), 400

        files = request.files.getlist("resumes")

        if not files:
            return jsonify({"error": "Please upload resumes"}), 400

        resumes_data = []

        # ------------------ PROCESS FILES ------------------ #
        for file in files:
            if file and allowed_file(file.filename):

                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                raw_text = extract_text(filepath)

                if not raw_text.strip():
                    print(f"[SKIPPED EMPTY FILE] {filename}")
                    continue

                cleaned_text = clean_text(raw_text)

                skills = extract_skills(cleaned_text)
                details = parse_resume_details(cleaned_text)

                resumes_data.append({
                    "filename": filename,
                    "text": cleaned_text,
                    "skills": skills,
                    "details": details
                })

        if len(resumes_data) == 0:
            return jsonify({"error": "No valid resumes could be processed"}), 400

        # ------------------ PROCESS JD ------------------ #
        jd_cleaned = clean_text(job_description)
        jd_skills = extract_skills(jd_cleaned)

        # ------------------ SEMANTIC SIMILARITY ------------------ #
        similarity_scores = compute_semantic_similarity(
            jd_cleaned,
            [r["text"] for r in resumes_data]
        )

        # ------------------ FINAL SCORING ------------------ #
        final_results = []

        for i, resume in enumerate(resumes_data):

            semantic_score = float(similarity_scores[i])
            skill_score = float(skill_match_score(jd_skills, resume["skills"]))

            # Experience score
            experience_years = resume["details"]["experience_years"]
            experience_score = min(experience_years / 5, 1)

            # Final ATS Score
            final_score = compute_ats_score(
                skill_score,
                semantic_score,
                experience_score
            )

            missing_skills = list(set(jd_skills) - set(resume["skills"]))

            final_results.append({
                "filename": resume["filename"],
                "semantic_score": round(semantic_score * 100, 2),
                "skill_score": round(skill_score * 100, 2),
                "experience_score": round(experience_score * 100, 2),
                "final_score": round(final_score * 100, 2),
                "skills": resume["skills"],
                "missing_skills": missing_skills,
                "experience_years": experience_years,
                "education": resume["details"]["education"],
                "companies": resume["details"]["companies"]
            })

        # ------------------ RANKING ------------------ #
        ranked_results = sorted(
            final_results,
            key=lambda x: x["final_score"],
            reverse=True
        )

        return jsonify({
            "success": True,
            "total_resumes": len(ranked_results),
            "results": ranked_results
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


# ------------------ RUN ------------------ #
if __name__ == "__main__":
    app.run(debug=True)