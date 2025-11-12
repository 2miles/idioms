import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL_SUPABASE")


def get_conn():
    """Return a new psycopg2 connection to Supabase Postgres."""
    return psycopg2.connect(DB_URL)


def get_idioms_missing_definitions(limit=100):
    """Fetch idioms with no definition (for scraping)."""
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


# not yet used
# refactor later to use this function
def stage_row(idiom_id, job, content, status):
    """Insert a single staged result into staging_scrapes."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO staging_scrapes (idiom_id, job, content, status)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
            """,
            (idiom_id, job, content, status),
        )
        conn.commit()


# def upsert_definition(idiom_id, definition, source):
#     with get_conn() as conn, conn.cursor() as cur:
#         cur.execute(
#             """
#             UPDATE idioms
#             SET definition = %s,
#                 definition_source = %s,
#                 definition_scraped_at = NOW()
#             WHERE id = %s;
#         """,
#             (definition, source, idiom_id),
#         )
#         conn.commit()


# def log_scrape_attempt(idiom_id, job, status, source, error_msg=None):
#     with get_conn() as conn, conn.cursor() as cur:
#         cur.execute(
#             """
#             INSERT INTO scrape_attempts (idiom_id, job, status, source, last_attempt_at, error_msg)
#             VALUES (%s, %s, %s, %s, NOW(), %s)
#             ON CONFLICT (idiom_id, job, source)
#             DO UPDATE SET
#                 status = EXCLUDED.status,
#                 last_attempt_at = NOW(),
#                 attempt_count = scrape_attempts.attempt_count + 1,
#                 error_msg = EXCLUDED.error_msg;
#         """,
#             (idiom_id, job, status, source, error_msg),
#         )
#         conn.commit()
