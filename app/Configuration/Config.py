import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_BASEURL = os.getenv("DB_BASEURL")
DB_NAME = os.getenv("DB_NAME")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")