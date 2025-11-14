from connectors.supabase import get_conn


def get_idioms_missing_examples(limit=100, retry_rejected=False):
    """
    Fetch idioms missing examples, respecting retry rules.

    retry_rejected=False:
        Skip ANY idiom that has been staged before (any review_status).
    retry_rejected=True:
        Only retry idioms where ALL existing staged rows for job='example'
        are 'rejected'. Skip idioms with pending/approved/applied rows.
    """
    with get_conn() as conn, conn.cursor() as cur:
        if retry_rejected:
            # Retry only idioms where ALL staged rows are rejected
            cur.execute(
                """
                SELECT i.id, i.title AS idiom
                FROM idioms i
                WHERE NOT EXISTS (
                        SELECT 1
                        FROM idiom_examples e
                        WHERE e.idiom_id = i.id
                )
                AND NOT EXISTS (
                        SELECT 1
                        FROM staging_scrapes s
                        WHERE s.idiom_id = i.id
                          AND s.job = 'example'
                          AND s.review_status IN ('pending','approved','applied')
                )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )
        else:
            # Skip ANY idiom that has *ever* had example staging attempts
            cur.execute(
                """
                SELECT i.id, i.title AS idiom
                FROM idioms i
                WHERE NOT EXISTS (
                        SELECT 1
                        FROM idiom_examples e
                        WHERE e.idiom_id = i.id
                )
                AND NOT EXISTS (
                        SELECT 1
                        FROM staging_scrapes s
                        WHERE s.idiom_id = i.id
                          AND s.job = 'example'
                )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )

        rows = cur.fetchall()
        return [{"id": r[0], "idiom": r[1]} for r in rows]
