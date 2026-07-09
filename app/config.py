"""
Application Configuration
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"
DATABASE_DIR = BASE_DIR / "database"

for folder in [
    DATA_DIR,
    REPORT_DIR,
    LOG_DIR,
    DATABASE_DIR,
]:
    folder.mkdir(exist_ok=True)