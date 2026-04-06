# Fake Job Detection System

A full-stack machine learning application designed to identify fraudulent job postings. It uses a custom-trained Scikit-Learn Random Forest Classifier wrapped in a FastAPI backend, with a modern, glassmorphic React (Vite) frontend for easy user interaction.

## ✨ Features
- **AI-Powered Analysis**: Trained on the Employment Scam Aegean Dataset (EMSCAD).
- **Modern UI**: A responsive, glassmorphic frontend built with React and Vanilla CSS.
- **FastAPI Backend**: High-performance, fully typed Python API server.
- **Ready for Deployment**: Includes `render.yaml` for zero-downtime backend deployment on Render.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- A Kaggle Account (for downloading the dataset)

### 1. Backend Setup (Machine Learning & API)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Kaggle API key:
   - Go to Kaggle -> Settings -> Create New Token (`kaggle.json`).
   - Create a `.env` file in the `backend/` directory:
     ```env
     KAGGLE_USERNAME=your_username
     KAGGLE_KEY=your_key
     ```
4. Download the dataset & train the model:
   ```bash
   python download_data.py
   python train_model.py
   ```
5. Start the server:
   ```bash
   uvicorn app:app --reload --port 8000
   ```
  
### 2. Frontend Setup (React Application)

1. Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Open the provided Local URL (e.g., `http://localhost:5173`) in your browser.

## 📦 Deployment
- **Backend**: Can be deployed directly to [Render](https://render.com/) by connecting this repository (uses the included `render.yaml`).
- **Frontend**: Can be deployed to [Vercel](https://vercel.com/) with zero configuration. Ensure you add `VITE_API_URL` to your Vercel Environment Variables pointing to your live backend URL.
You can see project demo on https://ssdmpr-oj-ect.vercel.app/
## 🛡️ License
This project is open-source. For demonstration and educational purposes.
