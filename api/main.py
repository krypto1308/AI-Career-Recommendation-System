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
    recommendations = recommend_roles(user.skills)

    return {
        "input_skills": user.skills,
        "experience_level": user.experience_level,
        "recommendations": recommendations
    }
