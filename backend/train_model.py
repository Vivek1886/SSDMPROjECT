import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train():
    data_path = os.path.join("data", "fake_job_postings.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found. Please run download_data.py first.")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)
    
    # Fill missing values
    text_columns = ['title', 'company_profile', 'description', 'requirements', 'benefits']
    for col in text_columns:
        df[col] = df[col].fillna('')
    
    # Combine text columns to form a single text feature for simplicity
    print("Pre-processing text features...")
    df['combined_text'] = df['title'] + " " + df['company_profile'] + " " + df['description'] + " " + df['requirements']
    
    X = df['combined_text']
    y = df['fraudulent']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("Training model pipeline (TF-IDF + Random Forest)...")
    # Quick, robust base model pipeline
    model = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000, stop_words='english')),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced'))
    ])
    
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "fake_job_model.joblib")
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    print("Training complete and model saved!")

if __name__ == "__main__":
    train()
