from connectors.supabase import get_conn


def stage_origins(results: list[dict]) -> dict:
    """
    Insert scraped AI origins into staging_scrapes.

    Each row in `results` must have:
        - idiom_id
        - job = 'origin'
        - content (origin text, may be empty)
        - status ('success', 'error', 'http_XXX')

    Successful items become review_status='pending'.
    Others become review_status='rejected'.

    Returns summary dict:
        { "success": int, "rejected": int, "total": int }
    """

    with get_conn() as conn, conn.cursor() as cur:
        for row in results:
            review_status = "pending" if row["status"] == "success" else "rejected"

            cur.execute(
                """
                INSERT INTO staging_scrapes (idiom_id, job, content, status, review_status)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    row["idiom_id"],
                    row["job"],  # should be 'origin'
                    row["content"],
                    row["status"],
                    review_status,
                ),
            )

        conn.commit()

    summary = {
        "success": sum(1 for r in results if r["status"] == "success"),
        "rejected": sum(1 for r in results if r["status"] != "success"),
        "total": len(results),
    }

    return summary
