from connectors.supabase import get_conn


def get_idioms_missing_origins(limit=50, retry_rejected=False):
    """
    Fetch idioms that don't yet have an entry in idiom_origins_ai, respecting retry rules.

    retry_rejected=False:
        Skip ANY idiom that has been staged before for job='origin'.
    retry_rejected=True:
        Only retry idioms where ALL staged rows for job='origin'
        are rejected/applied (no pending/approved).
    """
    with get_conn() as conn, conn.cursor() as cur:
        if retry_rejected:
            cur.execute(
                """
                SELECT i.id, i.title AS idiom, i.definition
                FROM idioms i
                WHERE NOT EXISTS (
                        SELECT 1
                        FROM idiom_origins_ai o
                        WHERE o.idiom_id = i.id
                )
                  AND NOT EXISTS (
                        SELECT 1
                        FROM staging_scrapes s
                        WHERE s.idiom_id = i.id
                          AND s.job = 'origin'
                          AND s.review_status IN ('pending','approved')
                )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )
        else:
            cur.execute(
                """
                SELECT i.id, i.title AS idiom, i.definition
                FROM idioms i
                WHERE NOT EXISTS (
                        SELECT 1
                        FROM idiom_origins_ai o
                        WHERE o.idiom_id = i.id
                )
                  AND NOT EXISTS (
                        SELECT 1
                        FROM staging_scrapes s
                        WHERE s.idiom_id = i.id
                          AND s.job = 'origin'
                )
                ORDER BY i.id
                LIMIT %s;
                """,
                (limit,),
            )

        rows = cur.fetchall()
        return [{"id": r[0], "idiom": r[1], "definition": r[2]} for r in rows]
