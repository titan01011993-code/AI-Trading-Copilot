import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
dotenv_path = BASE_DIR / ".env"

print(f"Loading .env from: {dotenv_path}")
print(f"File exists: {dotenv_path.exists()}")

load_dotenv(dotenv_path)

print("DHAN_CLIENT_ID =", os.getenv("DHAN_CLIENT_ID"))
print("DHAN_ACCESS_TOKEN =", os.getenv("DHAN_ACCESS_TOKEN"))

class Settings:
    APP_ENV = os.getenv("APP_ENV", "development")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    DHAN_CLIENT_ID = os.getenv("DHAN_CLIENT_ID")
    DHAN_ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

settings = Settings()