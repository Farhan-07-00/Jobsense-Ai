import streamlit as st
import os
import pandas as pd
from datetime import datetime
#import database
import utils
from keyword_lists import COURSE_RECOMMENDATIONS, YOUTUBE_RECOMMENDATIONS
import config

# Page config
st.set_page_config(
    page_title="JobSense AI",
    page_icon="🎯",
    layout="wide"
)

# Load CSS
try:
    with open('static/style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except:
    pass


# Session state
if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False


# Initialize objects
matcher = utils.ResumeJobMatcher()
#db = database.Database()


# ------------------------------
# Display Results
# ------------------------------
def display_results(analysis):

    col1, col2, col3 = st.columns(3)

    # Match Score
    with col1:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg,#667eea,#764ba2);
        padding:2rem;border-radius:15px;text-align:center;color:white'>
        <h2>🎯 Match Score</h2>
        <h1>{analysis['match_score']}%</h1>
        </div>
        """, unsafe_allow_html=True)

    # ATS Score
    with col2:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg,#11998e,#38ef7d);
        padding:2rem;border-radius:15px;text-align:center;color:white'>
        <h2>🤖 ATS Score</h2>
        <h1>{analysis['ats_score']}%</h1>
        </div>
        """, unsafe_allow_html=True)

    # Job Matches
    with col3:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg,#f093fb,#f5576c);
        padding:2rem;border-radius:15px;text-align:center;color:white'>
        <h2>💼 Job Matches</h2>
        <h1>{len(analysis['predicted_jobs'])}</h1>
        </div>
        """, unsafe_allow_html=True)


    # ------------------------------
    # Skills vs Gaps
    # ------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🟢 Your Skills Found")

        skills = sorted(analysis["resume_skills"])
        skills_df = pd.DataFrame({"Skills": skills})

        st.dataframe(skills_df, use_container_width=True, height=300)

    with col2:

        st.markdown("### 🔴 Skill Gaps (Learn These!)")

        gaps_df = pd.DataFrame({"Missing Skills": analysis["skill_gaps"]})

        st.dataframe(gaps_df, use_container_width=True, height=300)

        st.markdown("### 💡 AI Suggestions to Improve Resume")

        missing = analysis["skill_gaps"]

        if missing:
             st.write("Improve your resume by adding these skills:")

             for skill in missing[:5]:
              st.markdown(f"📚 Consider learning **{skill}** to increase your match score")

        else:
             st.success("🎉 Your resume already matches most job requirements!")


    # -----------------------------
    # Resume Insights
    # ------------------------------

    st.markdown("### 🧠 Resume Insights")

    st.write(f"Detected Skills: **{len(analysis['resume_skills'])}**")
    st.write(f"Missing Skills: **{len(analysis['skill_gaps'])}**")


    # ------------------------------
    # Job Predictions
    # ------------------------------

    st.markdown("### 🎯 Predicted Job Fields")

    for i, job in enumerate(analysis["predicted_jobs"], 1):

        st.success(f"{i}. {job} 🚀 Recommended Career Path")

        job_text = analysis["job_text"]

        job_words = set(job_text.split())

        matching_skills = [
            skill for skill in analysis["resume_skills"]
            if skill.lower() in job_words
        ]

        st.subheader("⭐ Matching Skills with Job Description")

        st.write(matching_skills)


# ------------------------------
# Main UI
# ------------------------------

st.title("🎯 Smart Resume & Job Matcher")

st.markdown(
"### Upload your Resume and Job Description to analyze compatibility using JobSense AI."
)

st.info("💡 Tip: Paste detailed job descriptions for more accurate matching.")


# ------------------------------
# File Upload
# ------------------------------

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📄 Your Resume")

    resume_file = st.file_uploader(
        "Upload Resume (PDF)",
        type=["pdf"],
        key="resume"
    )


with col2:

    st.markdown("### 💼 Job Description")

    job_option = st.radio(
        "Choose Input Method",
        ["Upload File", "Paste Text"]
    )

    job_file = None
    job_text_input = ""

    if job_option == "Upload File":

        job_file = st.file_uploader(
            "Upload Job Description (PDF/TXT)",
            type=["pdf","txt"],
            key="job"
        )

    else:

        job_text_input = st.text_area(
            "Paste Job Description Here",
            height=200
        )


# ------------------------------
# Analyze Button
# ------------------------------

if st.button("🚀 ANALYZE MATCH", use_container_width=True):

    if resume_file and (job_file or job_text_input):

        with st.spinner("🤖 AI analyzing resume..."):

            resume_path = f"temp_resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

            with open(resume_path,"wb") as f:
                f.write(resume_file.getbuffer())


            if job_file:

                job_path = f"temp_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{job_file.name.split('.')[-1]}"

                with open(job_path,"wb") as f:
                    f.write(job_file.getbuffer())

            else:

                job_path = f"temp_job_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

                with open(job_path,"w",encoding="utf-8") as f:
                    f.write(job_text_input)


            analysis = matcher.analyze_resume_job_match(
                resume_path,
                job_path
            )

            st.session_state.analysis = analysis
            st.session_state.analysis_done = True

            os.remove(resume_path)
            os.remove(job_path)

            st.success("✅ Analysis Complete!")

    else:

        st.error("Please upload resume and job description.")


# ------------------------------
# Show Results
# ------------------------------

if st.session_state.get("analysis_done",False):

    st.divider()

    st.subheader("📊 Analysis Results")

    display_results(st.session_state.analysis)


    # Score Quality
    analysis = st.session_state.analysis
    score = analysis["match_score"]

    if score >= 75:

        st.balloons()

        st.success(f"🎉 Excellent Match! ({score}%)— Your resume aligns very well with the job requirements.")

    elif score >= 50:

        st.warning(f"👍 Moderate Match ({score}%) Your profile matches many requirements, but adding a few key skills could improve compatibility.")

    else:

        st.error(f"⚠️ Low Match ({score}%) Your resume doesn't align well with the job requirements. ")


    # Download Report

    report = f"""
