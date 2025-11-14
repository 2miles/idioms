import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL_SUPABASE")


def get_conn():
    """Return a new psycopg2 connection to Supabase Postgres."""
    return psycopg2.connect(DB_URL)


def get_idioms_missing_definitions(limit=100, retry_rejected=False):
    """
    Fetch idioms missing definitions, respecting retry rules.

    retry_rejected=False:
        Skip ANY idiom that has been staged before, in ANY state.
    retry_rejected=True:
        Only retry rows where ALL staged rows are 'rejected'.
        Never touch pending/approved/applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        if retry_rejected:
            # Allow retry only when every staging row is rejected
            cur.execute(
                """
                SELECT i.id, i.title AS idiom
                FROM idioms i
                WHERE i.definition IS NULL
                  AND (
                        NOT EXISTS (
                            SELECT 1
                            FROM staging_scrapes s
                            WHERE s.idiom_id = i.id
                              AND s.job = 'definition'
                              AND s.review_status IN ('pending','approved','applied')
                        )
                  )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )
        else:
            # Skip ALL previously scraped (any review_status)
            cur.execute(
                """
                SELECT i.id, i.title AS idiom
                FROM idioms i
                WHERE i.definition IS NULL
                  AND NOT EXISTS (
                        SELECT 1
                        FROM staging_scrapes s
                        WHERE s.idiom_id = i.id
                          AND s.job = 'definition'
                  )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )

        rows = cur.fetchall()
        return [{"id": r[0], "idiom": r[1]} for r in rows]


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
