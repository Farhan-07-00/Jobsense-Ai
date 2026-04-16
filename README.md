🤖 JobSense AI — Smart Resume Matcher

An AI-powered Resume and Job Description Matching System built with Python and Streamlit that analyzes resumes, evaluates ATS compatibility, and provides skill-gap insights to improve job readiness.

🚀 Live Demo

🌐 Try the application here

https://jobsense-ai.streamlit.app
📌 Project Overview

JobSense AI helps job seekers understand how well their resume matches a job description.

The system analyzes the resume using Natural Language Processing (NLP) techniques and compares it with a job description to generate intelligent insights such as:

Resume-Job Match Score
ATS Compatibility Score
Skill Gap Analysis
Predicted Job Roles
AI Suggestions for Resume Improvement

This helps users improve their resumes and increase their chances of passing Applicant Tracking Systems (ATS) used by companies.

✨ Features
📄 Resume Parsing

Extracts structured information from resume PDFs using NLP.

🎯 Job Match Score

Calculates similarity between resume and job description using TF-IDF + Cosine Similarity.

🤖 ATS Score

Evaluates resume compatibility with Applicant Tracking Systems.

🧠 Skill Extraction

Detects technical skills from resumes using predefined job skill datasets.

📉 Skill Gap Analysis

Identifies missing skills required for the job.

💼 Job Role Prediction

Predicts suitable job categories based on detected skills.

📚 Learning Recommendations

Suggests relevant courses and learning resources.

🌐 Web Interface

Interactive UI built with Streamlit.

🛠️ Tech Stack

Frontend

Streamlit

Backend

Python

Machine Learning / NLP

Scikit-learn
NLTK
TF-IDF Vectorization
Cosine Similarity

Resume Processing

PyResParser
PDFMiner

Data Handling

Pandas
NumPy
⚙️ Installation

Clone the repository

git clone https://github.com/Farhan-07-00/jobsense-ai.git

Move into project directory

cd jobsense-ai

Install dependencies

pip install -r requirements.txt

Run the application

streamlit run app.py
📊 How It Works

1️⃣ User uploads a Resume (PDF)
2️⃣ User uploads or pastes a Job Description
3️⃣ The system processes text using NLP techniques
4️⃣ Resume and job description are compared
5️⃣ AI generates:

Match Score
ATS Score
Skill Gaps
Suggested Job Roles
📁 Project Structure
jobsense-ai
│
├── app.py
├── utils.py
├── keyword_lists.py
├── config.py
├── requirements.txt
│
├── static
│   └── style.css
📸 Screenshots
Resume Analysis Dashboard

Shows AI analysis including scores, skills, and recommendations.

🎯 Future Improvements
Semantic Resume Matching using Sentence Transformers
Resume Improvement Suggestions using LLMs
Resume PDF Report Generation
Support for more job domains
Better AI skill detection
👨‍💻 Author

Farhan Akhtar

B.Tech CSE Student
Adamas University

GitHub
https://github.com/Farhan-07-00

⭐ If you like this project

Give it a star ⭐ on GitHub.
