import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/experienceloop.db")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY", "")
HINDSIGHT_URL = os.getenv("HINDSIGHT_URL", "https://api.hindsight.vectorize.io")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "experienceloop")
