import streamlit as st
import requests

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="AI Career Recommendation",
    page_icon="🎯",
    layout="centered"
)

st.title("🎯 AI Career Recommendation System")
st.write("Enter your skills and get career recommendations.")

st.divider()

# -----------------------------
# User input
# -----------------------------
experience_level = st.selectbox(
    "Select your experience level",
    ["Fresher", "Mid-Level", "Senior"]
)

skills_text = st.text_input(
    "Enter your skills (comma separated)",
    placeholder="python, sql, pandas"
)

# -----------------------------
# Backend API (LOCAL)
# -----------------------------
API_URL = "https://ai-career-recommendation-api.onrender.com/recommend"

st.caption(f"Connected to backend: {API_URL}")

# -----------------------------
# Button action
# -----------------------------
if st.button("🚀 Get Recommendations"):
    if skills_text.strip() == "":
        st.warning("Please enter at least one skill.")
    else:
        skills = [s.strip().lower() for s in skills_text.split(",")]

        payload = {
            "skills": skills,
            "experience_level": experience_level
        }

        try:
            response = requests.post(API_URL, json=payload)

            if response.status_code == 200:
                data = response.json()
                recommendations = data["recommendations"]

                st.success("Recommendations generated!")
                st.divider()

                for i, rec in enumerate(recommendations, start=1):
                    st.subheader(f"🏆 Recommendation {i}: {rec['role']}")

                    st.write("**Skill Match Percentage**")
                    st.progress(min(int(rec["match_percentage"]), 100))

                    st.metric("AI Confidence Score", rec["ai_score"])

                    if rec["missing_skills"]:
                        st.write("**Skills to Learn:**")
                        st.write(", ".join(rec["missing_skills"]))
                    else:
                        st.write("🎉 You already match this role well!")

                    st.divider()
            else:
                st.error(f"Backend error: {response.status_code}")
                st.write(response.text)

        except Exception as e:
            st.error("Could not connect to backend")
            st.write(e)
