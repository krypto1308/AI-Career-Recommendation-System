# ==================================
# AI Career Recommendation Dashboard
# ==================================

import streamlit as st
import requests

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎯",
    layout="centered"
)

# -------------------------------
# Title Section
# -------------------------------
st.title("🎯 AI Career Recommendation System")
st.write(
    "Get personalized career role recommendations based on your skills "
    "and job market intelligence."
)

st.divider()

# -------------------------------
# User Input Section
# -------------------------------
st.subheader("🧍 Your Profile")

experience = st.selectbox(
    "Select your experience level",
    ["Fresher", "Mid-Level", "Senior"]
)

skills_input = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="python, sql, pandas"
)

# -------------------------------
# Button Action
# -------------------------------
if st.button("🚀 Get Career Recommendations"):
    if not skills_input.strip():
        st.warning("⚠️ Please enter at least one skill.")
    else:
        user_skills = [s.strip().lower() for s in skills_input.split(",")]

        payload = {
            "skills": user_skills,
            "experience_level": experience
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend",
                json=payload
            )

            if response.status_code == 200:
                data = response.json()
                recommendations = data["recommendations"]

                st.success("✅ AI Recommendations Ready!")
                st.divider()

                # -------------------------------
                # Display Results
                # -------------------------------
                for idx, rec in enumerate(recommendations, 1):
                    with st.container():
                        st.subheader(f"🏆 Recommendation {idx}: {rec['role']}")

                        st.write("**Skill Match Percentage**")
                        st.progress(min(int(rec["match_percentage"]), 100))

                        st.metric(
                            label="AI Confidence Score",
                            value=rec["ai_score"]
                        )

                        if rec["missing_skills"]:
                            st.write("**Skills to Learn:**")
                            st.write(", ".join(rec["missing_skills"]))
                        else:
                            st.write("🎉 You already have all required skills!")

                        st.divider()

            else:
                st.error("❌ Failed to get recommendations from AI server.")

        except Exception as e:
            st.error("⚠️ Could not connect to AI backend.")
            st.write(str(e))
