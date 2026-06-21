# core/db.py

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase

load_dotenv()

db = SQLDatabase.from_uri(
    "postgresql://postgres:cbj123@localhost:5432/E-Commerce",
    engine_args={
        "connect_args": {
            "options": "-c statement_timeout=10000"
        }
    }
)