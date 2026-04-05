import os
import zipfile
import subprocess
from dotenv import load_dotenv

load_dotenv()

def download_emscad():
    """
    Downloads the 'Employment Scam Aegean Dataset' (EMSCAD) or the standard
    'Real or Fake Fake Job Posting Prediction' dataset using Kaggle CLI.
    Ensure you have your Kaggle credentials set up!
    """
    dataset_name = "shivamb/real-or-fake-fake-jobposting-prediction"
    download_dir = "data"
    
    os.makedirs(download_dir, exist_ok=True)
    
    print(f"Downloading {dataset_name} from Kaggle...")
    try:
        # We call the kaggle CLI tool directly
        subprocess.run(["kaggle", "datasets", "download", "-d", dataset_name, "-p", download_dir], check=True)
        
        # Unzip the downloaded file
        zip_path = os.path.join(download_dir, "real-or-fake-fake-jobposting-prediction.zip")
        if os.path.exists(zip_path):
            print("Unzipping dataset...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(download_dir)
            print("Dataset downloaded and extracted successfully to the 'data' directory!")
            os.remove(zip_path) # Clean up the zip file
        else:
            print("Zip file not found after download.")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("\nNote: Please make sure you have 'kaggle' installed, and your kaggle.json "
              "is placed in '~/.kaggle/' (or C:\\Users\\<user>\\.kaggle\\ on Windows).")

if __name__ == "__main__":
    download_emscad()
