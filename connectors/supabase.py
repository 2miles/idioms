import os, psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL_SUPABASE")


def get_conn():
    return psycopg2.connect(DB_URL)


def get_idioms_missing_definitions(limit=100):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, title AS idiom
            FROM idioms
            WHERE definition IS NULL
            ORDER BY id
            LIMIT %s;
        """,
            (limit,),
        )
        return [{"id": r[0], "idiom": r[1]} for r in cur.fetchall()]


def upsert_definition(idiom_id, definition, source):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE idioms
            SET definition = %s,
                definition_source = %s,
                definition_scraped_at = NOW()
            WHERE id = %s;
        """,
            (definition, source, idiom_id),
        )
        conn.commit()


def log_scrape_attempt(idiom_id, job, status, source, error_msg=None):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO scrape_attempts (idiom_id, job, status, source, last_attempt_at, error_msg)
            VALUES (%s, %s, %s, %s, NOW(), %s)
            ON CONFLICT (idiom_id, job, source)
            DO UPDATE SET
                status = EXCLUDED.status,
                last_attempt_at = NOW(),
                attempt_count = scrape_attempts.attempt_count + 1,
                error_msg = EXCLUDED.error_msg;
        """,
            (idiom_id, job, status, source, error_msg),
        )
        conn.commit()


# Then in your pipeline:
# - after each scrape → call log_scrape_attempt(...)
# - if it succeeds → also call upsert_definition(...)
