from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# --------------------
# Create app
# --------------------
app = FastAPI(title="AI Career API")

# --------------------
# Input schema
# --------------------
class UserProfile(BaseModel):
    skills: List[str]
    experience_level: str

# --------------------
# Root endpoint
# --------------------
@app.get("/")
def root():
    return {"message": "FastAPI backend is running"}

# --------------------
# Recommend endpoint
# --------------------
@app.post("/recommend")
def recommend(user: UserProfile):
    return {
        "recommendations": [
            {
                "role": "Data Analyst",
                "match_percentage": 78,
                "missing_skills": ["excel", "power bi"],
                "ai_score": 85
            },
            {
                "role": "Data Scientist",
                "match_percentage": 65,
                "missing_skills": ["machine learning", "statistics"],
                "ai_score": 80
            }
        ]
    }
