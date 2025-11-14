from connectors.supabase import get_conn


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
