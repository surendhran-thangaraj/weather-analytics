import os
import subprocess
import sys
from dotenv import load_dotenv

# Load variables from .env

def download_kaggle_dataset():
    print("Checking Kaggle credentials...")
    load_dotenv()
    kaggle_user = os.getenv("KAGGLE_USERNAME")
    kaggle_key = os.getenv("KAGGLE_KEY")

    # Check credentials
    if not kaggle_user or not kaggle_key:
        print("Kaggle credentials not found!")
        print("Please set up Kaggle API in .env")
        print("Set env vars KAGGLE_USERNAME and KAGGLE_KEY")
        sys.exit(1)

    print("Kaggle credentials found")
    # Create data folder if not exists
    os.makedirs("data", exist_ok=True)

    # Run download command
    try:
        subprocess.run(
            [
                "kaggle",
                "datasets",
                "download",
                "-d",
                "nelgiriyewithana/global-weather-repository",
                "-p",
                "data/",
                "--unzip"
            ],
            check=True
        )
        print("Dataset downloaded successfully")

    except FileNotFoundError:
        print("Kaggle CLI not installed!")
        print("Run: pip install kaggle")
        sys.exit(1)

    except subprocess.CalledProcessError as e:
        print("Kaggle download failed!")
        print("Error:", e)
        sys.exit(1)

def __main__():
    download_kaggle_dataset()