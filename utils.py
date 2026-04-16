import nltk

# Download NLTK resources if missing
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

import re
from pyresparser import ResumeParser
from pdfminer.high_level import extract_text
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from keyword_lists import JOB_KEYWORDS


class ResumeJobMatcher:

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))

        # words that appear in resumes but are NOT skills
        self.noise_words = {
            "name","email","phone","summary","experience","project","projects",
            "education","responsibilities","responsibility","team","worked",
            "work","using","use","page","pages","easy","ensure","maximum",
            "requirements","developer","implementing"
        }

    # -----------------------------
    # Extract text from PDF or TXT
    # -----------------------------
    def extract_full_text(self, file_path):

        try:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()
            else:
                text = extract_text(file_path)

            text = re.sub(r"\s+", " ", text)
            return text.lower()

        except Exception as e:
            print("Text extraction error:", e)
            return ""

    # -----------------------------
    # Resume parsing
    # -----------------------------
    def parse_resume(self, pdf_path):

        try:
            return ResumeParser(pdf_path).get_extracted_data()
        except:
            return {}

    # -----------------------------
    # NLP preprocessing
    # -----------------------------
    def preprocess_text(self, text):

        tokens = word_tokenize(text)

        cleaned = [
            w for w in tokens
            if w.isalpha()
            and w not in self.stop_words
            and w not in self.noise_words
            and len(w) > 2
        ]

        return cleaned

    # -----------------------------
    # Skill extraction
    # -----------------------------
    def extract_skills(self, text):

        text = text.lower()

        detected_skills = []

        # search skills from predefined job keywords
        for job, skills in JOB_KEYWORDS.items():

            for skill in skills:

                if skill.lower() in text:
                    detected_skills.append(skill.lower())

        return list(set(detected_skills))

    # -----------------------------
    # TF-IDF matching
    # -----------------------------
    def calculate_match_score(self, resume_text, job_text):

        resume_words = " ".join(self.preprocess_text(resume_text))
        job_words = " ".join(self.preprocess_text(job_text))

        vectorizer = TfidfVectorizer(max_features=2000)

        tfidf_matrix = vectorizer.fit_transform([resume_words, job_words])

        similarity = cosine_similarity(
            tfidf_matrix[0:1],
            tfidf_matrix[1:2]
        )[0][0]

        return round(similarity * 100, 2)

    # -----------------------------
    # ATS score
    # -----------------------------
    def ats_score(self, resume_text, job_text):

        job_keywords = set(self.preprocess_text(job_text))
        resume_words = set(self.preprocess_text(resume_text))

        matches = len(job_keywords.intersection(resume_words))

        if len(job_keywords) == 0:
            return 0

        return round((matches / len(job_keywords)) * 100, 2)

    # -----------------------------
    # Skill gap
    # -----------------------------
    def skill_gap_analysis(self, resume_skills, job_keywords):

        resume_set = set(resume_skills)

        missing = [s for s in job_keywords if s not in resume_set]

        return missing[:10]

    # -----------------------------
    # Job prediction
    # -----------------------------
    def predict_job_field(self, skills, full_text):

        text = full_text + " " + " ".join(skills)

        scores = {}

        for job, keywords in JOB_KEYWORDS.items():

            score = sum(
                1 for k in keywords if k.lower() in text
            )

            scores[job] = score

        sorted_jobs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [job for job, score in sorted_jobs if score > 0][:3]


    def analyze_resume_job_match(self, resume_path, job_desc_path):

        resume_text = self.extract_full_text(resume_path)
        job_text = self.extract_full_text(job_desc_path)

        parsed_data = self.parse_resume(resume_path)

        resume_skills = self.extract_skills(resume_text)

        match_score = self.calculate_match_score(resume_text, job_text)

        ats = self.ats_score(resume_text, job_text)

        predicted_jobs = self.predict_job_field(resume_skills, resume_text)

        job_keywords = []

        job_text_lower = job_text.lower()

        for job, skills in JOB_KEYWORDS.items():
           for skill in skills:
               if skill.lower() in job_text_lower:
                   job_keywords.append(skill.lower())

        job_keywords = sorted(list(set(job_keywords)))

        skill_gaps = self.skill_gap_analysis(resume_skills, job_keywords)

        return {
            "parsed_data": parsed_data,
            "match_score": match_score,
            "ats_score": ats,
            "resume_skills": resume_skills,
            "predicted_jobs": predicted_jobs,
            "skill_gaps": skill_gaps,
            "resume_text": resume_text,
            "job_text": job_text
 }
