# ===============================
# AI Career Recommendation API
# ===============================

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pandas as pd
import numpy as np
import joblib
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------------------
# App Initialization
# -------------------------------
app = FastAPI(
    title="AI Career Recommendation System",
    description="AI-powered career role and skill gap recommendation",
    version="1.0"
)

# -------------------------------
# Base Directory (IMPORTANT)
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------
# Load Data
# -------------------------------
role_skill_map = pd.read_csv(
    os.path.join(BASE_DIR, "data", "processed", "role_skill_map.csv")
)

skill_demand = pd.read_csv(
    os.path.join(BASE_DIR, "data", "processed", "skill_demand_scores.csv")
)

# Convert string list → real list
role_skill_map["Role_Skills"] = role_skill_map["Role_Skills"].apply(eval)

# Create demand dictionary
demand_dict = dict(
    zip(skill_demand["Skill"], skill_demand["Demand_Score"])
)

# -------------------------------
# Load ML Models
# -------------------------------
nn_model = joblib.load(
    os.path.join(BASE_DIR, "models", "nn_role_ranker.pkl")
)

scaler = joblib.load(
    os.path.join(BASE_DIR, "models", "feature_scaler.pkl")
)

# -------------------------------
# Prepare TF-IDF
# -------------------------------
role_skill_map["skill_text"] = role_skill_map["Role_Skills"].apply(
    lambda skills: " ".join(skills)
)

vectorizer = TfidfVectorizer()
role_vectors = vectorizer.fit_transform(role_skill_map["skill_text"])

# -------------------------------
# Input Schema
# -------------------------------
class UserProfile(BaseModel):
    skills: List[str]
    experience_level: str

# -------------------------------
# Core Recommendation Logic
# -------------------------------
def recommend_roles(user_skills: List[str]):
    user_skill_text = " ".join(user_skills)
    user_vector = vectorizer.transform([user_skill_text])

    similarity_scores = cosine_similarity(user_vector, role_vectors)[0]

    results = []

    for idx, row in role_skill_map.iterrows():
        role = row["Title"]
        role_skills = row["Role_Skills"]

        missing_skills = list(set(role_skills) - set(user_skills))

        gap_severity = sum(
            demand_dict.get(skill, 0) for skill in missing_skills
        )

        avg_demand = np.mean(
            [demand_dict.get(skill, 0) for skill in role_skills]
        )

        features = np.array([[
            similarity_scores[idx] * 100,
            gap_severity,
            len(missing_skills),
            avg_demand
        ]])

        features_scaled = scaler.transform(features)
        ai_score = nn_model.predict(features_scaled)[0]

        results.append({
            "role": role,
            "match_percentage": round(similarity_scores[idx] * 100, 2),
            "missing_skills": missing_skills,
            "ai_score": round(float(ai_score), 2)
        })

    return sorted(results, key=lambda x: x["ai_score"], reverse=True)[:3]

# -------------------------------
# API Endpoints
# -------------------------------
@app.get("/")
def home():
    return {"status": "AI Career Recommendation API is running"}

@app.post("/recommend")
def recommend(user: UserProfile):
    recommendations = recommend_roles(user.skills)
    return {
        "input_skills": user.skills,
        "experience_level": user.experience_level,
        "recommendations": recommendations
    }
