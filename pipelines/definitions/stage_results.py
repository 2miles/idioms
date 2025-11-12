from pipelines.definitions.scrape_sources import scrape_free_dictionary

from connectors.supabase import get_conn


def stage_definitions(results):
    """
    Insert scraped definitions into staging_scrapes.
    Inserts all results, marking 'success' as pending and others as rejected.
    Returns a summary dict for optional logging.
    """
    with get_conn() as conn, conn.cursor() as cur:
        for row in results:
            review_status = "pending" if row["status"] == "success" else "rejected"
            cur.execute(
                """
                INSERT INTO staging_scrapes (idiom_id, job, content, status, review_status)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (idiom_id, job) DO UPDATE
                    SET status = EXCLUDED.status,
                        content = EXCLUDED.content,
                        review_status = EXCLUDED.review_status;
                """,
                (row["idiom_id"], row["job"], row["content"], row["status"], review_status),
            )
        conn.commit()

    summary = {
        "success": sum(1 for r in results if r["status"] == "success"),
        "rejected": sum(1 for r in results if r["status"] != "success"),
        "total": len(results),
    }
    return summary
