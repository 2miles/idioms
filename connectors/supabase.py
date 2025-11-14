import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL_SUPABASE")


def get_conn():
    """Return a new psycopg2 connection to Supabase Postgres."""
    return psycopg2.connect(DB_URL)
