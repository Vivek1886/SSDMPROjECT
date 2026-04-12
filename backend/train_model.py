import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

def train():
    data_path = os.path.join("data", "fake_job_postings.csv")
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    print("Loading dataset...")
    df = pd.read_csv(data_path)

    # Fill missing values
    text_columns = ['title', 'company_profile', 'description', 'requirements', 'benefits']
    for col in text_columns:
        df[col] = df[col].fillna('')

    # Better text combination (weighted)
    print("Pre-processing text...")
    df['combined_text'] = (
        df['title'] * 3 + " " +
        df['company_profile'] + " " +
        df['description'] + " " +
        df['requirements'] * 2 + " " +
        df['benefits']
    )

    X = df['combined_text']
    y = df['fraudulent']

    # Check imbalance
    print("\nClass distribution:")
    print(y.value_counts(normalize=True))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("\nTraining model (TF-IDF + Logistic Regression)...")

    model = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            stop_words='english',
            min_df=2,
            max_df=0.9
        )),
        ('clf', LogisticRegression(
            max_iter=1000,
            class_weight='balanced'
        ))
    ])

    model.fit(X_train, y_train)

    print("\nEvaluating model...")
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save model
    model_dir = "models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "fake_job_model.joblib")

    joblib.dump(model, model_path)
    print(f"\nModel saved at: {model_path}")

if __name__ == "__main__":
    train()