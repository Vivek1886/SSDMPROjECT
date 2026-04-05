import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

app = FastAPI(title="Fake Job Detection API")

# Setup CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, lock this down to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = os.path.join("models", "fake_job_model.joblib")
model = None

@app.on_event("startup")
def load_model():
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print("Model loaded successfully.")
    else:
        print("Warning: Model not found. The /predict endpoint will fail. Run train_model.py first.")

class JobPosting(BaseModel):
    title: str = ""
    company_profile: str = ""
    description: str = ""
    requirements: str = ""

@app.get("/")
def read_root():
    return {"message": "Welcome to the Fake Job Detection API. Use the /predict endpoint."}

@app.post("/predict")
def predict_job(job: JobPosting):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded on the server.")
    
    # Combine text the same way as during training
    combined_text = f"{job.title} {job.company_profile} {job.description} {job.requirements}"
    
    # Predict
    prediction = model.predict([combined_text])[0]
    probabilities = model.predict_proba([combined_text])[0]
    
    is_fake = bool(prediction == 1)
    # Return probability of being fake
    fake_prob = float(probabilities[1])
    
    return {
        "is_fake": is_fake,
        "fake_probability": fake_prob
    }