Match Score: {analysis['match_score']}%
ATS Score: {analysis['ats_score']}%

Skills Found:
{', '.join(analysis['resume_skills'])}

Missing Skills:
{', '.join(analysis['skill_gaps'])}
"""


    st.download_button(
        label="📥 Download Analysis Report",
        data=report,
        file_name="resume_analysis.txt",
        mime="text/plain"
    )


    # ------------------------------
    # Recommendations
    # ------------------------------

    st.markdown("### 🚀 Personalized Learning")

    jobs = analysis["predicted_jobs"]

    for job in jobs[:2]:

        with st.expander(f"Improve for {job}"):

            col1,col2 = st.columns(2)

            with col1:

                if job in COURSE_RECOMMENDATIONS:

                    st.markdown("**Top Courses**")

                    for course,link in COURSE_RECOMMENDATIONS[job]:

                        st.markdown(f"- [{course}]({link})")


            with col2:

                if job in YOUTUBE_RECOMMENDATIONS:

                    st.markdown("**YouTube Learning**")

                    for channel,link in YOUTUBE_RECOMMENDATIONS[job]:

                        st.markdown(f"- [{channel}]({link})")


# ------------------------------
# Sidebar
# ------------------------------

with st.sidebar:

    st.markdown("### 📊 Quick Stats")

    if st.session_state.get("analysis_done"):

        score = st.session_state.analysis["match_score"]

        ats = st.session_state.analysis["ats_score"]

        st.metric("Job Fit Score", f"{score}%")
        st.progress(int(score))

        st.metric("ATS Compatibility", f"{ats}%")
        st.progress(int(ats))


    st.markdown("---")

    st.markdown("""
### 🤖 JobSense AI

AI-powered Resume Matching System

**Features**

• Resume-Job Matching  
• Skill Gap Detection  
• ATS Score Evaluation
""")


# Footer

st.markdown("---")

st.markdown(
"<p style='text-align:center;color:grey;'>🎯 Powered by AI | Upload resume + job description → Get instant match score</p>",
unsafe_allow_html=True
)
